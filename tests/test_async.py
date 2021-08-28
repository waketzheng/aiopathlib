"""Tests for asyncio's os module."""
import json
from os.path import dirname, exists, isdir, join
from pathlib import Path

import aiofiles.os
import pytest

from aiopathlib import AsyncPath

# @pytest.mark.asyncio
# async def test_stat():
#     """Test the stat call."""
#     filename = join(dirname(__file__), "resources", "test_file1.txt")
#
#     stat_res = await aiofiles.os.stat(filename)
#
#     assert stat_res.st_size == 10


@pytest.mark.asyncio
async def test_remove():
    """Test the remove call."""
    filename = join(dirname(__file__), "resources", "test_file2.txt")
    with open(filename, "w") as f:
        f.write("Test file for remove call")

    assert exists(filename)
    await AsyncPath(filename).remove()
    assert exists(filename) is False


@pytest.mark.asyncio
async def test_mkdir_and_rmdir():
    """Test the mkdir and rmdir call."""
    directory = join(dirname(__file__), "resources", "test_dir")
    await AsyncPath(directory).mkdir()
    assert isdir(directory)
    with pytest.raises(FileExistsError):
        await AsyncPath(directory).mkdir()
    assert (await AsyncPath(directory).mkdir(exist_ok=True)) is None
    await AsyncPath(directory).rmdir()
    assert exists(directory) is False

    sub_dir = join(directory, "sub_dir")
    with pytest.raises(FileNotFoundError):
        await AsyncPath(sub_dir).mkdir()
    await AsyncPath(sub_dir).mkdir(parents=True)
    assert isdir(sub_dir)
    await AsyncPath(sub_dir).rmdir()
    await AsyncPath(directory).rmdir()
    assert exists(sub_dir) is False


@pytest.mark.asyncio
async def test_exists():
    """Test the exists call."""
    assert await AsyncPath(__file__).exists()
    not_exist_file = join(dirname(__file__), "not_exist")
    assert not await AsyncPath(not_exist_file).exists()


@pytest.mark.asyncio
async def test_rename():
    """Test the rename call."""
    old_filename = join(dirname(__file__), "resources", "test_file1.txt")
    new_filename = join(dirname(__file__), "resources", "test_file2.txt")
    await aiofiles.os.rename(old_filename, new_filename)
    assert exists(old_filename) is False and exists(new_filename)
    await aiofiles.os.rename(new_filename, old_filename)
    assert exists(old_filename) and exists(new_filename) is False


@pytest.mark.asyncio
async def test_write():
    """Test the write call."""
    filename = join(dirname(__file__), "resources", "test_write.txt")
    await AsyncPath(filename).write_bytes(b"1")
    assert Path(filename).read_bytes() == b"1"
    await AsyncPath(filename).write_text("2")
    assert Path(filename).read_text() == "2"
    await AsyncPath(filename).write_json({"key": 3})
    assert Path(filename).read_text() == json.dumps({"key": 3})
    assert await AsyncPath(filename).read_json() == {"key": 3}
    await AsyncPath(filename).async_write(b"4")
    assert Path(filename).read_bytes() == b"4"
    assert await AsyncPath(filename).read_bytes() == b"4"
    assert await AsyncPath(filename).read_text() == "4"
    assert exists(filename)
    new_name = filename.replace(".txt", ".json")
    await AsyncPath(filename).rename(new_name)
    assert not exists(filename)
    assert exists(new_name)
    await AsyncPath(new_name).unlink()
    assert not exists(new_name)
