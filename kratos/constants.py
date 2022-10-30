from enum import Enum 


#1828820	Vaskerom_VVBereder	ON

#11290966	Hyttebad_Varmekabel	OFF
#11284748	Hyttebad_VVBereder	OFF
#11020052	Ovn_Bad	ON
#11290951	Ovn_Kjøkken	ON
#11290926	Ovn_Peis


OdderheiHotwater = '1828820'
BjonntjonnHotwater = '11284748'
BjonntjonnKitchenInTemp = '1554261662'
OdderheiKitchenInTemp = '1548595445'
BjonntjonnBadTemp = '1554261848'
BjonntjonnOvnBad = '11020052'
BjonntjonnOvnKjokken = '11290951'
BjonntjonnOvnPeis = '11290926'

EOL = -273

class State(Enum):
    AllwaysOff = 0
    Optimze = 1
    AllwaysOn = 2

class Power(Enum):
    Off = 0
    On = 1