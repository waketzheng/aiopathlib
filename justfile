#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile lint`, for example.

# NOTE: You can run the following command to install `just`:
#   uv tool install rust-just

system-info:
    @echo "This is an {{arch()}} machine running on {{os_family()}}"
    just --list

# Use powershell for Windows so that 'Git Bash' and 'PyCharm Terminal' get the same result
set windows-powershell := true
VENV_CREATE := "pdm venv create --with uv --with-pip"
UV_DEPS := "uv sync --all-extras --all-groups"
UV_PIP_I := "uv pip install"
BIN_DIR := if os_family() == "windows" { "Scripts" } else { "bin" }
PY_EXEC := if os_family() == "windows" { ".venv/Scripts/python.exe" } else { ".venv/bin/python" }
SRC := "aiopathlib"

[unix]
venv *args:
    @if test ! -e .venv; then {{ VENV_CREATE }} {{ args }}; fi
[windows]
venv *args:
    @if (-Not (Test-Path '.venv')) { {{ VENV_CREATE }} {{ args }} }

venv313 *args:
    {{ VENV_CREATE }} 3.13 {{args}}

pypi *args:
    @uv run --no-sync fast pypi --quiet {{args}}

pypi_reverse *args:
    @just pypi --reverse {{args}}

uv_deps *args:
    @just pypi_reverse
    {{ UV_DEPS }} --reinstall-package={{SRC}} {{args}}
    @just pypi

[unix]
deps *args: venv
    @just uv_deps {{args}}
[windows]
deps *args: venv
    if (Test-Path '~/AppData/Roaming/uv/tools/rust-just') { echo 'uv sync ...'; just uv_deps {{ args }} } else { echo 'Using pdm ...'; pdm i -G :all --frozen {{ args }} }

uv_lock *args:
    @just pypi_reverse
    uv lock {{args}}
    @just deps --frozen

[unix]
lock *args:
    @just uv_lock {{args}}
[windows]
lock *args:
    if (-Not (Test-Path '~/AppData/Roaming/uv/tools/rust-just')) { echo 'Using pdm ...'; pdm lock -G :all {{ args }} } else { echo 'uv lock...'; just uv_lock {{ args }} }

add *args:
    @just pypi_reverse
    uv add {{args}}
    @just pypi

[unix]
up *args: venv
    @just uv_lock --upgrade {{args}}
[windows]
up *args: venv
    if (-Not (Test-Path '~/AppData/Roaming/uv/tools/rust-just')) { echo 'Using pdm ...'; pdm update -G :all {{ args }} } else { echo 'uv lock...'; just uv_lock --upgrade {{ args }} }

uv_clear *args:
    {{ UV_DEPS }} {{args}}

[unix]
clear *args:
    @just uv_clear {{args}}
[windows]
clear *args:
    @if (-Not (Test-Path 'pdm.lock')) { just uv_clear {{args}}  } else { pdm sync -G :all --clean {{args}} }

run *args: venv
    .venv/{{BIN_DIR}}/{{args}}

_lint *args:
    pdm run fast lint --bandit {{args}}
    @just mypy {{SRC}}

uvx_py *args:
    uvx --python={{PY_EXEC}} {{args}}

mypy *args:
    @just uvx_py mypy --python-executable={{PY_EXEC}} {{args}}

mypy310 *args:
    uv export --python=3.10 --no-hashes --all-extras --all-groups --no-group test --frozen -o dev_requirements.txt
    uvx --python=3.10 --with-requirements=dev_requirements.txt mypy --cache-dir=.mypy310_cache {{SRC}} {{args}}

right *args:
    @just uvx_py pyright --pythonpath={{PY_EXEC}} {{args}}

lint *args: deps
    @just _lint {{args}}

fmt *args:
    @just _lint --skip-mypy {{args}}

alias _style := fmt

style *args: deps
    @just fmt {{args}}

_check *args:
    pdm run fast check {{args}}
    @just mypy {{SRC}}

check *args: deps
    @just _check {{args}}

_build *args:
    uv build --offline {{args}}

build *args: deps
    pdm build {{args}}

_test *args:
    pdm run fast test {{args}}

test *args: deps
    @just _test {{args}}

prod *args: venv
    uv sync --no-dev {{args}}

[unix]
pipi *args: venv
    {{ UV_PIP_I }} {{args}}
[windows]
pipi *args: venv
    @if (-Not (Test-Path '.venv/Scripts/pip.exe')) { UV_PIP_I {{args}} } else { @just run pip install {{args}} }

install_me:
    @just pipi -e .

start:
    pre-commit install
    @just deps

version part="patch" *args:
    pdm run fast bump {{part}} {{args}}

bump *args:
    @just version patch --commit {{args}}

tag *args:
    pdm run fast tag {{args}}

# Bump version with patch part(0.1.1->0.1.2) and auto mark tag
release: venv bump tag
    git --no-pager log -1

# Bump version with minor part(0.1.1->0.2.0) and auto mark tag
minor *args:
    @just version minor --commit {{args}}
    git --no-pager log -1
