from enum import IntEnum
import random
import warnings


class DEPLOYMENTS(IntEnum):
    NONE = 0
    QUARANTINE_OPEN = 1
    QUARANTINE_FENCED = 2
    BITE_CENTER_DISINFECT = 3
    BITE_CENTER_AMPUTATE = 4
    Z_CURE_CENTER_FDA = 5
    Z_CURE_CENTER_EXP = 6
    FLU_VACCINE_OPT = 7
    FLU_VACCINE_MAN = 8
    KILN_OVERSIGHT = 9
    KILN_NO_QUESTIONS = 10
    BROADCAST_DONT_PANIC = 11
    BROADCAST_CALL_TO_ARMS = 12
    SNIPER_TOWER_CONFIRM = 13
    SNIPER_TOWER_FREE = 14
    PHEROMONES_BRAINS = 15
    PHEROMONES_MEAT = 16
    BSL4LAB_SAFETY_ON = 17
    BSL4LAB_SAFETY_OFF = 18
    RALLY_POINT_OPT = 19
    RALLY_POINT_FULL = 20
    FIREBOMB_PRIMED = 21
    FIREBOMB_BARRAGE = 22
    SOCIAL_DISTANCING_SIGNS = 23
    SOCIAL_DISTANCING_CELEBRITY = 24
    # Added deployments
    TESTING_CENTER_OPT = 25
    TESTING_CENTER_MAN = 26
    SUPPLY_DEPOT = 27
    FACTORY = 28
    VOLUNTEER_RECRUITMENT = 29

    @staticmethod
    def print():
        for deployment in DEPLOYMENTS:
            print('{0} -> {1}'.format(deployment.value, deployment.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(DEPLOYMENTS))


    @staticmethod
    def get_value_from_string(deployment):
        for dep in DEPLOYMENTS:
            if deployment.upper() == dep.name:
                return dep.value
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.value

    @staticmethod
    def get_name_from_string(deployment):
        for dep in DEPLOYMENTS:
            if deployment.upper() == dep.name:
                return dep.name
        else:
            warnings.warn('Tried to convert string ({}) to DEPLOYMENTS enum and failed; returned NONE'.format(deployment))
            return DEPLOYMENTS.NONE.name

class LOCATIONS(IntEnum):
    CENTER = 0
    N = 1
    S = 2
    E = 3
    W = 4
    NE = 5
    NW = 6
    SE = 7
    SW = 8

    @staticmethod
    def print():
        for location in LOCATIONS:
            print('{0} -> {1}'.format(location.value, location.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(LOCATIONS))

    @staticmethod
    def get_value_from_string(location):
        for loc in LOCATIONS:
            if location.upper() == loc.name:
                return loc.value
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.value

    @staticmethod
    def get_name_from_string(location):
        for loc in LOCATIONS:
            if location.upper() == loc.name:
                return loc.name
        else:
            warnings.warn('Tried to convert string ({}) to LOCATION enum and failed; returned CENTER'.format(location))
            return LOCATIONS.CENTER.name