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


def execute_docker(*action: str) -> None:
    check_call(["docker", *action])


def add_content(path: str, content: str) -> None:
    check_call(["sudo", "bash", "-c", " ".join(["echo", "-e", content, ">>", path])])


def write_texts(path: str, texts: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(
            t + "\n" if i != len(texts) - 1 else t for i, t in enumerate(texts)
        )


def remove_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def restart_service(name: str) -> None:
    check_call(["sudo", "service", name, "restart"])


def restart_systemctl(name: str) -> None:
    check_call(["sudo", "systemctl", "restart", name])


def public_folder(_dir: str) -> None:
    check_call(["sudo", "chmod", "777", "-R", _dir])


def replace_content_in_file(
    file_path: str, from_text: str, to_text: str, out: None | str = None
) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        content: str = f.read()
    with open(file_path if out is None else out, "w", encoding="utf-8") as f:
        f.write(content.replace(from_text, to_text))


# user customized configuration
CUSTOM_CONFIGURATION_PATH: Final[str] = os.path.join(BASE_PATH, "configuration.json")
CUSTOM_CONFIGURATION: Final[dict] = read_config(CUSTOM_CONFIGURATION_PATH)

_ENABLE_CUSTOM_CONFIGURATION_VALIDATION: bool = True

if _ENABLE_CUSTOM_CONFIGURATION_VALIDATION:
    if len(CUSTOM_CONFIGURATION["password"]) == 0:
        raise ValueError(
            "configuration.json: password has not being configured correctly!"
        )

    if len(CUSTOM_CONFIGURATION["username"]) == 0:
        raise ValueError(
            "configuration.json: username has not being configured correctly!"
        )

    # make sure ssl key is valid
    if len(CUSTOM_CONFIGURATION["ssl_key"]) == 0:
        raise ValueError(
            "configuration.json: ssl_key has not being configured correctly!"
        )

    # make sure ssl cert is valid
    if len(CUSTOM_CONFIGURATION["ssl_cert"]) == 0:
        raise ValueError(
            "configuration.json: ssl_cert has not being configured correctly!"
        )

    # make domain is valid
    if len(CUSTOM_CONFIGURATION["domain"]) == "example.com":
        raise ValueError(
            "configuration.json: domain has not being configured correctly!"
        )

# path to locally shared folder
SHARE_FOLDER_DIR: Final[str] = os.path.join(
    "/home", CUSTOM_CONFIGURATION["username"], CUSTOM_CONFIGURATION["SharedFolderName"]
)

# update domain in files
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "nginx.glob.conf"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "services", "nginx.glob.conf"),
)
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "nginx.dawnlit.prod.conf"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "services", "nginx.dawnlit.prod.conf"),
)
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "docker-compose.yml"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "services", "docker-compose.yml"),
)

# update postgres_db config username and password
dk_compose: dict = read_config(
    os.path.join(BASE_PATH, "services", "docker-compose.yml")
)
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_DB"] = (
    CUSTOM_CONFIGURATION["postgres_db_name"]
)
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_USER"] = (
    CUSTOM_CONFIGURATION["postgres_db_username"]
)
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_PASSWORD"] = (
    CUSTOM_CONFIGURATION["postgres_db_password"]
)
write_config(os.path.join(BASE_PATH, "services", "docker-compose.yml"), dk_compose)
