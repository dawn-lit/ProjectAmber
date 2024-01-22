from utils import CUSTOM_CONFIGURATION_PATH, read_config, write_config

write_config(CUSTOM_CONFIGURATION_PATH, read_config(CUSTOM_CONFIGURATION_PATH))
