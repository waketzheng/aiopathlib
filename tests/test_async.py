"""Tests for asyncio's os module."""
import json
import os
from os.path import dirname, exists, isdir, join
from pathlib import Path

import aiofiles.os
import pytest

from aiopathlib import AsyncPath


@pytest.mark.asyncio
async def test_stat_lstat_is_sth():
    """Test the stat call."""
    filename = join(dirname(__file__), "resources", "test_file1.txt")

    stat_res = await AsyncPath(filename).stat()

    assert stat_res.st_size == 10
    p = Path(filename)
    assert stat_res == p.stat()
    ln = p.with_name(p.name + ".ln")
    aln = AsyncPath(ln)
    await aln.remove(True)
    ln.symlink_to(p)
    await aln.stat() == stat_res
    lstat_res = await AsyncPath(ln).lstat()
    lstat_res != stat_res
    lstat_res.st_size < 10
    assert await aln.is_symlink()
    assert await aln.is_file()
    assert not await aln.is_dir()
    assert await aln.parent.is_dir()
    await aln.remove(True)
    assert not await aln.is_symlink()
    assert not await aln.is_file()
    assert not await aln.is_dir()
    assert not await aln.is_mount()
    assert not await aln.is_socket()
    assert await AsyncPath("/").is_mount()
    assert await AsyncPath("/dev").is_mount()
    assert not await aln.is_char_device()
    char_path = list(Path("/dev").glob("tty*"))[0]
    assert await AsyncPath(char_path).is_char_device()
    assert not await aln.is_block_device()
    block_paths = list(Path("/dev").glob("loop*"))
    if block_paths:
        block_path = block_paths[0]
    else:
        block_path = list(Path("/dev").glob("disk*"))[0]
    assert await AsyncPath(block_path).is_block_device()
    assert not await aln.is_fifo()
    ap = AsyncPath("fifo-test.foo")
    await ap.remove(True)
    # await ap.touch()
    os.mkfifo(ap)
    assert await ap.is_fifo()
    await ap.remove(True)


@pytest.mark.asyncio
async def test_touch():
    ap = AsyncPath("touch-test.foo")
    await ap.remove(True)
    await ap.touch()
    assert (await ap.stat()).st_mode in [33204, 33188]
    assert await ap.exists()
    with pytest.raises(FileExistsError):
        await ap.touch(exist_ok=False)
    await ap.remove(True)
    await ap.touch(mode=511)
    assert (await ap.stat()).st_mode != 33188
    if hasattr(ap, "_raise_closed"):
        ap._closed = True
        with pytest.raises(ValueError):
            await ap.touch()
    await ap.remove(True)


@pytest.mark.asyncio
async def test_remove():
    """Test the remove call."""
    filename = join(dirname(__file__), "resources", "test_file2.txt")
    with open(filename, "w") as f:
        f.write("Test file for remove call")

    assert exists(filename)
    await AsyncPath(filename).remove()
    assert exists(filename) is False
    with pytest.raises(FileNotFoundError):
        await AsyncPath("not_exist_file").remove()
    await AsyncPath("not_exist_file").remove(True)
    folder = AsyncPath("folder_for_test")
    try:
        os.rmdir(folder)
    except FileNotFoundError:
        ...
    await folder.mkdir()
    with pytest.raises((PermissionError, IsADirectoryError)):
        await folder.unlink()
    await folder.remove()
    assert not await folder.exists()


@pytest.mark.asyncio
async def test_mkdir_and_rmdir():
    """Test the mkdir and rmdir call."""
    directory = join(dirname(__file__), "resources", "test_dir")
    ap = AsyncPath(directory)
    if await ap.exists():
        if await ap.is_dir():
            await ap.rmdir()
        else:
            await ap.remove()
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
    size = await AsyncPath(filename).write_bytes(b"1")
    assert Path(filename).read_bytes() == b"1"
    assert size == 1
    size = await AsyncPath(filename).write_text("22")
    assert Path(filename).read_text() == "22"
    assert size == 2
    data = {"key": 3}
    size = await AsyncPath(filename).write_json(data)
    content = json.dumps(data)
    assert Path(filename).read_text() == content
    assert await AsyncPath(filename).read_json() == data
    assert size == len(content)
    await AsyncPath(filename).async_write(b"4")
    assert Path(filename).read_bytes() == b"4"
    assert await AsyncPath(filename).read_bytes() == b"4"
    assert await AsyncPath(filename).read_text() == "4"
    assert exists(filename)
    new_name = filename.replace(".txt", ".json")
    await AsyncPath(filename).rename(new_name)
    assert not exists(filename)
    assert await AsyncPath(Path(new_name)).exists()
    await AsyncPath(new_name).unlink()
    assert not exists(new_name)
