# ChangeLog

## 0.6

#### 0.6.1 (2025-08-03)
- feat: override resolve to be asynchronous (#1)
- feat: auto use orjson to speed up json read/write

#### 0.6.0 (2025-08-01)
- Migrate from poetry to uv

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
