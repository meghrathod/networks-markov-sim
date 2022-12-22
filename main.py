from Simulate_UE import Simulate_UE
from UE import UE
from environment import eNBs
from utils import graph_rsrp


def main():
    # Define the UEs
    u1 = UE(12000)

    # seed(42)
    graph_rsrp(eNBs)
    S = Simulate_UE(u1, eNBs)
    S.run(time=1000000)


main()
