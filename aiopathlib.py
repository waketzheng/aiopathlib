from __future__ import annotations

import json
import os
from os import PathLike
from pathlib import Path
from typing import Optional, Union

import aiofiles
import aiofiles.os

JSONType = Union[list, dict, int, str, float, bool, None]


class AsyncPath:
    def __init__(self, *args, **kwargs):
        self._path = Path(*args, **kwargs)

    async def mkdir(
        self, mode: int = 511, parents: bool = False, exist_ok: bool = False
    ) -> None:
        try:
            await aiofiles.os.mkdir(self._path, mode)
        except FileExistsError:
            if exist_ok and not self._path.is_file():
                return
            raise
        except FileNotFoundError:
            if not parents:
                raise
            for p in list(self._path.parents)[::-1]:
                if not p.exists():
                    await aiofiles.os.mkdir(p, mode)
            await aiofiles.os.mkdir(self._path, mode)

    async def exists(self) -> bool:
        try:
            return bool(await aiofiles.os.stat(self._path))
        except FileNotFoundError:
            return False

    async def write_bytes(self, content: bytes) -> None:
        await self.async_write(content, "wb")

    async def write_text(
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
            self._path, mode, encoding=encoding, errors=errors
        ) as fp:  # type:ignore
            await fp.write(ctx)

    async def read_text(
        self,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> str:
        async with aiofiles.open(self._path, encoding=encoding, errors=errors) as fp:
            return await fp.read()

    async def read_bytes(self) -> bytes:
        async with aiofiles.open(self._path, mode="rb") as fp:
            return await fp.read()

    async def read_json(
        self, encoding: Optional[str] = None, errors: Optional[str] = None, **kw
    ) -> JSONType:
        return json.loads(await self.read_text(encoding, errors), **kw)

    async def remove(self) -> None:
        return await aiofiles.os.remove(self._path)

    async def rmdir(self) -> None:
        return await aiofiles.os.rmdir(self._path)

    async def unlink(self) -> None:
        return await self.remove()

    async def rename(self, target: str) -> AsyncPath:
        await aiofiles.os.rename(self._path, target)
        return self.__class__(target)

    # Sync functions
    def joinpath(self, *args: Union[str, PathLike]) -> AsyncPath:
        return self.__class__(self._path.joinpath(*args))

    @classmethod
    def cwd(cls) -> AsyncPath:
        """Return a new path pointing to the current working directory
        (as returned by os.getcwd()).
        """
        return cls(os.getcwd())

    @classmethod
    def home(cls) -> AsyncPath:
        """Return a new path pointing to the user's home directory (as
        returned by os.path.expanduser('~')).
        """
        return cls(Path()._flavour.gethomedir(None))  # type:ignore

    @property
    def parent(self) -> AsyncPath:
        return self.__class__(self._path.parent)

    def __truediv__(self, key):
        return self.__class__(self._path.__truediv__(key))

    def __rtruediv__(self, key):
        return self.__class__(self._path.__rtruediv__(key))

    def __eq__(self, other):
        return self._path == other._path
