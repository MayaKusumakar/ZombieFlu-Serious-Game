from enum import IntEnum


class PLAY_TYPE(IntEnum):
    HUMAN = 0
    MACHINE = 1

    @staticmethod
    def print():
        for play_type in PLAY_TYPE:
            print('{0} -> {1}'.format(play_type.value, play_type.name))
