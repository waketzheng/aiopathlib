#!/usr/bin/env python
"""
Make style by `ruff` and verify type hints by `mypy`,
then run `bandit -r <package>` to find security issue.


Usage::
    ./scripts/lint.py

"""

import os
import sys
from enum import IntEnum


class Tools(IntEnum):
    poetry = 0
    pdm = 1
    uv = 2
    none = 3


CMD = "ruff format && ruff check --fix"
_tool = Tools.uv
BANDIT = True
TOOL = getattr(_tool, "name", str(_tool))
PREFIX = (TOOL + " run ") if TOOL and Tools.none.name != TOOL else ""
parent = os.path.abspath(os.path.dirname(__file__))
work_dir = os.path.dirname(parent)
if os.getcwd() != work_dir:
    os.chdir(work_dir)


def run_and_echo(cmd, prefix=PREFIX, verbose=True):
    # type: (str, str, bool) -> int
    cmd = prefix + cmd
    if verbose:
        print("--> " + cmd)
    return os.system(cmd)


if run_and_echo(CMD) != 0:
    sys.exit(1)
if run_and_echo("mypy .") != 0:
    sys.exit(1)
if BANDIT:
    package_name = os.path.basename(work_dir).replace("-", "_")
    if run_and_echo(f"bandit -r {package_name}") != 0:
        sys.exit(1)
print("Done. ✨ 🍰 ✨")
