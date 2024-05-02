from utils import check_call, execute_docker

# run docker-compose
try:
    check_call(["sudo", "docker-compose", "up", "-d", "postgres_db", "gitlab_web"])
except Exception:
    pass

# restart back-end application
try:
    execute_docker("restart", "dotnet-app")
except Exception:
    pass

# restart front-end application
try:
    execute_docker("restart", "angular-app")
except Exception:
    pass

# restart coder
try:
    execute_docker("restart", "/code-server")
except Exception:
    pass
