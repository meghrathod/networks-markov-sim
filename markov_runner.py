import eNB_environments
from Simulate_UE import Simulate_UE
from UE import UE
from utils.Ticker import Ticker

u1 = UE(25000)
print(u1.get_location())
enbs = eNB_environments.eNBs_mix1

s = Simulate_UE(u1, enbs[1])
s.run(Ticker(), 5000000)
