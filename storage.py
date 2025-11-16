import os
import json
import tempfile
import shutil
from rkgparser import RKG

CONFIG_PATH = "config.json"
EXAMPLE_PATH = "config.example.json"
GHOSTS_DIR = "./ghosts/"

REQUIRED_KEYS = [
    "challenge_num",
    "challenge_channel",
    "challenge_staff_role",
    "submit_channel"
]

def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"{CONFIG_PATH} not found.\n"
            f"Please copy {EXAMPLE_PATH} to {CONFIG_PATH} and fill in ALL required keys:\n"
            f"{REQUIRED_KEYS}"
        )
    
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing {CONFIG_PATH}: {e}")

    missing = [key for key in REQUIRED_KEYS if key not in config]
    if missing:
        raise KeyError(
            f"{CONFIG_PATH} is missing required keys: {missing}\n"
            f"Please add them manually based on {EXAMPLE_PATH}."
        )

    return config

def save_config(config: dict):
    # Safely save the configuration via temp files to avoid corruption
    dir_name = os.path.dirname(CONFIG_PATH) or "."
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name) as temp_file:
        json.dump(config, temp_file, indent=4)
        temp_file.flush()
        temp_path = temp_file.name

    shutil.move(temp_path, CONFIG_PATH)

def load_chal_num() -> int:
    return int(load_config()["challenge_num"])

def save_chal_num(num: int):
    config = load_config()
    config["challenge_num"] = num
    save_config(config)

def load_challenge_channel() -> int:
    return int(load_config()["challenge_channel"])

def load_challenge_staff_role() -> int:
    return int(load_config()["challenge_staff_role"])

def load_submit_channel() -> int:
    return int(load_config()["submit_channel"])

def submit_time(filename: str, data: bytes) -> str:
    if not os.path.exists(GHOSTS_DIR):
        os.makedirs(GHOSTS_DIR)

    ghost_path = os.path.join(GHOSTS_DIR, filename)

    with open(ghost_path, "wb") as f:
        f.write(data)

    rkg = RKG(data)
    rkg.skip_bits(4 * 8)
    minutes = rkg.read_bits(7)
    seconds = rkg.read_bits(7)
    milliseconds = rkg.read_bits(10)

    return f"{minutes}:{seconds}.{milliseconds}"
