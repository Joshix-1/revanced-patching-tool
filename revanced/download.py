import shutil
import sys

from tempfile import NamedTemporaryFile

import urllib3

from bs4 import BeautifulSoup

APK_MIRROR_BASE_URL = "https://www.apkmirror.com"
SEARCH_URL = APK_MIRROR_BASE_URL + "/?post_type=app_release&searchtype=apk&s={version}+{app}&arch%5B%5D=universal"

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")

def eprint(*args, **kwargs) -> None:
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)

def download_file(url: str, suffix: str) -> NamedTemporaryFile:
    c = urllib3.PoolManager()
    out_file = NamedTemporaryFile(suffix=suffix)
    with c.request('GET',url, preload_content=False) as resp:
        shutil.copyfileobj(resp, out_file)
    eprint(url, out_file.name)
    return out_file


def download_apk(app: str, version: str) -> NamedTemporaryFile:
    search_response = urllib3.request("GET", SEARCH_URL.format(app=app, version=version))
    soup = parse_html(search_response.data)
    paths = {
        el.get("href")
        for el in soup.find_all(class_="downloadLink")
        if version.replace(".", "-") in el.get("href")
    }
    assert len(paths) == 1, f"found {paths} links"
    path = paths.pop()
    eprint(path)

    download_info_response = urllib3.request("GET", APK_MIRROR_BASE_URL + path)
    soup = parse_html(download_info_response.data)
    els = soup.find(text="universal").find_parent().find_parent().find(class_="accent_color")
    path = els.get("href")
    eprint(path)

    download_response = urllib3.request("GET", APK_MIRROR_BASE_URL + path)
    soup = parse_html(download_response.data)
    els = soup.find(class_="downloadButton", rel="nofollow")
    path = els.get("href")
    eprint(path)
    return download_file(APK_MIRROR_BASE_URL + path, ".apk")


