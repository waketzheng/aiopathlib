from __future__ import annotations

import json
import os
from pathlib import Path, PosixPath, PurePath, WindowsPath
from typing import Optional, Union

import aiofiles
import aiofiles.os

JSONType = Union[list, dict, int, str, float, bool, None]


class AsyncPath(Path):
    def __new__(cls, *args, **kwargs):
        if cls is AsyncPath:
            cls = AsyncWindowsPath if os.name == "nt" else AsyncPosixPath
        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError(
                "cannot instantiate %r on your system" % (cls.__name__,)
            )
        self._init()
        return self

    async def mkdir(  # type: ignore[override]
        self, mode: int = 511, parents: bool = False, exist_ok: bool = False
    ) -> None:
        try:
            await aiofiles.os.mkdir(self, mode)
        except FileExistsError:
            if exist_ok and not self.is_file():
                return
            raise
        except FileNotFoundError:
            if not parents:
                raise
            for p in list(self.parents)[::-1]:
                if not await p.exists():
                    await aiofiles.os.mkdir(p, mode)
            await aiofiles.os.mkdir(self, mode)

    async def exists(self) -> bool:  # type: ignore[override]
        try:
            return bool(await aiofiles.os.stat(self))
        except FileNotFoundError:
            return False

    async def write_bytes(self, content: bytes) -> None:  # type: ignore[override]
        await self.async_write(content, "wb")

    async def write_text(  # type: ignore[override]
        self,
        text: str,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> None:
        await self.async_write(text, "w", encoding=encoding, errors=errors)

    async def write_json(
        self,
        context: JSONType,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **kw,
    ) -> None:
        await self.async_write(
            json.dumps(context, **kw), "w", encoding=encoding, errors=errors
        )

    async def async_write(
        self,
        ctx: Union[bytes, str],
        mode: Optional[str] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ):
        if mode is None:
            mode = "wb" if isinstance(ctx, bytes) else "w"
        async with aiofiles.open(
            self, mode, encoding=encoding, errors=errors
        ) as fp:  # type:ignore
            await fp.write(ctx)

    async def read_text(  # type: ignore[override]
        self,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> str:
        async with aiofiles.open(self, encoding=encoding, errors=errors) as fp:
            return await fp.read()

    async def read_bytes(self) -> bytes:  # type: ignore[override]
        async with aiofiles.open(self, mode="rb") as fp:
            return await fp.read()

    async def read_json(
        self, encoding: Optional[str] = None, errors: Optional[str] = None, **kw
    ) -> JSONType:
        return json.loads(await self.read_text(encoding, errors), **kw)

    async def remove(self, missing_ok: bool = False) -> None:
        try:
            return await aiofiles.os.remove(self)
        except FileNotFoundError:
            if not missing_ok:
                raise

    async def rmdir(self) -> None:  # type: ignore[override]
        return await aiofiles.os.rmdir(self)

    async def unlink(self, missing_ok: bool = False) -> None:  # type: ignore[override]
        return await self.remove()

    async def rename(  # type: ignore[override]
        self, target: Union[str, PurePath]
    ) -> AsyncPath:
        await aiofiles.os.rename(self, target)
        return self.__class__(target)


class AsyncPosixPath(AsyncPath, PosixPath):
    """AsyncPath subclass for non-Windows systems.

    On a POSIX system, instantiating a AsyncPath should return this object.
    """

    __slots__ = ()


class AsyncWindowsPath(AsyncPath, WindowsPath):
    """AsyncPath subclass for Windows systems.

    On a Windows system, instantiating a AsyncPath should return this object.
    """
