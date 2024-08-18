import yaml

def load_config():
    with open('./config/config.yaml') as f:
        return yaml.safe_load(f)
    
config = load_config()

DETECTOR_CONFIG = config['detector']