from Simulator import Simulator
from UE import UE
from environment import eNBs


def main():
    # Define the UEs
    u1 = UE(12000)
    u2 = UE(20000)
    u3 = UE(30000)
    u4 = UE(40000)
    UEs = [u1, u2, u3, u4]

    S = Simulator(eNBs, UEs)
    S.run()


main()
