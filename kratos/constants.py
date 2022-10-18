from enum import Enum 

class State(Enum):
    AllwaysOff = 0
    Optimze = 1
    AllwaysOn = 2

class Power(Enum):
    Off = 0
    On = 1