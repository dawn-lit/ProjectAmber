import shutil

from config import *

# setup gitlab volumes location
write_texts(".env", [f"GITLAB_HOME={SHARE_FOLDER_DIR}/gitlab", f"GITLAB_SSL=/etc/ssl"])

# setup docker-compose
check_call(["docker", "compose", "up", "-d", "postgres_db", "gitlab_web"])

# dawnlit backend dir path
_BACKEND_DIR: str = os.path.join(BASE_PATH, "DawnLitWeb")

# clone dawnlit backend
if not os.path.exists(_BACKEND_DIR):
    check_call(["git", "clone", "https://github.com/yudonglin/DawnLitWeb.git"])
else:
    check_call(["git", "pull"], cwd=_BACKEND_DIR)
check_call(["git", "lfs", "fetch", "--all"], cwd=_BACKEND_DIR)

# modify backend database connection
app_settings: Final[dict] = read_config(os.path.join(_BACKEND_DIR, "appsettings.json"))
app_settings["Database"][
    "Connection"
] = f'Host={CUSTOM_CONFIGURATION["postgres_db_host"]};\
    Database={CUSTOM_CONFIGURATION["postgres_db_name"]};\
        Username={CUSTOM_CONFIGURATION["postgres_db_username"]};\
            Password={CUSTOM_CONFIGURATION["postgres_db_password"]}'
write_config(os.path.join(_BACKEND_DIR, "appsettings.json"), app_settings)

# build back-end application
execute_docker("build", _BACKEND_DIR, "-t", "dotnet-app")
# run back-end application
execute_docker("run", "--name", "dotnet-app", "-d", "-p", "7061:8080", "dotnet-app")

# dawnlit frontend dir path
_FRONTEND_DIR = os.path.join(_BACKEND_DIR, "View")

# make ssl folder
os.makedirs(os.path.join(_FRONTEND_DIR, "ssl"), exist_ok=True)
# write dns certificate to front-end
write_texts(
    os.path.join(_FRONTEND_DIR, "ssl", "cert.pem"), CUSTOM_CONFIGURATION["ssl_cert"]
)
# write dns key to front-end
write_texts(
    os.path.join(_FRONTEND_DIR, "ssl", "key.pem"), CUSTOM_CONFIGURATION["ssl_key"]
)
# use Dockerfile
remove_if_exists(os.path.join(_FRONTEND_DIR, "Dockerfile"))
shutil.copyfile(
    os.path.join(BASE_PATH, "services", "Dockerfile"),
    os.path.join(_FRONTEND_DIR, "Dockerfile"),
)
# use nginx.dawnlit.prod.conf
remove_if_exists(os.path.join(_FRONTEND_DIR, "nginx.conf"))
shutil.copyfile(
    os.path.join(BASE_PATH, "services", "nginx.dawnlit.prod.conf"),
    os.path.join(_FRONTEND_DIR, "nginx.conf"),
)
# build front-end application
execute_docker("build", _FRONTEND_DIR, "-t", "angular-app")
# run front-end application
execute_docker("run", "--name", "angular-app", "-d", "-p", "4200:443", "angular-app")

# start code-server
coder_commend = f"""
docker run --name code-server -p 8949:8080 -v "$HOME/.local:/home/coder/.local" -v "$HOME/.config:/home/coder/.config" -v "{SHARE_FOLDER_DIR}:/home/coder/{CUSTOM_CONFIGURATION['SharedFolderName']}" -v "$PWD:/home/coder/project" -u "$(id -u):$(id -g)" -e "DOCKER_USER=$USER" codercom/code-server:latest
"""
check_call(coder_commend, shell=True)

# setup nginx
shutil.copy2(
    os.path.join(BASE_PATH, "services", "nginx.glob.conf"),
    "/etc/nginx/conf.d/default.conf",
)

# restart nginx service
restart_service("nginx")
