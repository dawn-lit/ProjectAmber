import json
import os
from subprocess import check_call, check_output

import yaml


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


def stop_docker_container(name: str) -> None:
    try:
        execute_docker("container", "stop", name)
    except Exception:
        print(f"Warning: Unable to stop container '{name}'")


def remove_docker_container(name: str) -> None:
    try:
        stop_docker_container(name)
        execute_docker("container", "remove", name)
    except Exception:
        print(f"Warning: Unable to remove container '{name}'")


def pull_docker_base_image(name: str) -> None:
    try:
        execute_docker("image", "pull", name)
    except Exception:
        print(f"Warning: Unable to pull base image '{name}'")


def get_all_docker_containers() -> tuple[str, ...]:
    return tuple(check_output(["docker", "ps", "-a", "-q"]).decode().split("\n")[:-1])


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
