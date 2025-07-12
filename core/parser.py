# core/parser.py
import yaml

def load_yaml_config(filepath):
    """
    Load YAML config file and return dict.
    """
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    # Optional: validate keys
    expected_keys = ['repos', 'topics', 'tags', 'labels', 'ownership']
    for key in expected_keys:
        if key not in config:
            config[key] = None  # default to None if missing

    return config
