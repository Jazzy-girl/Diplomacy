from enum import Enum


class UnitTypes(Enum):
    TROOP = 0
    FLEET = 1

    def __str__(self):
        return self.name


class Unit:
    unit_type = None
    """ UnitType """

    position = None
    """ String -- Name of occupied territory """

    def __init__(self, unit_type, position):
        self.unit_type = unit_type
        self.position = position

    def __eq__(self, other):
        return self.unit_type == other.unit_type and self.position == other.position

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.unit_type, self.position))

    def __repr__(self):
        return '[{} -- {}]'.format(self.unit_type, self.position)
