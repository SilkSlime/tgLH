import os
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config.yaml'

def load_config():
    """Load configuration from YAML file and environment variables."""
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)

    # Overwrite with environment variables if they are set
    config['DOWNLOAD_PATH'] = os.getenv('DOWNLOAD_PATH', config['DOWNLOAD_PATH'])
    config['DOWNLOAD_TIMEOUT'] = int(os.getenv('DOWNLOAD_TIMEOUT', config['DOWNLOAD_TIMEOUT']))
    config['TOKEN'] = os.getenv('TOKEN', config['TOKEN'])

    return config

config = load_config()
