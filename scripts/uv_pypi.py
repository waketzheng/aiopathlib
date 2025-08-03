#!/usr/bin/env python
"""Auto change registry of uv.lock to be pypi.org

Usage::
    python3 <me>.py
"""

from __future__ import annotations

import functools
import re
import sys
from pathlib import Path

PYPI = "https://pypi.org/simple"
HOST = "https://files.pythonhosted.org"


def main() -> int | None:
    verbose = "--verbose" in sys.argv
    p = Path("uv.lock")
    if not p.exists():
        p = Path("..", p.name)
        if not p.exists():
            if verbose:
                print(f"{p.name} not found, skip.")
            return None
    text = p.read_text("utf-8")
    registry_pattern = r'(registry = ")(.*?)"'
    replace_registry = functools.partial(re.sub, registry_pattern, rf'\1{PYPI}"')
    registry_urls = {i[1] for i in re.findall(registry_pattern, text)}
    download_pattern = r'(url = ")(https?://.*?)(/packages/.*?\.)(gz|whl)"'
    replace_host = functools.partial(re.sub, download_pattern, rf'\1{HOST}\3\4"')
    download_hosts = {i[1] for i in re.findall(download_pattern, text)}
    if not registry_urls:
        raise ValueError(f"Failed to find pattern {registry_pattern!r} in {p}")
    if len(registry_urls) == 1:
        current_registry = registry_urls.pop()
        if current_registry == PYPI:
            if download_hosts == {HOST}:
                if verbose:
                    print(f"Registry of {p} is {PYPI}, no need to change.")
                return 0
        else:
            text = replace_registry(text)
            if verbose:
                print(current_registry, "-->", PYPI)
    else:
        # TODO: ask each one to confirm replace
        text = replace_registry(text)
        if verbose:
            for current_registry in sorted(registry_urls):
                print(current_registry, "-->", PYPI)
    if len(download_hosts) == 1:
        current_host = download_hosts.pop()
        if current_host != HOST:
            text = replace_host(text)
            if verbose:
                print(current_host, "-->", HOST)
    elif download_hosts:
        # TODO: ask each one to confirm replace
        text = replace_host(text)
        if verbose:
            for current_host in sorted(download_hosts):
                print(current_host, "-->", HOST)
    size = p.write_text(text, encoding="utf-8")
    if verbose:
        print(f"Updated {p} with {size} bytes.")
    if "--quiet" in sys.argv:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
