"""Load Python's real stdlib 'types' module to avoid shadowing it.

This file is named types.py and lives in the glass package directory.
It must not break any stdlib code that does ``import types``.
All glass application code uses node_types.py instead.
"""
import sys as _sys
import os as _os

_this = _os.path.normcase(_os.path.abspath(__file__))

for _p in _sys.path:
    if not _p:
        continue
    _candidate = _os.path.normcase(_os.path.abspath(_os.path.join(_p, "types.py")))
    if _candidate != _this and _os.path.isfile(_candidate):
        with open(_candidate, "rb") as _fh:
            _code = _fh.read()
        exec(compile(_code, _candidate, "exec"), globals())
        break

del _sys, _os, _this, _p, _candidate, _fh, _code


