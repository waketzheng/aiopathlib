aiopathlib: Pathlib support for asyncio
=======================================

[![image](https://img.shields.io/pypi/v/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/pyversions/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/l/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/codecov/c/github/waketzheng/aiopathlib/master.svg)](https://codecov.io/github/waketzheng/aiopathlib?branch=master)
![Mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> If you are not using aiofiles, `anyio.Path` is another choice:

```py
from datetime import datetime
from anyio import Path  # pip install anyio

filepath = Path(__file__)
another = filepath.parent / 'sub_dirpath' / 'filename.ext'

if await another.exists():
    content = await another.read_bytes()
elif not await another.parent.exists():
    await another.parent.mkdir(parents=True)
else:
    await another.write_bytes(b'1')

# glob/stat/remove
async for p in filepath.parent.glob('*'):
    if await p.is_file():
        stat = await p.stat()
        create_time = datetime.fromtimestamp(stat.st_ctime)
        update_time = datetime.fromtimestamp(stat.st_mtime)
        await p.unlink()  # remove file
        print(f'{p} created at: {create_time}, modified at: {update_time}, removed at: {datetime.now()}')
```
See more at: https://github.com/agronholm/anyio

------
**aiopathlib** is written in Python, for handling local
disk files in asyncio applications.

Base on [aiofiles](https://github.com/Tinche/aiofiles) and just like pathlib, but use await.

```py
with open('filename', 'w') as fp:
    fp.write('{"msg":"My file contents"}')

apath = aiopathlib.AsyncPath('filename')
text = await apath.read_text()
print(repr(text))
# '{"msg":"My file contents"}'

content = await apath.read_bytes()
print(content)
# b'{"msg":"My file contents"}'

data = await apath.read_json()
print(data)
# {"msg": "My file contents"}
```

Asynchronous interface to create folder.

```py
from aiopathlib import AsyncPath

apath = AsyncPath('dirname/subpath')
if not await apath.exists():
    await apath.mkdir(parents=True)
```


Features
--------

- a file API very similar to Python's standard package `pathlib`, blocking API
- support for buffered and unbuffered binary files, and buffered text files
- support for ``async``/``await`` (:PEP:`492`) constructs


Installation
------------

To install aiopathlib, simply:


```bash
$ pip install aiopathlib
```


Usage
-----
These functions are awaitable

* ``read_text``
* ``read_bytes``
* ``read_json``
* ``write_text``
* ``write_bytes``
* ``write_json``
* ``mkdir``
* ``touch``
* ``exists``
* ``rename``
* ``unlink``
* ``rmdir``
* ``remove``
* ``stat``
* ``lstat``
* ``is_file``
* ``is_dir``
* ``is_symlink``
* ``is_fifo``
* ``is_mount``
* ``is_block_device``
* ``is_char_device``
* ``is_socket``

Example
-------
Some common using cases:

```
from pashlib import Path
from aiopathlib import AsyncPath

filename = 'test.json'
ap = AsyncPath(filename)
p = Path(filename)
assert (await ap.exists()) == p.exists() == False
await ap.touch()  # Create a empty file
assert (await ap.is_file()) == p.is_file() == True
assert (await ap.is_dir()) == p.is_dir() == False
assert (await ap.is_symlink()) == p.is_symlink() == False
for func in ('is_fifo', 'is_mount', 'is_block_device', 'is_char_device', 'is_socket'):
    assert (await getattr(ap, func)()) == getattr(p, func)()
d = {'key': 'value'}
await ap.write_json(d)  # == p.write_text(json.dumps(d))
assert (await ap.read_json()) == d  # == json.loads(p.read_text())
assert (await ap.read_bytes()) == p.read_bytes()  # b'{"key": "value"}'
assert (await ap.stat()) == p.stat()
assert (await ap.lstat()) == p.lstat()
ap = await ap.rename('test_dir')  # == AsyncPath(p.rename('test_dir'))
await ap.remove()  # == await ap.unlink() == p.unlink()
await ap.mkdir()  # == p.mkdir()
await ap.resolve() # == AsyncPath(p.resolve())

# Synchronization functions
[Path(i) for i in ap.glob('*')] == list(p.glob('*'))
[Path(i) for i in ap.rglob('*')] == list(p.rglob('*'))
ap / 'filename' == ap.joinpath('filename') == AsyncPath(f'{ap}/filename')
str(AsyncPath('string-or-Path-or-AsyncPath')) == str(Path('string-or-Path-or-AsyncPath'))
ap.stem == p.stem
ap.suffix == p.suffix
Path(ap.with_name('xxx')) == p.with_name('xxx')
Path(ap.parent) == p.parent
...
```


History
-------

See the [CHANGELOG.md](https://github.com/waketzheng/aiopathlib/blob/master/CHANGELOG.md) file for details.


Contributing
------------

Contributions are very welcome.
