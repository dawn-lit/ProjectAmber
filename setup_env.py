from utils import *

# keep system running with the lid closed
add_content("/etc/systemd/logind.conf", "HandleLidSwitch=ignore")
add_content("/etc/systemd/logind.conf", "LidSwitchIgnoreInhibited=no")
add_content("/etc/needrestart/needrestart.conf", "$nrconf{restart} = 'a'")

# update to latest env
execute_sudo_apt("update")
execute_sudo_apt("upgrade", "-y")
execute_sudo_apt("autoremove")
execute_sudo_apt("autoclean")

# install necessary apt packages
_apt_packages: Final[tuple[str, ...]] = (
    "git",
    "git-lfs",
    "docker",
    "docker-compose",
    "cockpit",
    "samba",
    "python3-pip",
    "nginx",
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
os.makedirs(SHARE_FOLDER_DIR, exist_ok=True)
public_folder(SHARE_FOLDER_DIR)
# add config to smb.conf
add_content("/etc/samba/smb.conf", "[sambashare]")
add_content("/etc/samba/smb.conf", "    comment = Samba on DawnLit")
add_content("/etc/samba/smb.conf", f"    path = {SHARE_FOLDER_DIR}")
add_content("/etc/samba/smb.conf", "    read only = no")
add_content("/etc/samba/smb.conf", "    browsable = yes")
# restart Samba
restart_service("smbd")
# Update the firewall rules to allow Samba traffic
check_call(["sudo", "ufw", "allow", "samba"])
# setup samba user
write_texts(
    "./createSambaUser.sh",
    [
        "#!/bin/bash",
        f'username={CUSTOM_CONFIGURATION["username"]}',
        f'password={CUSTOM_CONFIGURATION["password"]}',
        '(echo "$password"; echo "$password") | smbpasswd -s -a "$username"',
    ],
)
check_call(["sudo", "sh", "./createSambaUser.sh"])

os.remove("./createSambaUser.sh")

check_call(["sudo", "reboot"])
