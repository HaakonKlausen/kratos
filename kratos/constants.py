from enum import Enum 


#1828820	Vaskerom_VVBereder	ON

#11290966	Hyttebad_Varmekabel	OFF
#11284748	Hyttebad_VVBereder	OFF
#11020052	Ovn_Bad	ON

#11290926	Ovn_Peis


OdderheiHotwater = '1828820'
BjonntjonnHotwater = '11284748'
BjonntjonnKitchenInTemp = '1554261662'
OdderheiKitchenInTemp = '1548595445'
BjonntjonnBadTemp = '1554261848'
BjonntjonnOvnGang = '11290926'
BjonntjonnOvnBod = '11290951'
BjonntjonnOvnKjokken = '12103291'
BjonntjonnOvnPeis = '11290926'
BjonntjonnKjokkenskap = '1556983303'
BjonntjonnKjokkenskapOvn = '11417057'
BjonntjonnVarmekabelVann = '11290966'
BjonntjonnOutTemp = '1555014559'

EOL = -273

class State(Enum):
    AllwaysOff = 0
    Optimze = 1
    AllwaysOn = 2

class Power(Enum):
    Off = 0
    On = 1