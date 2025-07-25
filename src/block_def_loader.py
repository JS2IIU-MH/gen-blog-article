import yaml

def load_block_defs(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)
