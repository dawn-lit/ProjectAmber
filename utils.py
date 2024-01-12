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
