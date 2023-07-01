import shutil
import sys

from tempfile import NamedTemporaryFile

import urllib3
from bs4 import BeautifulSoup

c = urllib3.PoolManager()

def eprint(*args, **kwargs) -> None:
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def download_file(
    url: str, suffix: str, headers: "dict[str, str] | None" = None
) -> NamedTemporaryFile:
    out_file = NamedTemporaryFile(suffix=suffix, prefix=url.split("/")[-1])
    eprint("Downloading", url)
    with c.request('GET', url, preload_content=False, headers=headers) as resp:
        shutil.copyfileobj(resp, out_file)
    if resp.status != 200:
        eprint(resp.headers)
        input()
        raise ValueError(f"Download failed ({resp.status=})")
    eprint(resp.url, out_file.name)
    return out_file

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")
