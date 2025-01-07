from typing import Union

import requests

GITLAB_URL = "https://code.ihep.ac.cn"
PROJECT_ID = "5548"

# API URL to get all tags of a project
TAGS_API_URL = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/tags"


def get_all_tags():
    tags = []
    page = 1
    while True:
        response = requests.get(TAGS_API_URL, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error fetching tags: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            break  # No more tags to fetch

        tags.extend(data)
        page += 1

    return [t["name"] for t in tags]


def get_latest_version(tags: list[str]) -> Union[tuple[int, int, int, int], None]:
    latest_version = None

    for tag in tags:
        if not tag.startswith("v"):
            continue

        try:
            version = [int(i) for i in tag[1:].split(".")]
            if len(version) == 3:
                version.append(0)
            elif len(version) != 4:
                continue

            if latest_version is None or version > latest_version:
                latest_version = version
        except:
            continue

    return tuple(latest_version)


def check_latest_version(test_version_tuple: Union[tuple[int, int, int, int], None] = None):
    tags = get_all_tags()
    latest_version = get_latest_version(tags)

    if latest_version is None:
        if test_version_tuple is None:  # Not being tested, keep silent
            return
        else:
            raise ValueError("Failed to get latest version from GitLab")

    if test_version_tuple is None:
        # get current version
        try:
            from ._version import __version_tuple__ as current_version_tuple
        except ImportError:
            return
    else:
        current_version_tuple = test_version_tuple

    if len(current_version_tuple) > 4:  # dev version
        return

    if len(current_version_tuple) == 3:
        current_version = current_version_tuple + (0,)
    elif len(current_version_tuple) == 4:
        current_version = current_version_tuple
    else:
        raise ValueError("Invalid version tuple")

    if current_version < latest_version:
        print(
            f"Warning: A newer version is available: \"{'.'.join(map(str, latest_version))}\". "
            "It is recommended to upgrade to latest version, since `pybes3` is still in beta version "
            "and there might be bug fixes and new features in the latest version."
        )
        print(
            f"You can run `pip install pybes3 --upgrade [--user]` to upgrade to the latest version."
        )
