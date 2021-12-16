#!/usr/bin/env python3
import asyncio

from aiopathlib import AsyncPath


async def clear_it(filename):
    p = AsyncPath(filename)
    ss = (await p.read_text()).splitlines()
    unique = {}
    for i in ss:
        package = i.split(";", 1)[0]
        name, version = package.strip().split("==")
        v = unique.get(name)
        if not v or v[0] < version:
            unique[name] = (version, package)
        else:
            print(name, "already exists! Ignore.")
    lines_count = len(unique)
    print(len(ss) - lines_count, "removed!")
    await p.write_text("\n".join(i[1] for i in unique.values()))
    print(p, "updated! Only", lines_count, "lines now.")


def main():
    filename = "dev_requirements.txt"
    asyncio.run(clear_it(filename))


if __name__ == "__main__":
    main()
