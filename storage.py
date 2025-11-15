import os
from rkgparser import RKG
def load_chal_num() -> int:
    try:
        with open("chal_num", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

def save_chal_num(num: int):
    with open("chal_num", "w") as f:
        f.write(str(num))


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
