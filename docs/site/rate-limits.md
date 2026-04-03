# Rate Limit Pacing

specsmith ships a proactive rate-limit scheduler so AI provider requests are paced *before* dispatch rather than only reacting after a `429` error.

## The Problem

Provider rate limits come in two flavours:

- **RPM** — requests per minute
- **TPM** — tokens per minute (input + output combined)

A scheduler that only reacts after a 429 wastes time, thrashes concurrency, and causes avoidable failures in long-running agentic sessions. specsmith's scheduler is proactive: it checks both the rolling RPM and TPM windows before each dispatch, and sleeps until the budget refills if needed.

## How It Works

1. **Profile lookup** — each `(provider, model)` pair has a `ModelRateLimitProfile` with `rpm_limit`, `tpm_limit`, a `utilization_target` (default 70 %), and a `concurrency_cap`.
2. **Pre-dispatch pacing** — `acquire()` estimates `input_tokens + max_output_tokens`, checks whether enough budget remains in the current 60-second rolling window, and sleeps until the window refills if not.
3. **429 handling** — `record_rate_limit()` parses provider-prescribed wait times (e.g. OpenAI's `"Please try again in 10.793s"` text), halves the concurrency cap, and returns the delay before retry.
4. **Concurrency restoration** — after a configurable number of consecutive successes (`restore_after_successes`, default 3), the concurrency cap is gradually restored to its base value.
5. **Moving averages** — the scheduler continuously tracks an exponential moving average of requests and tokens per window so you can see utilisation trends.

## Built-in Profiles

specsmith ships conservative default profiles for common provider/model paths.
These are starting points — your account tier may differ.

| Provider | Model | RPM | TPM |
|----------|-------|-----|-----|
| openai | gpt-4o | 500 | 30,000,000 |
| openai | gpt-4o-mini | 500 | 200,000,000 |
| openai | gpt-4-turbo | 500 | 800,000 |
| openai | gpt-3.5-turbo | 3500 | 90,000 |
| openai | o1 | 500 | 30,000,000 |
| openai | o1-mini / o3-mini | 1000 | 200,000,000 |
| openai | gpt-5.4 | 60 | 500,000 |
| openai | * (wildcard) | 500 | 500,000 |
| anthropic | claude-opus-4 | 2000 | 40,000,000 |
| anthropic | claude-sonnet-4 | 2000 | 40,000,000 |
| anthropic | claude-haiku-3-5 | 2000 | 200,000,000 |
| anthropic | * (wildcard) | 2000 | 40,000,000 |
| google | gemini-1.5-pro | 360 | 4,000,000 |
| google | gemini-1.5-flash / 2.0-flash / 2.5-pro | 1000 | 4,000,000 |
| google | * (wildcard) | 360 | 4,000,000 |

Wildcard entries (`provider/*`) match any model for that provider that does not have an exact profile. Resolution order: exact key → provider wildcard → model wildcard → global wildcard.

## CLI Commands

### View built-in profiles

```bash
specsmith credits limits defaults
```

### Install defaults into your project

```bash
specsmith credits limits defaults --install --project-dir ./my-project
```

Merges built-in profiles into `.specsmith/model-rate-limits.json`. Existing local overrides are preserved — they always take precedence.

### Set a custom profile

Override the built-in defaults when your account has a different tier:

```bash
specsmith credits limits set \
  --provider openai \
  --model gpt-5.4 \
  --rpm 120 \
  --tpm 600000 \
  --target 0.80 \
  --concurrency 2 \
  --project-dir ./my-project
```

### List active profiles

```bash
specsmith credits limits list --project-dir ./my-project
```

### Show rolling-window snapshot

See live RPM/TPM utilisation and concurrency state for a model:

```bash
specsmith credits limits status --provider openai --model gpt-5.4
```

Output example:

```
openai/gpt-5.4
  RPM: 3 / 42 (limit 60, target 42)
  TPM: 341,693 / 350,000 (limit 500,000)
  Utilization: RPM 7.1%  TPM 97.6%
  Concurrency: 1 in-flight / 1 cap (base 1)
  Moving avg:  2.5 req/window  280,000 tok/window
```

## Persistent State

Profile overrides are stored at `.specsmith/model-rate-limits.json` (gitignored).
Rolling-window runtime state is stored at `.specsmith/model-rate-limit-state.json` (also gitignored) and is rehydrated on the next scheduler load so pacing is consistent across separate CLI invocations.

## Python API

```python
from specsmith.rate_limits import (
    BUILTIN_PROFILES,
    load_rate_limit_profiles,
    load_rate_limit_scheduler,
)
from pathlib import Path

root = Path(".")
profiles = load_rate_limit_profiles(root, defaults=BUILTIN_PROFILES)
scheduler = load_rate_limit_scheduler(root, profiles)

# Before dispatching a request
reservation = scheduler.acquire(
    "openai", "gpt-5.4",
    estimated_input_tokens=5000,
    max_output_tokens=2000,
)

# ... make the API call ...

# After success
scheduler.record_success(
    reservation,
    actual_input_tokens=4800,
    actual_output_tokens=1900,
)

# After a 429
delay = scheduler.record_rate_limit(reservation, exc, attempt=1)
time.sleep(delay)
```

See `src/specsmith/rate_limits.py` for the full API reference.
