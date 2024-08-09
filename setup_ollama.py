from utils import *

# remove old ollama container
remove_docker_container("ollama")

# pull latest image
pull_docker_base_image("ollama/ollama:latest")

# run ollama container - cpu mode
# https://hub.docker.com/r/ollama/ollama
execute_docker(
    "run",
    "-d",
    "-v",
    "ollama:/root/.ollama",
    "-p",
    "11434:11434",
    "--name",
    "ollama",
    "ollama/ollama:latest",
)

# using llama3.1 model
execute_docker(
    "exec",
    "-it",
    "ollama",
    "ollama",
    "pull",
    "llama3.1",
)
