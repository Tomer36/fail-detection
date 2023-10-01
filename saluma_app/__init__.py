import configparser
import os
config = configparser.ConfigParser()

config_file_path = os.path.abspath("config.ini")

def reload_config(file=config_file_path):
    config.read(file)
    return config

def write_config(file=config_file_path):
    with open(file, 'w') as configfile:
        config.write(configfile)

reload_config()

__all__ = [config, reload_config, write_config, config_file_path]