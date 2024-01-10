from subprocess import check_call
import shutil


def _execute_sudo_apt(*action: str) -> None:
    check_call(["sudo", "apt", *action])


def _execute_sudo_apt_install(_lib: str) -> None:
    _execute_sudo_apt("install", _lib, "-y")


def _execute_sudo_snap(*action: str) -> None:
    check_call(["sudo", "snap", *action])


def _execute_sudo_snap_install(_lib: str) -> None:
    _execute_sudo_snap("install", _lib, "-y")


# update to latest env
_execute_sudo_apt("update")
_execute_sudo_apt("upgrade", "-y")
_execute_sudo_apt("autoremove")
_execute_sudo_apt("autoclean")

# install apt packages
_apt_packages: tuple[str, ...] = (
    "git",
    "docker",
    "docker-compose",
    "docker-compose-plugin",
)
for pkg in _apt_packages:
    _execute_sudo_apt_install(pkg)

# refresh snap
_execute_sudo_snap("refresh")

# install apt packages
_snap_packages: tuple[str, ...] = ()
for pkg in _snap_packages:
    _execute_sudo_snap_install(pkg)

# setup nginx
shutil.copy2("./nginx.conf", "/etc/nginx/conf.d/default.conf")
# restart nginx service
check_call(["sudo", "service", "nginx", "restart"])
