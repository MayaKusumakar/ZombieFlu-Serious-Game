from enum import IntEnum
import random
import warnings


class NPC_STATES_DEAD(IntEnum):
    ALIVE = 0
    DEAD = 1
    ASHEN = 2

    @staticmethod
    def print():
        for state in NPC_STATES_DEAD:
            print('{0} -> {1}'.format(state.value, state.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(NPC_STATES_DEAD))

    @staticmethod
    def get_value_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_DEAD]:
            exec('return NPC_STATES_DEAD.' + state.upper() + '.value')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_DEAD enum and failed; returned ALIVE'.format(state))
            return NPC_STATES_DEAD.ALIVE.value

    @staticmethod
    def get_name_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_DEAD]:
            exec('return NPC_STATES_DEAD.' + state.upper() + '.name')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_DEAD enum and failed; returned ALIVE'.format(state))
            return NPC_STATES_DEAD.ALIVE.name


class NPC_STATES_ZOMBIE(IntEnum):
    HUMAN = 0
    ZOMBIE_BITTEN = 1
    ZOMBIE = 2

    @staticmethod
    def print():
        for state in NPC_STATES_ZOMBIE:
            print('{0} -> {1}'.format(state.value, state.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(NPC_STATES_ZOMBIE))

    @staticmethod
    def get_value_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_ZOMBIE]:
            exec('return NPC_STATES_ZOMBIE.' + state.upper() + '.value')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_ZOMBIE enum and failed; returned HUMAN'.format(state))
            return NPC_STATES_ZOMBIE.HUMAN.value

    @staticmethod
    def get_name_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_ZOMBIE]:
            exec('return NPC_STATES_ZOMBIE.' + state.upper() + '.name')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_ZOMBIE enum and failed; returned HUMAN'.format(state))
            return NPC_STATES_ZOMBIE.HUMAN.name


class NPC_STATES_FLU(IntEnum):
    HEALTHY = 0
    INCUBATING = 1
    FLU = 2
    IMMUNE = 3

    @staticmethod
    def print():
        for state in NPC_STATES_FLU:
            print('{0} -> {1}'.format(state.value, state.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(NPC_STATES_FLU))

    @staticmethod
    def get_value_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_FLU]:
            exec('return NPC_STATES_FLU.' + state.upper() + '.value')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_FLU enum and failed; returned HEALTHY'.format(state))
            return NPC_STATES_FLU.HEALTHY.value

    @staticmethod
    def get_name_from_string(state):
        if state.upper() in [s.name for s in NPC_STATES_FLU]:
            exec('return NPC_STATES_FLU.' + state.upper() + '.name')
        else:
            warnings.warn('Tried to convert string ({}) to NPC_STATES_FLU enum and failed; returned HEALTHY'.format(state))
            return NPC_STATES_FLU.HEALTHY.name
