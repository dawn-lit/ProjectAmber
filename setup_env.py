from utils import *

# keep system running with the lid closed
add_content("/etc/systemd/logind.conf", "HandleLidSwitch=ignore")
add_content("/etc/systemd/logind.conf", "LidSwitchIgnoreInhibited=no")
restart_service("systemd-logind")

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
    "cockpit",
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

# enable Cockpit
check_call(["sudo", "systemctl", "enable", "--now", "cockpit.socket"])

# create folder for samba share
os.makedirs(SHARE_FOLDER_DIR)
# add config to smb.conf
add_content(
    "/etc/samba/smb.conf",
    f"[sambashare]\n    comment = Samba on DawnLit\n    path = {SHARE_FOLDER_DIR}\n    read only = no\n    browsable = yes\n",
)
# restart Samba
restart_service("smbd")
# Update the firewall rules to allow Samba traffic:
check_call(["sudo", "ufw", "allow", "samba"])
# setup samba user
add_content(
    "./createSambaUser.sh",
    f'#!/bin/bash\nusername={CUSTOM_CONFIGURATION["username"]}\npassword={CUSTOM_CONFIGURATION["password"]}\n(echo "$password"; echo "$password") | smbpasswd -s -a "$username"\n',
)
check_call(["sudo", "./createSambaUser.sh"])
