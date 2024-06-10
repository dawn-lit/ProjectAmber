from typing import Final

from utils import *

# base path
BASE_PATH: Final[str] = os.path.dirname(__file__)

# user customized configuration
CUSTOM_CONFIGURATION_PATH: Final[str] = os.path.join(BASE_PATH, "configuration.json")
CUSTOM_CONFIGURATION: Final[dict] = read_config(CUSTOM_CONFIGURATION_PATH)

_ENABLE_CUSTOM_CONFIGURATION_VALIDATION: bool = True

if _ENABLE_CUSTOM_CONFIGURATION_VALIDATION:
    if len(CUSTOM_CONFIGURATION["password"]) == 0:
        raise ValueError(
            "configuration.json: password has not being configured correctly!"
        )

    if len(CUSTOM_CONFIGURATION["username"]) == 0:
        raise ValueError(
            "configuration.json: username has not being configured correctly!"
        )

    # make sure ssl key is valid
    if len(CUSTOM_CONFIGURATION["ssl_key"]) == 0:
        raise ValueError(
            "configuration.json: ssl_key has not being configured correctly!"
        )

    # make sure ssl cert is valid
    if len(CUSTOM_CONFIGURATION["ssl_cert"]) == 0:
        raise ValueError(
            "configuration.json: ssl_cert has not being configured correctly!"
        )

    # make domain is valid
    if len(CUSTOM_CONFIGURATION["domain"]) == "example.com":
        raise ValueError(
            "configuration.json: domain has not being configured correctly!"
        )

# path to locally shared folder
SHARE_FOLDER_DIR: Final[str] = os.path.join(
    "/home", CUSTOM_CONFIGURATION["username"], CUSTOM_CONFIGURATION["SharedFolderName"]
)

# update domain in files
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "nginx.glob.conf"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "services", "nginx.glob.conf"),
)
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "nginx.dawnlit.prod.conf"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "services", "nginx.dawnlit.prod.conf"),
)
replace_content_in_file(
    os.path.join(BASE_PATH, "services_templates", "docker-compose.yml"),
    "example.com",
    CUSTOM_CONFIGURATION["domain"],
    os.path.join(BASE_PATH, "docker-compose.yml"),
)

# update postgres_db config username and password
dk_compose: dict = read_config(os.path.join(BASE_PATH, "docker-compose.yml"))
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_DB"] = (
    CUSTOM_CONFIGURATION["postgres_db_name"]
)
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_USER"] = (
    CUSTOM_CONFIGURATION["postgres_db_username"]
)
dk_compose["services"]["postgres_db"]["environment"]["POSTGRES_PASSWORD"] = (
    CUSTOM_CONFIGURATION["postgres_db_password"]
)
write_config(os.path.join(BASE_PATH, "docker-compose.yml"), dk_compose)
