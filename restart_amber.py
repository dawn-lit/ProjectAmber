from utils import check_call, execute_sudo_docker

# run docker-compose
try:
    check_call(["sudo", "docker-compose", "up", "-d", "gitlab_web", "postgres_db"])
except Exception:
    pass

# restart back-end application
try:
    execute_sudo_docker("restart", "dotnet-app")
except Exception:
    pass

# restart front-end application
try:
    execute_sudo_docker("restart", "angular-app")
except Exception:
    pass

# restart coder
try:
    execute_sudo_docker("restart", "/code-server")
except Exception:
    pass
