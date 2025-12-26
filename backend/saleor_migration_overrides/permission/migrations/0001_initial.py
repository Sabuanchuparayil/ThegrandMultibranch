"""Proxy to upstream Saleor permission migration 0001.

We keep upstream operations intact and only patch later migrations when needed.

NOTE: Python cannot import modules like `...migrations.0001_initial` using normal
`from x.y.0001_initial import ...` syntax because `0001_initial` is not a valid
identifier. Use `importlib.import_module` instead.
"""

import importlib


Migration = importlib.import_module("saleor.permission.migrations.0001_initial").Migration  # type: ignore[attr-defined]


