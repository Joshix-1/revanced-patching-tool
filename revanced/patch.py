import subprocess
import sys

from functools import cache

import urllib3

from .apk_download import download_apk
from .utils import download_file, eprint

REVANCED_TOOLS_URL = "https://api.revanced.app/tools"

def download_patches() -> list:
    return urllib3.request("GET", "https://api.revanced.app/v4/patches/list").json()


def patch_supports_app(patch: dict, app: str) -> bool:
    if not patch["compatiblePackages"]:
        eprint("compatiblePackages not present", app, patch)
        return False
    return app in {package for package in patch["compatiblePackages"]}

def get_app_version(app: str, patches: list[dict]) -> str:
    versions: set[frozenset[str]] = set()
    for patch in patches:
        print(patch)
        versions.update(
            frozenset(versions)
            for (package, versions) in patch["compatiblePackages"].items()
            if package == app
            if versions  # empty means everything is compatible
        )
    return max(frozenset.intersection(*versions))

@cache
def _get_tools() -> list[dict]:
    eprint("Downloading data from https://api.revanced.app/tools")
    return sorted(
        urllib3.request("GET", "https://api.revanced.app/tools").json()["tools"],
        key=lambda tool: tool["version"],
        reverse=True,
    )

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
    version: str | None = None,
) -> "None | str":
    eprint("Not selected patches:", tuple(sorted(
        set(patch["name"] for patch in download_patches() if patch_supports_app(patch, app)) - set(selected_patches)
    )))
    patches = [
        patch
        for patch in download_patches()
        if patch["name"] in selected_patches
        if patch_supports_app(patch, app)
    ]
    eprint("\033[91mMissing patches:", tuple(sorted(
        set(selected_patches) - set(p["name"] for p in patches)
    )), "\033[0m")
    version = version or get_app_version(app, patches)
    eprint("Version: ", version)

    eprint("\n\n")

    apk_file = download_apk(app, version)

    subprocess.run(["file", apk_file.name])  # for debugging
    subprocess.run(["apkinfo", apk_file.name])  # for debugging

    revanced_cli_jar = download_file(get_tool_url("revanced/revanced-cli", ".jar"), ".jar")
    revanced_patches_jar = download_file(get_tool_url("revanced/revanced-patches", ".rvp"), ".rvp")
    #revanced_integrations_apk = download_file(get_tool_url("revanced/revanced-integrations", ".apk"), ".apk")
    subprocess.run(["java", "-jar", revanced_cli_jar.name, "patch", "--help"])
    command = [
        "java", "-jar", revanced_cli_jar.name,
        "patch",
        "-o", "output.apk",
        "--patches", revanced_patches_jar.name,
        "--keystore-entry-alias=alias",
        "--keystore-entry-password=ReVanced",
        "--keystore-password=ReVanced",
        "--keystore=output.keystore",
        "--exclusive",
    ]
    for patch in selected_patches:
        command.extend(["-e", patch])
    command.append(apk_file.name)
    print(command)
    try:
        subprocess.run(command, check=True)
    except:
        input()
        pass
