from rkgparser import RKG
import os
import json

def load_chal_num() -> int:
    try:
        with open("config.json", "r") as f:
            return int(json.load(f)["challenge_num"])
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

def save_chal_num(num: int):
    with open("config.json", "w") as f:
        json.dump({"challenge_num": num}, f)

def save_channel_id(channel_id: int):
    with open("config.json", "w") as f:
        json.dump({"counting_channel": channel_id}, f)

def load_channel_id() -> int:
    try:
        with open("config.json", "r") as f:
            return int(json.load(f)["counting_channel"])
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


GHOSTS_DIR =  "./ghosts/"

def submit_time(filename: str, data: bytes) -> str:

    if not os.path.exists(GHOSTS_DIR):
        os.makedirs(GHOSTS_DIR)
    
    ghost_filename = GHOSTS_DIR + filename

    with open(ghost_filename, "wb") as f:
        f.write(data)

    rkg = RKG(data)
    rkg.skip_bits(4*8)
    minutes = rkg.read_bits(7)
    seconds = rkg.read_bits(7)
    milliseconds = rkg.read_bits(10)
    return f"{minutes}:{seconds}.{milliseconds}"
