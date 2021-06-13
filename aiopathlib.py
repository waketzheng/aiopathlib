from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Union

import aiofiles
import aiofiles.os


class AsyncPath:
    def __init__(self, fname: Union[str, Path]):
        self._fname = fname

    async def mkdir(
        self, mode: int = 511, parents: bool = False, exist_ok: bool = False
    ) -> None:
        try:
            await aiofiles.os.mkdir(self._fname, mode)
        except FileExistsError:
            if exist_ok and not Path(self._fname).is_file():
                return
            raise
        except FileNotFoundError:
            if not parents:
                raise
            if isinstance(fpath := self._fname, str):
                fpath = Path(fpath)
            for p in list(fpath.parents)[::-1]:
                if not p.exists():
                    await aiofiles.os.mkdir(p, mode)
            await aiofiles.os.mkdir(self._fname, mode)

    async def exists(self) -> bool:
        try:
            return bool(await aiofiles.os.stat(self._fname))
        except FileNotFoundError:
            return False

    async def write_bytes(self, content: bytes) -> None:
        await self.async_write(content, "wb")

    async def write_text(self, text: str) -> None:
        await self.async_write(text, "w")

    async def write_json(self, context: Union[list, dict, int, str, float]) -> None:
        await self.async_write(json.dumps(context), "w")

    async def async_write(self, ctx: Union[bytes, str], mode: Optional[str] = None):
        if mode is None:
            mode = "wb" if isinstance(ctx, bytes) else "w"
        async with aiofiles.open(self._fname, mode) as fp:  # type:ignore
            await fp.write(ctx)

    async def read_text(self, encoding=None, errors=None) -> str:
        async with aiofiles.open(self._fname, encoding=encoding, errors=errors) as fp:
            return await fp.read()

    async def read_bytes(self) -> bytes:
        async with aiofiles.open(self._fname, mode="rb") as fp:
            return await fp.read()

    async def read_json(self, encoding=None, errors=None) -> Union[dict, list]:
        return json.loads(await self.read_text(encoding, errors))

    async def remove(self) -> None:
        return await aiofiles.os.remove(self._fname)

    async def rename(self, target: str) -> AsyncPath:
        await aiofiles.os.rename(self._fname, target)
        return self.__class__(Path(self._fname).with_name(target))
