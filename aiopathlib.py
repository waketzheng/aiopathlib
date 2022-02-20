from __future__ import annotations

import json
import os
from pathlib import Path, PosixPath, PurePath, WindowsPath, _ignore_error  # type:ignore
from stat import S_ISBLK, S_ISCHR, S_ISDIR, S_ISFIFO, S_ISLNK, S_ISREG, S_ISSOCK
from typing import Generator, Optional, Union

import aiofiles
import aiofiles.os

JSONType = Union[list, dict, int, str, float, bool, None]


class AsyncPath(Path):
    def __new__(cls, *args, **kwargs):
        path = super().__new__(Path, *args, **kwargs)
        if cls is AsyncPath:
            cls = AsyncWindowsPath if os.name == "nt" else AsyncPosixPath
        return cls._from_parts([path])

    async def mkdir(
        self, mode: int = 511, parents: bool = False, exist_ok: bool = False
    ) -> None:
        try:
            await aiofiles.os.mkdir(self, mode)
        except FileExistsError:
            if exist_ok and not await self.is_file():
                return
            raise
        except FileNotFoundError:
            if not parents:
                raise
            for p in list(self.parents)[::-1]:
                if not await p.exists():
                    await aiofiles.os.mkdir(p, mode)
            await aiofiles.os.mkdir(self, mode)

    async def exists(self) -> bool:
        try:
            return bool(await aiofiles.os.stat(self))
        except FileNotFoundError:
            return False

    async def write_bytes(self, content: bytes, *, loop=None, executor=None) -> int:
        return await self.async_write(content, "wb", loop=loop, executor=executor)

    async def write_text(
        self,
        text: str,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        *,
        loop=None,
        executor=None,
    ) -> int:
        return await self.async_write(
            text, "w", encoding=encoding, errors=errors, loop=loop, executor=executor
        )

    async def write_json(
        self,
        context: JSONType,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        *,
        loop=None,
        executor=None,
        **json_dump_kwargs,
    ) -> int:
        return await self.async_write(
            json.dumps(context, **json_dump_kwargs),
            "w",
            encoding=encoding,
            errors=errors,
            loop=loop,
            executor=executor,
        )

    async def async_write(
        self,
        ctx: Union[bytes, str],
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        *,
        loop=None,
        executor=None,
    ) -> int:
        if mode is None:
            mode = "wb" if isinstance(ctx, bytes) else "w"
        async with aiofiles.open(
            self, mode, encoding=encoding, errors=errors, loop=loop, executor=executor
        ) as fp:  # type:ignore
            return await fp.write(ctx)

    async def read_text(
        self,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        *,
        loop=None,
        executor=None,
    ) -> str:
        async with aiofiles.open(
            self, encoding=encoding, errors=errors, loop=loop, executor=executor
        ) as fp:
            return await fp.read()

    async def read_bytes(self, *, loop=None, executor=None) -> bytes:
        async with aiofiles.open(self, mode="rb", loop=loop, executor=executor) as fp:
            return await fp.read()

    async def read_json(
        self,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        *,
        loop=None,
        executor=None,
        **kw,
    ) -> JSONType:
        return json.loads(await self.read_text(encoding, errors), **kw)

    async def remove(self, missing_ok: bool = False) -> None:
        if await self.is_dir():
            return await self.rmdir()
        return await self.unlink(missing_ok)

    async def rmdir(self) -> None:
        return await aiofiles.os.rmdir(self)

    async def unlink(self, missing_ok: bool = False) -> None:
        try:
            return await aiofiles.os.remove(self)
        except FileNotFoundError:
            if not missing_ok:
                raise

    async def rename(self, target: Union[str, PurePath]) -> AsyncPath:
        await aiofiles.os.rename(self, target)
        return self.__class__(target)

    async def stat(self) -> os.stat_result:
        return await aiofiles.os.stat(self)

    async def lstat(self) -> os.stat_result:
        return await aiofiles.os.stat(self, follow_symlinks=False)

    async def _is_sth(self, func, symlink: bool = False) -> bool:
        try:
            if symlink:
                st = await self.lstat()
            else:
                st = await self.stat()
            return func(st.st_mode)
        except OSError as e:
            if not _ignore_error(e):
                raise
            # Path doesn't exist
            # or is a broken symlink (if params `symlink` set to False)
            # (see https://bitbucket.org/pitrou/pathlib/issue/12/)
            return False
        except ValueError:
            # Non-encodable path
            return False

    async def is_dir(self) -> bool:
        """
        Whether this path is a directory.
        """
        return await self._is_sth(S_ISDIR)

    async def is_file(self) -> bool:
        """
        Whether this path is a regular file (also True for symlinks pointing
        to regular files).
        """
        return await self._is_sth(S_ISREG)

    async def is_mount(self) -> bool:
        """
        Check if this path is a POSIX mount point
        """
        # Need to exist and be a dir
        if not await self.exists() or not await self.is_dir():
            return False

        try:
            pst = await self.parent.stat()
            parent_dev = pst.st_dev
        except OSError:
            return False
        st = await self.stat()
        dev = st.st_dev
        if dev != parent_dev:
            return True
        ino = st.st_ino
        parent_ino = pst.st_ino
        return ino == parent_ino

    async def is_symlink(self) -> bool:
        """
        Whether this path is a symbolic link.
        """
        return await self._is_sth(S_ISLNK, True)

    async def is_block_device(self) -> bool:
        """
        Whether this path is a block device.
        """
        return await self._is_sth(S_ISBLK)

    async def is_char_device(self) -> bool:
        """
        Whether this path is a character device.
        """
        return await self._is_sth(S_ISCHR)

    async def is_fifo(self) -> bool:
        """
        Whether this path is a FIFO.
        """
        return await self._is_sth(S_ISFIFO)

    async def is_socket(self) -> bool:
        """
        Whether this path is a socket.
        """
        return await self._is_sth(S_ISSOCK)

    async def touch(self, mode=0o666, exist_ok=True):
        """
        Create this file with the given access mode, if it doesn't exist.
        """
        if getattr(self, "_closed", False) and hasattr(self, "_raise_closed"):
            self._raise_closed()
        if await self.exists() and not exist_ok:
            raise FileExistsError
        if mode == 0o666:
            async with aiofiles.open(self, "wb") as af:
                af.write(b"")
        else:
            return Path(self).touch(mode, exist_ok)

    def glob(self, pattern: str) -> Generator[Path, None, None]:
        return Path(self).glob(pattern)

    def rglob(self, pattern: str) -> Generator[Path, None, None]:
        return Path(self).rglob(pattern)


class AsyncPosixPath(AsyncPath, PosixPath):
    """AsyncPath subclass for non-Windows systems.

    On a POSIX system, instantiating a AsyncPath should return this object.
    """


class AsyncWindowsPath(AsyncPath, WindowsPath):
    """AsyncPath subclass for Windows systems.

    On a Windows system, instantiating a AsyncPath should return this object.
    """
