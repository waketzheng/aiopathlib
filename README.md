aiopathlib: Pathlib support for asyncio
=======================================

[![image](https://img.shields.io/pypi/v/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/pyversions/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/l/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/codecov/c/github/waketzheng/aiopathlib/master.svg)](https://codecov.io/github/waketzheng/aiopathlib?branch=master)
[![image](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)

**aiopathlib** is written in Python, for handling local
disk files in asyncio applications.

Base on [aiofiles](https://github.com/Tinche/aiofiles) and just like pathlib, but use await.

```py
with open('filename', 'w') as fp:
    fp.write('My file contents')

text = await aiopathlib.AsyncPath('filename').read_text()
print(text)
'My file contents'

content = await aiopathlib.AsyncPath(Path('filename')).read_bytes()
print(content)
b'My file contents'
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

# Synchronization functions
[Path(i) for i in ap.glob('*')] == list(p.glob('*'))
[Path(i) for i in ap.rglob('*')] == list(p.rglob('*'))
ap / 'filename' == ap.joinpath('filename') == AsyncPath(f'{ap}/filename')
str(AsyncPath('string-or-Path-or-AsyncPath')) == str(Path('string-or-Path-or-AsyncPath'))
ap.stem == p.stem
ap.suffix == p.suffix
Path(ap.with_name('xxx')) == p.with_name('xxx')
Path(ap.parent) == p.parent
Path(ap.resolve()) == p.resolve()
...
```


History
-------

#### 0.3.1 (2022-02-20)

- Return content size after write local file
- Upgrade dependencies

#### 0.3.0 (2021-12-16)

- Support Python3.7
- Clear `dev_requirements.txt` to be only package name and version

#### 0.2.3 (2021-10-16)

- Make `touch` pass test for py39.
- Remove support for pypy3 from docs.

#### 0.2.2 (2021-09-20)

- Make `touch`/`stat`/`is_file`/... be awaitable.
- Use `super().__new__` for initial.

#### 0.2.0 (2021-08-29)

- Make `AsyncPath` be subclass of `pathlib.Path`.
- Add github action to show test coverage.

#### 0.1.3 (2021-08-28)

- Add makefile.
- Test all functions.
- Fix rename method error.
- Support sync pathlib methods.

#### 0.1.0 (2021-06-14)

- Introduced a changelog.
- Publish at gitee.


Contributing
------------

Contributions are very welcome.
