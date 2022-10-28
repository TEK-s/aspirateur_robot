class Room:

    def __init__(self):
        self.has_jewel = False
        self.has_dust = False

    def add_jewel(self) -> None:
        self.has_jewel = True

    def add_dust(self) -> None:
        self.has_dust = True

    def reset(self) -> None:
        self.has_jewel = False
        self.has_dust = False

    def has_thing(self) -> bool:
        return self.has_dust or self.has_jewel

    def print(self) -> None:
        if self.has_jewel and self.has_dust:
            value = '\033[91m%\033[00m'
        elif self.has_jewel:
            value = '\033[96m¤\033[00m'
        elif self.has_dust:
            value = '\033[97m~\033[00m'
        else:
            value = ' '

        print(value, end='')
