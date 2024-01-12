import shutil

from utils import *

# setup docker-compose
execute_sudo_docker("compose", "up", "-d")

# clone dawnlit backend
check_call(["git", "clone", "https://github.com/yudonglin/DawnLitWeb.git"])

# modify backend database connection
app_settings: Final[dict] = read_json(
    os.path.join(BASE_PATH, "DawnLitWeb", "appsettings.json")
)
app_settings["Database"]["Connection"] = CUSTOM_CONFIGURATION[
    "dawnlit_database_connection"
]
write_json(os.path.join(BASE_PATH, "DawnLitWeb", "appsettings.json"), app_settings)

# build back-end application
execute_sudo_docker("build", ".", "-t", "dotnet-app")
# run back-end application
execute_sudo_docker(
    "run", "--name", "dotnet-app", "-d", "-p", "7061:8080", "dotnet-app"
)

# build front-end application
execute_sudo_docker("build", "./View/", "-t", "angular-app")
# run front-end application
execute_sudo_docker(
    "run", "--name", "angular-app", "-d", "-p", "4200:80", "angular-app"
)

# setup nginx
shutil.copy2("./nginx.conf", "/etc/nginx/conf.d/default.conf")
# make sure ssl dir exits
os.makedirs("/etc/ssl", exist_ok=True)
# copy dns certificate
shutil.copy2("./ssl/cert.pem", "/etc/ssl/cert.pem")
# copy dns key
shutil.copy2("./ssl/key.pem", "/etc/ssl/key.pem")
# restart nginx service
check_call(["sudo", "service", "nginx", "restart"])
