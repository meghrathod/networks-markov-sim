import math
from random import seed
from typing import List

import environment
from UE import UE
from eNB import eNB
from utils import Ticker

seed(42)


class Simulator:
    """This class defines an environment for the simulator"""

    def __init__(self, ue: UE, e_nbs: List[eNB]):
        self.Ticker = Ticker()
        self.ue = ue
        self.e_nbs = e_nbs
        self.ho_active = False
        self.ho_trigger_time = -1

    def run(self, time=10000):
        self.discover_bs()
        self.associate_ue_with_bs(self.ue)
        self.trigger_motion(self.ue, time)

    def search_for_bs(self, ue: UE):
        nearby_bs = []
        for e_nb in self.e_nbs:
            dist = math.fabs(ue.get_location() - e_nb.get_location())
            # TODO: finalise the distance to consider,
            #  at this distance the UE can connect to the eNB and be able a decode signal
            if dist <= 20000:
                nearby_bs.append(e_nb)
        return nearby_bs

    def associate_ue_with_bs(self, ue: UE):
        """
        This function associates the UE with the base station, it also checks if the UE is in range of the base station,
        if it is then it keeps a record of the eNB in the list of eNBs
        """
        nearby_bs = self.search_for_bs(ue)
        if len(nearby_bs) == 0:
            print("UE %s is out of range" % ue.get_location())
            return Exception("UE is out of range")
        else:
            sorted_nearby_bs = sorted(
                nearby_bs,
                key=lambda x: math.fabs(ue.get_location() - x.get_location()),
            )
            # TODO: add a minimum RSRP threshold to consider
            ue.set_eNB(sorted_nearby_bs[0])
            ue.set_nearby_bs(nearby_bs)
            print("UE %s is connected to eNB %s" %
                  (ue.get_id(), ue.get_eNB().get_id()))

    def trigger_motion(self, ue: UE, time=1000000):
        while self.Ticker.time < time:
            if self.ho_active is True:
                self.check_handover_completion(ue)
            ue.update_UE_location(self.Ticker)
            self.check_for_handover(ue)

    def check_handover_completion(self, ue: UE):
        if self.Ticker.time - self.ho_trigger_time >= environment.TTT:
            if ue.get_upcoming_eNB().calc_RSRP(ue.get_location()) >= \
                    ue.get_eNB().calc_RSRP(ue.get_location() + environment.HYSTERESIS):
                self.ho_active = False
                ue.set_eNB(ue.get_upcoming_eNB())
                print("UE %s is connected to eNB %s" % (ue.get_id(), ue.get_eNB().get_id()))
            else:
                ue.set_HO_failure()
                self.ho_active = False
            ue.set_upcoming_eNB(None)
            self.ho_trigger_time = -1
            self.associate_ue_with_bs(ue)
        else:
            return

    def check_for_handover(self, ue: UE):
        """
        Handover occurs when the UE is in area of another base station with higher RSRP for TTT
        """
        # TODO: Fix handover
        nearby_bs = ue.get_nearby_bs()
        if len(nearby_bs) == 0:
            ue.set_HO_failure()
            print("UE %s is out of range" % ue.get_location())
        else:
            for e_nb in nearby_bs:
                if e_nb.get_id() != ue.get_eNB().get_id():
                    if e_nb.calc_RSRP(ue.get_location()) > \
                            ue.get_eNB().calc_RSRP(ue.get_location() + environment.HYSTERESIS):
                        self.ho_active = True
                        self.ho_trigger_time = self.Ticker.time
                        ue.set_upcoming_eNB(e_nb)
                        print("UE %s is in area of eNB %s" % (ue.get_id(), e_nb.get_id()))

    def discover_bs(self):
        self.e_nbs.sort(key=lambda x: x.get_location())
