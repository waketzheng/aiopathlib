"""Tests for asyncio's os module."""
from pathlib import Path

from aiopathlib import AsyncPath


def test_parent_joinpath():
    """Test the parent and joinpath call."""
    filepath = Path(__file__).parent.joinpath("resources", "test_file2.txt")
    async_path = AsyncPath(__file__).parent.joinpath("resources", "test_file2.txt")
    assert str(filepath) == str(async_path)


def test_cwd_home():
    """Test the cmd and home call."""
    assert str(AsyncPath.home()) == str(Path.home())
    assert str(AsyncPath.cwd()) == str(Path.cwd())


def test_div():
    """Test the div magic call."""
    assert AsyncPath("a") / "b" == AsyncPath("a/b")
    assert "a" / AsyncPath("b") == AsyncPath("a/b")
