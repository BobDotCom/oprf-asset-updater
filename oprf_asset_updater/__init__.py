"""
OPRF Asset Updater
Copyright (C) 2023  BobDotCom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import json
from .enums import VersionComparison

import requests

from .typing_helpers import FileVersion


def main(directory: str, version_json: str, repository: str, branch: str, include: str, exclude: str, major: str, strict: str) -> None:
    version_json = os.path.join(directory, version_json)

    with open(version_json, "r") as f:
        local_version_data = json.load(f)

    def build_remote_url(path: str) -> str:
        return f"https://raw.githubusercontent.com/{repository}/{branch}/{path}"

    def save_local_version_data() -> None:
        with open(version_json, "w") as f:
            json.dump(local_version_data, f, indent=2)

    def compare_versions(first: str | None, second: str | None) -> VersionComparison:
        if first is None or second is None:
            return VersionComparison.UNKNOWN

        val1 = [int(val) for val in first.split(".")]
        val2 = [int(val) for val in second.split(".")]

        if val1[0] > val2[0]:
            return VersionComparison.NEWER_MAJOR
        if val1[:2] > val2[:2]:
            return VersionComparison.NEWER_MINOR
        if val1 > val2:
            return VersionComparison.NEWER_PATCH
        if val1 == val2:
            return VersionComparison.EQUAL
        if val2[0] > val1[0]:
            return VersionComparison.OLDER_MAJOR
        if val2[:2] > val1[:2]:
            return VersionComparison.OLDER_MINOR
        if val2 > val1:
            return VersionComparison.OLDER_PATCH

        raise RuntimeError("Unreachable code")

    with requests.get(build_remote_url("versions.json")) as response:
        remote_version_data = response.json()

    if include == "*":
        keys_to_check = list(local_version_data.keys())
    elif include == "":
        keys_to_check = []
    else:
        keys_to_check = include.split(",")

    if exclude != "":
        for key in exclude.split(","):
            keys_to_check.remove(key)

    def run_update(key: str, data: FileVersion) -> None:
        def update() -> None:
            with requests.get(build_remote_url(remote_version_data[key]["path"])) as response:
                response.raise_for_status()
                with open(os.path.join(directory, data["path"]), "w") as f:
                    f.write(response.text)
            print(f"Fetched {key} {data['version']}->{remote_version_data[key]['version']}")
            data["version"] = remote_version_data[key]["version"]
        match compare_versions(remote_version_data[key]["version"], data["version"]):
            case VersionComparison.NEWER_MAJOR:
                # Remote is a major version bump ahead of us
                if major == "true":
                    update()
                else:
                    print(f"Remote {key} ({remote_version_data[key]['version']}) is a major version newer than ours ({data['version']}), skipping.")
            case VersionComparison.NEWER_MINOR | VersionComparison.NEWER_PATCH | VersionComparison.UNKNOWN:
                # Remote is a minor/patch version bump ahead of us, or we don't have a saved version yet
                update()
            case VersionComparison.OLDER_MAJOR | VersionComparison.OLDER_MINOR | VersionComparison.OLDER_PATCH:
                newer_msg = f"Local {key} ({data['version']}) is newer than remote ({remote_version_data[key]['version']})"
                if strict == "true":
                    raise RuntimeError(newer_msg)
                else:
                    print(f"{newer_msg}, skipping.")
            case VersionComparison.EQUAL:
                print(f"{key} is up-to-date ({data['version']})")
        save_local_version_data()

    for key, value in {key: local_version_data[key] for key in keys_to_check}.items():
        run_update(key, value)
