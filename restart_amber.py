from utils import execute_docker, get_all_docker_containers

# sudo chmod -R 777 /var/run/docker.sock

# restart all docker containers
for container_id in get_all_docker_containers():
    try:
        print(f"Restarting docker container {container_id}...")
        execute_docker("restart", container_id)
    except Exception:
        print(f"Fail to restart docker container {container_id}, skip...")
