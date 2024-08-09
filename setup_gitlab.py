from config import *

# setup gitlab volumes location
if not os.path.exists(".env"):
    write_texts(
        ".env", [f"GITLAB_HOME={SHARE_FOLDER_DIR}/gitlab", f"GITLAB_SSL=/etc/ssl"]
    )

# remove old ollama container
remove_docker_container("gitlab-service")

# pull latest image
pull_docker_base_image("gitlab/gitlab-ee:latest")

# setup docker-compose
check_call(["docker", "compose", "up", "-d", "gitlab_web"])
