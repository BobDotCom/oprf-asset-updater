import argparse
import os
import json

import requests

parser = argparse.ArgumentParser(
    prog="OPRF Asset Updater",
    description="A script which automatically updates OPRF standard asset files from the OpRedFlag repository",
)
parser.add_argument(
    '-d',
    "--directory",
    help="Local root directory",
    required=False,
    default=".",
)
parser.add_argument(
    "-r",
    "--repository",
    help='Location of OpRedFlag asset GitHub repository, in User/Repo format. Default: "BobDotCom/OpRedFlag"',
    required=False,
    default="BobDotCom/OpRedFlag",
)
parser.add_argument(
    "-b",
    "--branch",
    help='The branch of the repository to use. Default: "master"',
    required=False,
    default="master",
)
parser.add_argument(
    "-v",
    "--version-json",
    help='Location of local versions.json file. Default: "oprf-versions.json"',
    required=False,
    default="oprf-versions.json",
)
parser.add_argument(
    "-i",
    "--include",
    help='Files to update, separated by commas. Default: "*"',
    required=False,
    default="*",
)
parser.add_argument(
    "-e",
    "--exclude",
    help='Files to skip, separated by commas. Default: ""',
    required=False,
    default="",
)
parser.add_argument(
    "-m",
    "--major",
    # action="store_true",
    help="Allow major updates, not recommended until after verifying compatibility",
    required=False,
    default="false",
    choices=["true", "false"]
)
# parser.add_argument(
#     "--damage",
#     help="Location of local damage.nas file",
#     required=False,
# )


args = parser.parse_args()
#print(args)

version_json = os.path.join(args.directory, args.version_json)

# if not os.path.isfile(args.version_json):
#     with open(args.version_json):
with open(version_json, "r") as f:
    local_version_data = json.load(f)


def build_remote_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{args.repository}/{args.branch}/{path}"


def save_local_version_data():
    with open(version_json, "w") as f:
        json.dump(local_version_data, f)


def compare_versions(first, second):
    if first is None or second is None:
        return None
    val1 = [int(val) for val in first.split(".")]
    val2 = [int(val) for val in second.split(".")]
    if val1[0] > val2[0]:
        return 3
    if val1[:2] > val2[:2]:
        return 2
    if val1 > val2:
        return 1
    if val1 == val2:
        return 0
    if val2[0] > val1[0]:
        return -3
    if val2[:2] > val1[:2]:
        return -2
    if val2 > val1:
        return -1


# with requests.get(build_remote_url("versions.json")) as response:
#     remote_version_data = response.json()
remote_version_data = {'vector': {'version': '1.0.0', 'path': 'emesary-damage-system/nasal/vector.nas'}, 'missile-code': {'version': '1.0.0', 'path': 'emesary-damage-system/nasal/missile-code.nas'}, 'radar-system': {'version': '1.0.0', 'path': 'radar/radar-system.nas'}, 'damage': {'version': '1.0.0', 'path': 'emesary-damage-system/nasal/damage.nas'}, 'iff': {'version': '1.0.0', 'path': 'libraries/iff.nas'}, 'datalink': {'version': '1.0.0', 'path': 'libraries/datalink.nas'}, 'station-manager': {'version': '1.0.0', 'path': 'libraries/station-manager.nas'}, 'rcs-mand': {'version': '1.0.0', 'path': 'radar/rcs.txt'}, 'hud-math': {'version': '1.0.0', 'path': 'libraries/hud_math.nas'}, 'armament-notification': {'version': '1.0.0', 'path': 'emesary-damage-system/nasal/ArmamentNotification.nas'}}

if args.include == "*":
    keys_to_check = list(local_version_data.keys())
elif args.include == "":
    keys_to_check = []
else:
    keys_to_check = args.include.split(",")

if args.exclude != "":
    for key in args.exclude.split(","):
        keys_to_check.remove(key)

for key, value in {key: local_version_data[key] for key in keys_to_check}.items():
    def update(major: bool = False):
        with requests.get(build_remote_url(remote_version_data[key]["path"])) as response:
            response.raise_for_status()
            with open(os.path.join(args.directory, value["path"]), "w") as f:
                f.write(response.text)
        print(f"Fetched {key} {value['version']}->{remote_version_data[key]['version']}")
        value["version"] = remote_version_data[key]["version"]
    match compare_versions(remote_version_data[key]["version"], value["version"]):
        case 3:  # Remote is a major version bump ahead of us
            if args.major:
                update()
            else:
                print(f"Remote {key} ({remote_version_data[key]['version']}) is a major version newer than ours ({value['version']}), skipping.")
        case 2, 1, None:  # Remote is a minor/patch version bump ahead of us, or we don't have a saved version yet
            update()
        case -1, -2, -3:
            raise RuntimeError(f"Local {key} ({value['version']}) is newer than remote ({remote_version_data[key]['version']})")
        case 0:
            print(f"{key} is up-to-date ({value['version']})")
    save_local_version_data()
