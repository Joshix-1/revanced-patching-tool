import subprocess
import sys

from functools import cache

import urllib3

from .apk_download import download_apk
from .utils import download_file, eprint

REVANCED_TOOLS_URL = "https://releases.revanced.app/tools"

def download_patches() -> list:
    return urllib3.request("GET", get_tool_url("revanced/revanced-patches", ".json")).json()

def get_app_version(app: str, patches: list[dict]) -> str:
    versions: set[frozenset[str]] = set()
    for patch in patches:
        print(patch)
        versions.update(
            frozenset(package["versions"])
            for package in patch["compatiblePackages"]
            if package["name"] == app
            if package["versions"]  # empty means everything is compatible
        )
    return max(frozenset.intersection(*versions))

@cache
def _get_tools() -> list[dict]:
    eprint("Downloading data from https://releases.revanced.app/tools")
    return urllib3.request("GET", "https://releases.revanced.app/tools").json()["tools"]

def get_tool_url(repo: str, file_extension: str) -> str:
    for tool in _get_tools():
        if tool["repository"] != repo:
            continue
        url = tool["browser_download_url"]
        if not url.endswith(file_extension):
            continue
        return url
    raise ValueError(f"Tool not found ({repo=}, {file_extension=})")

def create_patched_apk(
    app: str,
    selected_patches: set[str],
) -> "None | str":
    patches = [
        patch
        for patch in download_patches()
        if patch["name"] in selected_patches
    ]
    for p in selected_patches:
        if p not in {_["name"] for _ in patches}:
            eprint(f"{p} not found")
    version = get_app_version(app, patches)
    eprint("Version: ", version)
    apk_file = download_apk(app, version)

    subprocess.run(["file", apk_file.name])  # for debugging
    subprocess.run(["apkinfo", apk_file.name])  # for debugging

    revanced_cli_jar = download_file(get_tool_url("revanced/revanced-cli", ".jar"), ".jar")
    revanced_patches_jar = download_file(get_tool_url("revanced/revanced-patches", ".jar"), ".jar")
    revanced_integrations_apk = download_file(get_tool_url("revanced/revanced-integrations", ".apk"), ".apk")
    command = [
        "java", "-jar", revanced_cli_jar.name,
        "-a", apk_file.name,
        "-o", "output.apk",
        "-b", revanced_patches_jar.name,
        "-m", revanced_integrations_apk.name,
        "--exclusive",
    ]
    for patch in selected_patches:
        command.extend(["-i", patch])
    print(command)
    subprocess.run(command)
