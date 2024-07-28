from utils import *

# remove old ollama container
stop_docker_container("ollama")
remove_docker_container("ollama")

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
    "ollama/ollama",
)

# using llama3.1 model
execute_docker(
    "exec",
    "-it",
    "ollama",
    "ollama",
    "run",
    "llama3.1",
)
