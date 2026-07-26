"""Deterministic inference for matched model-capability substitution runs."""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict
from typing import Any

_DEFAULT_BOOTSTRAP_SAMPLES = 10_000
_NONINFERIORITY_MARGIN = 0.05
_WILSON_Z_95 = 1.959963984540054


def _quantile(values: list[float], probability: float) -> float:
    if not values:
        return float("inf")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    fraction = position - low
    return ordered[low] + (ordered[high] - ordered[low]) * fraction


def _system_metrics(cells: list[dict[str, Any]]) -> dict[str, float]:
    runs = len(cells)
    passes = sum(1 for cell in cells if bool(cell["passed"]))
    tokens = sum(float(cell["tokens"]) for cell in cells)
    cost = sum(float(cell["cost_usd"]) for cell in cells)
    pass_rate = passes / runs if runs else 0.0
    return {
        "runs": float(runs),
        "passes": float(passes),
        "pass_rate": pass_rate,
        "tokens_per_correct_answer": tokens / passes if passes else float("inf"),
        "cost_of_pass": cost / passes if passes else float("inf"),
    }


def _wilson_interval(successes: int, trials: int) -> tuple[float, float]:
    if trials <= 0:
        return (0.0, 0.0)
    probability = successes / trials
    z_squared = _WILSON_Z_95**2
    denominator = 1.0 + z_squared / trials
    center = (probability + z_squared / (2.0 * trials)) / denominator
    margin = (
        _WILSON_Z_95
        * math.sqrt((probability * (1.0 - probability) + z_squared / (4.0 * trials)) / trials)
        / denominator
    )
    return (max(0.0, center - margin), min(1.0, center + margin))


def _paired_cells(
    smaller_rows: list[dict[str, Any]],
    stronger_rows: list[dict[str, Any]],
    tasks: list[str],
) -> dict[str, list[tuple[dict[str, Any], dict[str, Any]]]]:
    smaller = {
        (str(row["task"]), int(row["rep"])): row
        for row in smaller_rows
        if row["condition"] == "SPECSMITH_FULL" and row["task"] in tasks
    }
    stronger = {
        (str(row["task"]), int(row["rep"])): row
        for row in stronger_rows
        if row["condition"] == "UNGOVERNED" and row["task"] in tasks
    }
    if smaller.keys() != stronger.keys():
        missing = sorted(stronger.keys() - smaller.keys())
        extra = sorted(smaller.keys() - stronger.keys())
        raise ValueError(
            "substitution headline cells are not paired; "
            f"missing_smaller={missing[:10]}, missing_stronger={extra[:10]}"
        )

    pairs: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for key in sorted(smaller):
        pairs[key[0]].append((smaller[key], stronger[key]))
    missing_tasks = sorted(set(tasks) - pairs.keys())
    if missing_tasks:
        raise ValueError(f"substitution comparison is missing tasks {missing_tasks}")
    return dict(pairs)


def _effect(
    smaller_cells: list[dict[str, Any]],
    stronger_cells: list[dict[str, Any]],
) -> dict[str, float]:
    smaller = _system_metrics(smaller_cells)
    stronger = _system_metrics(stronger_cells)
    smaller_pass_ci = _wilson_interval(int(smaller["passes"]), int(smaller["runs"]))
    stronger_pass_ci = _wilson_interval(int(stronger["passes"]), int(stronger["runs"]))
    stronger_tpca = stronger["tokens_per_correct_answer"]
    stronger_cop = stronger["cost_of_pass"]
    return {
        "pass_rate_difference": smaller["pass_rate"] - stronger["pass_rate"],
        "pass_rate_difference_low": smaller_pass_ci[0] - stronger_pass_ci[1],
        "pass_rate_difference_high": smaller_pass_ci[1] - stronger_pass_ci[0],
        "tpca_ratio": (
            smaller["tokens_per_correct_answer"] / stronger_tpca
            if stronger_tpca > 0
            else float("inf")
        ),
        "cost_of_pass_ratio": (
            smaller["cost_of_pass"] / stronger_cop if stronger_cop > 0 else float("inf")
        ),
    }


