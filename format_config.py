from glob import glob

from utils import BASE_PATH, CUSTOM_CONFIGURATION_PATH, os, read_config, write_config

# format all yml file
for path in glob(os.path.join(BASE_PATH, "*.yml")):
    write_config(path, read_config(path))

# format all json file
for path in glob(os.path.join(BASE_PATH, "*.json")):
    write_config(path, read_config(path))

# format config
write_config(CUSTOM_CONFIGURATION_PATH, read_config(CUSTOM_CONFIGURATION_PATH))
