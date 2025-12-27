import yaml
import os
from cryptography.fernet import Fernet
from default import BASE_DIR

setup_file = BASE_DIR / "setup.yaml"

def setup():
    if not os.path.exists(setup_file):
        data = {"setup": {"bot_token": "your bot token", "guild_id": "your guild id", "encryption_key": Fernet.generate_key().decode("utf8")}}
        yaml.dump(data, open(setup_file, "w"))
    

def get_guild_id():
    data = yaml.load(
        setup_file.read_text(encoding="utf-8"),
        Loader=yaml.FullLoader
    )
    return int(data["setup"]["guild_id"])


def get_bot_token():
    data = yaml.load(
        setup_file.read_text(encoding="utf-8"),
        Loader=yaml.FullLoader
    )
    return data["setup"]["bot_token"]


def get_encryption_key():
    data = yaml.load(
        setup_file.read_text(encoding="utf-8"),
        Loader=yaml.FullLoader
    )
    return data["setup"]["encryption_key"].encode("utf8")
    

def set_encryption_key():

    with open(setup_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        data["setup"]["encryption_key"] = Fernet.generate_key().decode("utf8")
    with open(setup_file, "w") as f:
        yaml.dump(data, f)
    return True
    
def set_guild_id(new_guild_id:int):
    with open(setup_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        data["setup"]["guild_id"] = int(new_guild_id)
    with open(setup_file, "w") as f:
        yaml.dump(data, f)
    return True

def set_bot_token(new_token:str):
    with open(setup_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        data["setup"]["bot_token"] = new_token
    with open(setup_file, "w") as f:
        yaml.dump(data, f)
    return True

if __name__ == "__main__":
    setup()