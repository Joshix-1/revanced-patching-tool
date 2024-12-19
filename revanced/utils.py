import shutil
import sys

from tempfile import NamedTemporaryFile

from subprocess import run
from bs4 import BeautifulSoup


def eprint(*args, **kwargs) -> None:
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


def download_file(url: str, suffix: str) -> NamedTemporaryFile:
    out_file = NamedTemporaryFile(suffix=suffix, prefix=url.split("/")[-1])

    eprint("Downloading", url)

    try:
        run(["curl", "-sSfLo", out_file.name, url], check=True)
    except Exception:
        eprint(resp.headers)
        input()
        raise

    eprint("downloaded to", out_file.name)
    return out_file

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")
