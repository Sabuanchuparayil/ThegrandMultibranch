"""Patch upstream Saleor permission migration 0002 dependency graph.

Runtime error observed:
  Migration permission.0002_alter_permission_content_type dependencies reference
  nonexistent parent node ('auth', '0013_auto_20221214_1224')

This blocks *all* migrations. The exact auth migration name varies by Django version,
so we depend on stable `auth.0001_initial` instead, which is sufficient to ensure
the auth tables exist.
"""

from django.db import migrations


def _load_upstream():
    try:
        from saleor.permission.migrations.0002_alter_permission_content_type import (  # noqa: WPS433
            Migration as UpstreamMigration,
        )
        return UpstreamMigration
    except Exception:
        return None


_Upstream = _load_upstream()
_upstream_ops = getattr(_Upstream, "operations", []) if _Upstream else []
_upstream_deps = list(getattr(_Upstream, "dependencies", [])) if _Upstream else []

_fixed_deps = []
for _dep in _upstream_deps:
    if _dep == ("auth", "0013_auto_20221214_1224"):
        _fixed_deps.append(("auth", "0001_initial"))
    else:
        _fixed_deps.append(_dep)

# Ensure dependency on our own initial migration always exists.
if ("permission", "0001_initial") not in _fixed_deps:
    _fixed_deps.insert(0, ("permission", "0001_initial"))

# If upstream deps couldn't be loaded for some reason, provide minimal safe deps.
if not _upstream_deps:
    _fixed_deps = [
        ("permission", "0001_initial"),
        ("auth", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]


class Migration(migrations.Migration):
    dependencies = _fixed_deps
    operations = _upstream_ops


