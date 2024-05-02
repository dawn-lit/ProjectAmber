import shutil

from utils import *

"""
# mount usb stick commends
lsblk
sudo mkdir /media/usbstick
sudo mount -t vfat /dev/sdb1 /media/usbstick 
"""

# keep system running with the lid closed
add_content("/etc/systemd/logind.conf", "HandleLidSwitch=ignore")
add_content("/etc/systemd/logind.conf", "LidSwitchIgnoreInhibited=no")
add_content("/etc/needrestart/needrestart.conf", r"\$nrconf{restart} = \'a\'")

# update to latest env
execute_sudo_apt("update")
execute_sudo_apt("upgrade", "-y")
execute_sudo_apt("autoremove")
execute_sudo_apt("autoclean")

# install necessary apt packages
_apt_packages: Final[tuple[str, ...]] = (
    "git",
    "git-lfs",
    "cockpit",
    "samba",
    "python3-pip",
    "nginx",
    *CUSTOM_CONFIGURATION["additional_apt_packages"],
)
for pkg in _apt_packages:
    execute_sudo_apt_install(pkg)

# install docker
check_call(["sudo", "install", "-m", "0755", "-d", "/etc/apt/keyrings"])
check_call(
    [
        "sudo",
        "curl",
        "-fsSL",
        "https://download.docker.com/linux/ubuntu/gpg",
        "-o",
        "/etc/apt/keyrings/docker.asc",
    ]
)
check_call(["sudo", "chmod", "a+r", "/etc/apt/keyrings/docker.asc"])
theCommand: str = """
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
"""
check_call(theCommand, shell=True)
execute_sudo_apt("update")
_docker_packages: Final[tuple[str, ...]] = (
    "docker-ce",
    "docker-ce-cli",
    "containerd.io",
    "docker-buildx-plugin",
    "docker-compose",
    "docker-compose-plugin",
)
for pkg in _docker_packages:
    execute_sudo_apt_install(pkg)

# make docker.sock public to fix docker permission denied issue
public_folder("/var/run/docker.sock")

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

# create .config/code-server folder
check_call(["sudo", "mkdir", "-p", "/home/.config"])

# make .config/code-server folder public
public_folder("/home/.config")

# create .local/share/code-server folder
check_call(["sudo", "mkdir", "-p", "/home/.local"])

# make .config/code-server folder public
public_folder("/home/.local")

# make sure ssl dir exits
os.makedirs("/etc/ssl", exist_ok=True)
# write dns certificate
write_texts("/etc/ssl/cert.pem", CUSTOM_CONFIGURATION["ssl_cert"])
# write dns key
write_texts("/etc/ssl/key.pem", CUSTOM_CONFIGURATION["ssl_key"])

# setup ca
os.makedirs("/etc/ssl/certs", exist_ok=True)
check_call(["sudo", "update-ca-certificates"])

# setup nginx
shutil.copy2(
    os.path.join(BASE_PATH, "services", "nginx.glob.conf"),
    "/etc/nginx/conf.d/default.conf",
)

# restart nginx service
restart_service("nginx")


# reboot system
check_call(["sudo", "reboot"])
