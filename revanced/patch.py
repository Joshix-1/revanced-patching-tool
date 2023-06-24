import subprocess
import sys

from functools import cache

import urllib3

from .download import download_file

REVANCED_TOOLS_URL = "https://releases.revanced.app/tools"

def download_patches() -> list:
    return urllib3.request("GET", get_tool_url("revanced/revanced-patches", ".json")).json()

def get_app_version(app: str, patches: list[dict]) -> str:
    versions: set[frozenset[str]] = set()
    for patch in patches:
        versions.update(
            frozenset(package["versions"])
            for package in patch["compatiblePackages"]
            if package["name"] == app
            if package["versions"]  # empty means everything is compatible
        )
    return max(frozenset.intersection(*versions))

@cache
def _get_tools() -> list[dict]:
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
    selected_patches: dict[str, list[object]],
) -> None | str:
    patches = [
        patch
        for patch in download_patches()
        if patch["name"] in selected_patches
    ]
    version = get_app_version(app, patches)

    # TODO: make apkmirror download work
    if len(sys.argv) == 2:
        apk_file = sys.argv[1]
    else:
        sys.exit(
            f"Download {app} {version} from apkmirror and provide the path as argument\n"
            f"Visit: https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s={version}+{app}&arch%5B%5D=universal&dpi[]=nodpi"
        )

    subprocess.run(["file", apk_file])  # for debugging

    revanced_cli_jar = download_file(get_tool_url("revanced/revanced-cli", ".jar"), ".jar")
    revanced_patches_jar = download_file(get_tool_url("revanced/revanced-patches", ".jar"), ".jar")
    revanced_integrations_apk = download_file(get_tool_url("revanced/revanced-integrations", ".apk"), ".apk")
    command = [
        "java", "-jar", revanced_cli_jar.name,
        "-a", apk_file,
        "-o", "output.apk",
        "-b", revanced_patches_jar.name,
        "-m", revanced_integrations_apk.name,
        "--exclusive",
    ]
    for patch in selected_patches:
        command.extend(["-i", patch])
    print(command)
    subprocess.run(command)

