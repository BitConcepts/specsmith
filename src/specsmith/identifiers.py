# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Layer1Labs Silicon, Inc. All rights reserved.
"""Canonical grammar for Specsmith requirement and test identifiers."""

from __future__ import annotations

# Namespace segments are intentionally strict: they begin with an ASCII letter
# and may then contain ASCII letters, digits, or underscores. Repeating the
# segment group supports IDs such as REQ-EG-MEM-003 without weakening the
# terminal numeric identity or accepting empty segments.
IDENTIFIER_NAMESPACE_SEGMENT = r"[A-Z][A-Z0-9_]*"
REQ_ID_PATTERN = rf"REQ-(?:{IDENTIFIER_NAMESPACE_SEGMENT}-)*\d+"
TEST_ID_PATTERN = rf"TEST-(?:{IDENTIFIER_NAMESPACE_SEGMENT}-)*\d+[A-Za-z]*"
