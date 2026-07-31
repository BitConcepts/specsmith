"""Versioned benchmark profiles for cheap admission and release evidence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BenchmarkProfile:
    """One immutable task, condition, and repetition contract."""

    name: str
    tasks: tuple[str, ...]
    conditions: tuple[str, ...]
    repetitions: int
    purpose: str


PROFILES: dict[str, BenchmarkProfile] = {
    "admission": BenchmarkProfile(
        name="admission",
        tasks=("T28",),
        conditions=("SPECSMITH_FULL",),
        repetitions=1,
        purpose="One paid long-horizon cell before any model receives repetition budget.",
    ),
    "controller-admission": BenchmarkProfile(
        name="controller-admission",
        tasks=("T1", "T10", "T11", "T13", "T28"),
        conditions=("SPECSMITH_FULL",),
        repetitions=1,
        purpose="One paid cell per controller path changed by an optimization.",
    ),
    "release-controls": BenchmarkProfile(
        name="release-controls",
        tasks=("T10", "T13", "T28"),
        conditions=("CURSOR_RULES", "SPECSMITH_FULL"),
        repetitions=10,
        purpose="Mandatory correctness and long-horizon controls for release evidence.",
    ),
    "broad-release": BenchmarkProfile(
        name="broad-release",
        tasks=("T1", "T2", "T6", "T7", "T10", "T11", "T13", "T28"),
        conditions=("CURSOR_RULES", "SPECSMITH_FULL"),
        repetitions=10,
        purpose="Same-commit broad release claim across the versioned eight-task grid.",
    ),
    "substitution-screen": BenchmarkProfile(
        name="substitution-screen",
        tasks=("T1", "T10", "T13", "T28"),
        conditions=("UNGOVERNED", "SPECSMITH_FULL"),
        repetitions=5,
        purpose=(
            "Two-by-two smaller/frontier model screen that separates model capability "
            "from governance lift."
        ),
    ),
    "substitution-release": BenchmarkProfile(
        name="substitution-release",
        tasks=("T1", "T2", "T6", "T7", "T10", "T11", "T13", "T28"),
        conditions=("UNGOVERNED", "SPECSMITH_FULL"),
        repetitions=10,
        purpose=(
            "Release-grade two-by-two lower-tier/frontier model comparison across "
            "the complete versioned task grid."
        ),
    ),
    "publication-matched": BenchmarkProfile(
        name="publication-matched",
        tasks=("T28", "T29", "T30"),
        conditions=("UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"),
        repetitions=10,
        purpose=(
            "Preregistered publication grid across two synthetic polyglot repositories "
            "and one pinned independent upstream repository."
        ),
    ),
    "publication-real-repository-recovery": BenchmarkProfile(
        name="publication-real-repository-recovery",
        tasks=("T30",),
        conditions=("UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"),
        repetitions=10,
        purpose=(
            "Frozen V2 recovery of the invalidated V1 real-repository stratum "
            "with corrected evaluator and completion invariants."
        ),
    ),
    "publication-open-admission": BenchmarkProfile(
        name="publication-open-admission",
        tasks=("T30",),
        conditions=("SPECSMITH_FULL",),
        repetitions=1,
        purpose="One frozen real-repository admission per 20B-35B open-model route.",
    ),
    "publication-open-screen": BenchmarkProfile(
        name="publication-open-screen",
        tasks=("T30",),
        conditions=("SPECSMITH_FULL",),
        repetitions=5,
        purpose="Matched n=5 screen for an open route that cleared frozen admission.",
    ),
    "publication-open-release": BenchmarkProfile(
        name="publication-open-release",
        tasks=("T30",),
        conditions=("SPECSMITH_FULL",),
        repetitions=10,
        purpose="Independent n=10 confirmation for an open route that cleared n=5.",
    ),
    "literature-v9-ablation": BenchmarkProfile(
        name="literature-v9-ablation",
        tasks=("T28", "T29", "T30"),
        conditions=("SPECSMITH_FULL",),
        repetitions=1,
        purpose=(
            "One admission cell per synthetic/fresh/upstream task for each isolated "
            "literature-backed v9 feature set."
        ),
    ),
    "literature-v9-screen": BenchmarkProfile(
        name="literature-v9-screen",
        tasks=("T28", "T29", "T30"),
        conditions=("SPECSMITH_FULL",),
        repetitions=5,
        purpose="Matched n=5 screen for a combined v9 controller that clears ablation admission.",
    ),
    "literature-v9-release": BenchmarkProfile(
        name="literature-v9-release",
        tasks=("T28", "T29", "T30"),
        conditions=("SPECSMITH_FULL",),
        repetitions=10,
        purpose="Independent n=10 confirmation for a combined v9 controller that clears n=5.",
    ),
    "literature-v9-hotspot-admission": BenchmarkProfile(
        name="literature-v9-hotspot-admission",
        tasks=("T29", "T30"),
        conditions=("SPECSMITH_FULL",),
        repetitions=1,
        purpose=(
            "Prospective admission for explicit recurring invariants and merged T30 boundaries."
        ),
    ),
    "literature-v9-hotspot-screen": BenchmarkProfile(
        name="literature-v9-hotspot-screen",
        tasks=("T29", "T30"),
        conditions=("SPECSMITH_FULL",),
        repetitions=5,
        purpose="Matched n=5 screen after the v9.2 hotspot admission clears every gate.",
    ),
}


def resolve_profile(
    name: str,
    *,
    tasks: list[str] | None,
    conditions: list[str] | None,
    repetitions: int | None,
) -> tuple[list[str] | None, list[str] | None, int]:
    """Resolve a named locked profile or the custom selection."""
    if name == "custom":
        return tasks, conditions, repetitions if repetitions is not None else 5
    profile = PROFILES[name]
    conflicts: list[str] = []
    if tasks is not None and tuple(tasks) != profile.tasks:
        conflicts.append(f"tasks must be {','.join(profile.tasks)}")
    if conditions is not None and tuple(conditions) != profile.conditions:
        conflicts.append(f"conditions must be {','.join(profile.conditions)}")
    if repetitions is not None and repetitions != profile.repetitions:
        conflicts.append(f"repetitions must be {profile.repetitions}")
    if conflicts:
        raise ValueError(f"{name} is a locked benchmark profile: {'; '.join(conflicts)}")
    return list(profile.tasks), list(profile.conditions), profile.repetitions
