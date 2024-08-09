from config import *

# remove old code-server container
remove_docker_container("code-server")

# pull latest image
pull_docker_base_image("codercom/code-server:latest")

# start code-server
coder_commend = f"""
docker run -d --name code-server -p 8949:8080 -v "$HOME/.local:/home/coder/.local" -v "$HOME/.config:/home/coder/.config" -v "{SHARE_FOLDER_DIR}:/home/coder/{CUSTOM_CONFIGURATION['SharedFolderName']}" -v "$PWD:/home/coder/project" -u "$(id -u):$(id -g)" -e "DOCKER_USER=$USER" codercom/code-server:latest
"""
check_call(coder_commend, shell=True)
