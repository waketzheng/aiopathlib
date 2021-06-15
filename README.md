aiopathlib: Pathlib support for asyncio
==================================

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
~~~~~~~

0.1.0 (2021-06-14)
``````````````````

- Introduced a changelog.
- Publish at gitee.


Contributing
~~~~~~~~~~~~
Contributions are very welcome.
