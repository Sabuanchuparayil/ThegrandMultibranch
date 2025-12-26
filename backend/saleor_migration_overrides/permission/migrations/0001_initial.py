"""Proxy to upstream Saleor permission migration 0001.

We keep upstream operations intact and only patch later migrations when needed.
"""

from saleor.permission.migrations.0001_initial import Migration  # noqa: F401


