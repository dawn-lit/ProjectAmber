from utils import *

# update to latest env
execute_sudo_apt("update")
execute_sudo_apt("upgrade", "-y")
execute_sudo_apt("autoremove")
execute_sudo_apt("autoclean")

# install necessary apt packages
_apt_packages: Final[tuple[str, ...]] = (
    "git",
    "docker",
    "docker-compose",
    "docker-compose-plugin",
    "samba",
    *CUSTOM_CONFIGURATION["additional_apt_packages"],
)
for pkg in _apt_packages:
    execute_sudo_apt_install(pkg)

# refresh snap
execute_sudo_snap("refresh")

# install apt packages
_snap_packages: Final[tuple[str, ...]] = CUSTOM_CONFIGURATION[
    "additional_snap_packages"
]
for pkg in _snap_packages:
    execute_sudo_snap_install(pkg)

# create folder for samba share
os.makedirs(f"/home/{CUSTOM_CONFIGURATION['username']}/share", exist_ok=True)
# add config to smb.conf
check_call(
    [
        "sudo",
        "echo",
        "-e",
        f"[sambashare]\n    comment = Samba on DawnLit\n    path = /home/{CUSTOM_CONFIGURATION['username']}/sambashare\n    read only = no\n    browsable = yes\n",
        ">>",
        "/etc/samba/smb.conf",
    ]
)
# restart Samba
check_call(["sudo", "service", "smbd", "restart"])
# Update the firewall rules to allow Samba traffic:
check_call(["sudo", "ufw", "allow", "samba"])
# setup samba user
check_call(
    [
        "sudo",
        "echo",
        "-e",
        f'#!/bin/bash\nusername={CUSTOM_CONFIGURATION["username"]}\npassword={CUSTOM_CONFIGURATION["password"]}\n(echo "$password"; echo "$password") | smbpasswd -s -a "$username"\n',
        ">>",
        "./createSambaUser.sh",
    ]
)
check_call(["sudo", "./createSambaUser.sh"])
