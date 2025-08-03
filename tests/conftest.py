import sys
from pathlib import Path
from typing import Generator

import pytest

if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    import os
    from contextlib import AbstractContextManager

    class chdir(AbstractContextManager):  # Copied from source code of Python3.13
        """Non thread-safe context manager to change the current working directory."""

        def __init__(self, path):
            self.path = path
            self._old_cwd = []

        def __enter__(self):
            self._old_cwd.append(os.getcwd())
            os.chdir(self.path)

        def __exit__(self, *excinfo):
            os.chdir(self._old_cwd.pop())


@pytest.fixture
def tmp_work_dir(tmp_path: Path) -> Generator[Path]:
    with chdir(tmp_path):
        yield tmp_path