def _bootstrap_effects(
    pairs_by_task: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]],
    *,
    samples: int,
    resample_tasks: bool,
    seed: str,
) -> list[dict[str, float]]:
    rng = random.Random(seed)
    task_ids = sorted(pairs_by_task)
    effects: list[dict[str, float]] = []
    for _ in range(samples):
        sampled_tasks = (
            [task_ids[rng.randrange(len(task_ids))] for _ in task_ids]
            if resample_tasks
            else task_ids
        )
        smaller_cells: list[dict[str, Any]] = []
        stronger_cells: list[dict[str, Any]] = []
        for task_id in sampled_tasks:
            pairs = pairs_by_task[task_id]
            for _rep in pairs:
                smaller, stronger = pairs[rng.randrange(len(pairs))]
                smaller_cells.append(smaller)
                stronger_cells.append(stronger)
        effects.append(_effect(smaller_cells, stronger_cells))
    return effects


def _intervals(effects: list[dict[str, float]]) -> dict[str, list[float]]:
    return {
        "pass_rate_difference": [
            _quantile([row["pass_rate_difference_low"] for row in effects], 0.025),
            _quantile([row["pass_rate_difference_high"] for row in effects], 0.975),
        ],
        "tpca_ratio": [
            _quantile([row["tpca_ratio"] for row in effects], 0.025),
            _quantile([row["tpca_ratio"] for row in effects], 0.975),
        ],
        "cost_of_pass_ratio": [
            _quantile([row["cost_of_pass_ratio"] for row in effects], 0.025),
            _quantile([row["cost_of_pass_ratio"] for row in effects], 0.975),
        ],
    }


def substitution_inference(
    smaller_rows: list[dict[str, Any]],
    stronger_rows: list[dict[str, Any]],
    tasks: list[str],
    *,
    bootstrap_samples: int = _DEFAULT_BOOTSTRAP_SAMPLES,
    noninferiority_margin: float = _NONINFERIORITY_MARGIN,
) -> dict[str, Any]:
    """Return point estimates, paired bootstrap intervals, and guarded claims.

    ``fixed_suite`` resamples repetitions within each fixed benchmark task.
    ``task_cluster`` also resamples task IDs and is the more conservative view
    when reasoning beyond the exact versioned task grid.
    """
    pairs_by_task = _paired_cells(smaller_rows, stronger_rows, tasks)
    smaller_cells = [pair[0] for pairs in pairs_by_task.values() for pair in pairs]
    stronger_cells = [pair[1] for pairs in pairs_by_task.values() for pair in pairs]
    point = _effect(smaller_cells, stronger_cells)
    seed_basis = "|".join(
        f"{task}:{pair[0]['rep']}:{pair[0]['model']}:{pair[1]['model']}"
        for task, pairs in sorted(pairs_by_task.items())
        for pair in pairs
    )
    seed = hashlib.sha256(seed_basis.encode("utf-8")).hexdigest()
    fixed = _intervals(
        _bootstrap_effects(
            pairs_by_task,
            samples=bootstrap_samples,
            resample_tasks=False,
            seed=f"{seed}:fixed",
        )
    )
    clustered = _intervals(
        _bootstrap_effects(
            pairs_by_task,
            samples=bootstrap_samples,
            resample_tasks=True,
            seed=f"{seed}:tasks",
        )
    )
    minimum_reps = min(len(pairs) for pairs in pairs_by_task.values())
    release_ready = minimum_reps >= 10
    fixed_noninferior = fixed["pass_rate_difference"][0] >= -noninferiority_margin
    fixed_token_superior = fixed["tpca_ratio"][1] < 1.0
    clustered_noninferior = clustered["pass_rate_difference"][0] >= -noninferiority_margin
    clustered_token_superior = clustered["tpca_ratio"][1] < 1.0
    return {
        "schema": "governancebench-substitution-v1",
        "tasks": list(tasks),
        "minimum_repetitions_per_task": minimum_reps,
        "bootstrap_samples": bootstrap_samples,
        "noninferiority_margin": noninferiority_margin,
        "point": point,
        "fixed_suite_95_ci": fixed,
        "task_cluster_95_ci": clustered,
        "claims": {
            "release_ready": release_ready,
            "fixed_suite_substitution": (
                release_ready and fixed_noninferior and fixed_token_superior
            ),
            "cross_task_substitution": (
                release_ready and clustered_noninferior and clustered_token_superior
            ),
        },
    }
