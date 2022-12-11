import math
from random import seed

seed(42)


class Simulator:
    """This class defines an environment for the simulator"""

    def __init__(self, e_nbs, UEs):
        self.e_nbs = e_nbs
        self.UEs = UEs
        self.time = 0
        # Scale of the ticker
        # 1 tick = 1 ms
        self.UEs_in_range = []
        self.UEs_out_of_range = []

    def run(self):
        self.discover_bs()
        self.associate_ue_with_bs()

    def associate_ue_with_bs(self):
        """
        This function associates the UE with the base station, it also checks if the UE is in range of the base station,
        if it is then it keeps a record of the eNB in the list of eNBs
        """
        for ue in self.UEs:
            nearby_bs = []
            for e_nb in self.e_nbs:
                dist = math.fabs(ue.get_location() - e_nb.get_location())
                # TODO: finalise the distance to consider,
                #  at this distance the UE can connect to the eNB and be able a decode signal

                # TODO: This algorithm can be improved but for now it works
                if dist <= 20000:
                    nearby_bs.append(e_nb)
            if len(nearby_bs) == 0:
                self.UEs_out_of_range.append(ue)
                print("UE %s is out of range" % ue.get_location())
            else:
                nearest_bs = min(
                    nearby_bs,
                    key=lambda x: math.fabs(ue.get_location() - x.get_location(
                    )),
                )
                # TODO: add a minimum RSS threshold to consider
                ue.set_eNB(nearest_bs)
                ue.set_nearby_bs(nearby_bs)
                print("UE %s is connected to eNB %s" %
                      (ue.get_id(), ue.get_eNB().get_id()))

    def discover_bs(self):
        self.e_nbs.sort(key=lambda x: x.get_location())

    def start_motion(self, constant, time):
        while self.time < time:
            for ue in self.UEs:
                ue.generate_random_motion(constant)
                self.time += 1

        print(self.time)
