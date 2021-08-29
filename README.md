aiopathlib: Pathlib support for asyncio
=======================================

[![image](https://img.shields.io/pypi/v/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/pyversions/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/pypi/l/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)
[![image](https://img.shields.io/codecov/c/github/waketzheng/aiopathlib/master.svg)](https://codecov.io/github/waketzheng/aiopathlib?branch=master)
[![image](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)

**aiopathlib** is written in Python, for handling local
disk files in asyncio applications.

Base on `aiofiles` and just like pathlib, but use await.

```py
with open('filename', 'w') as f:
    f.write('My file contents')

text = await aiopathlib.AsyncPath('filename').read_text()
print(text)
'My file contents'

content = await aiopathlib.AsyncPath(Path('filename')).read_bytes()
print(content)
b'My file contents'
```

Asynchronous interface to create folder.

```py
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

To install aiofiles, simply:


```bash
$ pip install aiopathlib
```


Usage
-----


* ``read_text``
* ``read_bytes``
* ``read_json``
* ``write_text``
* ``write_bytes``
* ``write_json``
* ``mkdir``
* ``exists``
* ``rename``
* ``remove``


History
-------

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
