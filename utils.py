import json
import os
from subprocess import check_call
from typing import Final

import yaml

# base path
BASE_PATH: Final[str] = os.path.dirname(__file__)


def execute_sudo_apt(*action: str) -> None:
    check_call(["sudo", "apt", *action])


def execute_sudo_apt_install(_lib: str) -> None:
    execute_sudo_apt("install", _lib, "-y")


def execute_sudo_snap(*action: str) -> None:
    check_call(["sudo", "snap", *action])


def read_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return dict(yaml.load(f.read(), Loader=yaml.Loader))
        else:
            return dict(json.load(f))


def write_config(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            yaml.dump(data, f, allow_unicode=True)
        else:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)


def execute_sudo_snap_install(_lib: str) -> None:
    execute_sudo_snap("install", _lib, "-y")


def execute_sudo_docker(*action: str) -> None:
    check_call(["sudo", "docker", *action])


def add_content(path: str, content: str) -> None:
    check_call(["sudo", "bash", "-c", " ".join(["echo", "-e", content, ">>", path])])


def write_texts(path: str, texts: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(texts)


def restart_service(name: str) -> None:
    check_call(["sudo", "service", name, "restart"])


# user customized configuration
CUSTOM_CONFIGURATION: Final[dict] = read_config(
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

# make sure ssl key is valid
if len(CUSTOM_CONFIGURATION["ssl_key"]) == 0:
    raise ValueError("configuration.json: ssl_key has not being configured correctly!")

# make sure ssl cert is valid
if len(CUSTOM_CONFIGURATION["ssl_cert"]) == 0:
    raise ValueError("configuration.json: ssl_cert has not being configured correctly!")

# path to locally shared folder
SHARE_FOLDER_DIR: Final[str] = os.path.join(
    "/home", CUSTOM_CONFIGURATION["username"], "MyShare"
)
