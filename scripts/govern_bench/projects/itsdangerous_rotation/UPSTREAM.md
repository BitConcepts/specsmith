# Upstream snapshot provenance

- Repository: https://github.com/pallets/itsdangerous
- Commit: `672971d66a2ef9f85151e53283113f33d642dabd`
- Commit date: 2025-06-14T20:35:42Z
- License: BSD-3-Clause (`LICENSE.txt`)
- Snapshot scope: `src/`, `tests/`, `docs/serializer.rst`, `pyproject.toml`,
  `README.md`, and `LICENSE.txt`
- Imported: 2026-07-30

The benchmark task and `tools/validate_rotation_api.py` are Specsmith
evaluation additions. All upstream files begin byte-for-byte identical to the
pinned commit. The benchmark model may edit only the files declared by T30;
the evaluator verifies that this provenance file and the upstream license are
unchanged.
