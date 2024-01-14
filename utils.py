import json
import os
from subprocess import check_call
from typing import Final

# base path
BASE_PATH: Final[str] = os.path.dirname(__file__)


def execute_sudo_apt(*action: str) -> None:
    check_call(["sudo", "apt", *action])


def execute_sudo_apt_install(_lib: str) -> None:
    execute_sudo_apt("install", _lib, "-y")


def execute_sudo_snap(*action: str) -> None:
    check_call(["sudo", "snap", *action])


def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return dict(json.load(f))


def write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)


def execute_sudo_snap_install(_lib: str) -> None:
    execute_sudo_snap("install", _lib, "-y")


def execute_sudo_docker(*action: str) -> None:
    check_call(["sudo", "docker", *action])


# user customized configuration
CUSTOM_CONFIGURATION: Final[dict] = read_json(
    os.path.join(BASE_PATH, "configuration.json")
)

# make sure user customized configuration has been configured
if (
    CUSTOM_CONFIGURATION["dawnlit_database_connection"]
    == "Host=localhost;Database=main;Username=postgres;Password=root"
):
    raise ValueError(
        "configuration.json: dawnlit_database_connection has not being configured correctly!"
    )

if len(CUSTOM_CONFIGURATION["password"]) == 0:
    raise ValueError("configuration.json: password has not being configured correctly!")

if len(CUSTOM_CONFIGURATION["username"]) == 0:
    raise ValueError("configuration.json: username has not being configured correctly!")

# path to locally shared folder
SHARE_FOLDER_DIR: Final[str] = os.path.join(
    "/home", CUSTOM_CONFIGURATION["username"], "MyShare"
)
