from .utils import parse_html, eprint, download_file
from tempfile import NamedTemporaryFile

import urllib3


APK_MIRROR_BASE_URL = "https://www.apkmirror.com"
SEARCH_URL = APK_MIRROR_BASE_URL + "/?post_type=app_release&searchtype=apk&s={version}+{app}&arch%5B%5D=universal"
DOWNLOAD_URL = "https://d.apkpure.com/b/APK/{app}?versionCode={version_code}"


def get_version_code(app: str, version: str) -> "str | None":
    search_response = urllib3.request("GET", SEARCH_URL.format(app=app, version=version))
    soup = parse_html(search_response.data)
    paths = {
        el.get("href")
        for el in soup.find_all(tag="a")
        if version.replace(".", "-") in el.get("href")
    }
    assert len(paths) == 1, f"found {paths} links for {app=} {version=}"
    path = paths.pop()
    eprint(path)

    download_info_response = urllib3.request("GET", APK_MIRROR_BASE_URL + path)
    soup = parse_html(download_info_response.data)
    els = soup.find(text="nodpi").find_parent().find_parent().find_all(class_="colorLightBlack")
    versions = []
    for el in els:
        if el.text.isdigit():
            versions.append(el.text)

    eprint(app, version, versions)
    return max(versions, default=None)


def download_apk(app: str, version: str) -> NamedTemporaryFile:
    import os.path
    class x: name = os.path.expanduser("~/dl/com.google.android.youtube_20.12.46-1553610176_minAPI26(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk") # put path to apk here if download failed
    return x()
    code = get_version_code(app, version)
    if not code:
        raise ValueError(f"Could not find {app} {version}")
    url = DOWNLOAD_URL.format(version_code=code, app=app)
    return download_file(url, ".apk", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:114.0) Gecko/20100101 Firefox/114.0"})
