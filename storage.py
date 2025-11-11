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
