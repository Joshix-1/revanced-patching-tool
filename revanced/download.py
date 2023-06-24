import shutil
import sys

from tempfile import NamedTemporaryFile

import urllib3

c = urllib3.PoolManager()

def eprint(*args, **kwargs) -> None:
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def download_file(url: str, suffix: str) -> NamedTemporaryFile:
    out_file = NamedTemporaryFile(suffix=suffix)
    with c.request('GET', url, preload_content=False) as resp:
        shutil.copyfileobj(resp, out_file)
    if resp.status != 200:
        eprint(resp.headers)
        input()
        raise ValueError(f"Download failed ({resp.status=})")
    eprint(resp.url, out_file.name)
    return out_file
