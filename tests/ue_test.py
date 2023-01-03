import UE
from utils.Ticker import Ticker

t = Ticker()
ue = UE.UE(0)
while t.time < 100000:
    ue.update_UE_location(t)
print(ue.get_location())
