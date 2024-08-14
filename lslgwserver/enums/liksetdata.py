from enum import IntEnum


# https://wiki.secondlife.com/wiki/Linkset_data
class Action(IntEnum):
    RESET = 0  #       The linkset's datastore has been cleared
    UPDATE = 1  #      A key in the linkset's datastore has been assigned a new value
    DELETE = 2  #      A key in the linkset's datastore has been deleted
    MULTIDELETE = 3  # A comma separated list of deleted keys
