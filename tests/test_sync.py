from pathlib import Path

from aiopathlib import AsyncPath


def test_glob_rglob():
    ap = AsyncPath(__file__).parent
    p = Path(ap)
    assert [Path(i) for i in ap.glob("*")] == list(p.glob("*"))
    assert [Path(i) for i in ap.rglob("*")] == list(p.rglob("*"))
