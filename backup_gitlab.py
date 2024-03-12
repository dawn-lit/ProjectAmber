from utils import *

# remove all previous backup
try:
    execute_sudo_docker(
        "exec",
        "gitlab-service",
        "/bin/bash",
        "-c",
        "'rm -rf /var/opt/gitlab/backups/*'",
    )
except Exception:
    print("Unable to remove old backup in container, skip!")

# execute backup cmd
execute_sudo_docker("exec", "gitlab-service", "gitlab-backup", "create")

# create folder for backup
gitlab_backup_dir: str = os.path.join(SHARE_FOLDER_DIR, "gitlab_backup")
if not os.path.exists(gitlab_backup_dir):
    os.mkdir(gitlab_backup_dir)

# copy backup to host
execute_sudo_docker("cp", "gitlab-service:/var/opt/gitlab/backups", gitlab_backup_dir)
