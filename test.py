import random

import eNB_environments
from UE import UE
from utils.Ticker import Ticker
from utils.grapher import graph_rsrp

u1 = UE(random.randint(0, 50000))
enbs = eNB_environments.eNBs_mix1
ticker = Ticker()
# seed(42)
graph_rsrp(enbs)
# S = Simulate_UE(u1, enbs[1])
# res = S.run(ticker, time=10000000)
# Result.save_to_file(res, "results_with_TH.xlsx", enbs[0])
