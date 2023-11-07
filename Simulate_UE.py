import math
from typing import List

import environment
from eNB import eNB
from UE import UE
from utils.Ticker import Ticker


class Simulate_UE:
    """This class defines an environment for the simulator"""

    def __init__(self, ue: UE, e_nbs: List[eNB]):
        self.Ticker = Ticker()
        self.ue = ue
        self.e_nbs = e_nbs
        self.ho_active = False
        self.ho_trigger_time = -1
        self.readings = 0
        self.throughput_aggregate = 0
        self.throughput = []
        self.totalHO = 0
        self.totalRLF = 0

    def run(self, t: Ticker, time=10000000):
        self.Ticker = t
        self.discover_bs()
        self.associate_ue_with_bs()
        self.simulate_motion_with_states(time, environment.TPREP)
        # return Result(result[0], result[1], timeOfExecution=time, throughput_avg=result[2])

    def simulate_motion_with_states(self, time=100000, tprep=2000):
        currentHOState = 0
        failedHO = 0
        prevHOF = False
        prevRLF = False
        resultRLF = 0
        success = 0
        totalCount = 0
        # create a list of states with time/200 number of states all set to zero
        pStates = [0] * int(tprep / 200)
        eStates = [0] * int(tprep / 200)
        rlfPStates = [0] * int(tprep / 200)
        rlfEStates = [0] * int(tprep / 200)
        prepComplete = False

        while self.Ticker.time < time:
            totalCount += 1

            if currentHOState == len(pStates) - 1:
                success += 1
                currentHOState = 0
                self.ho_active = False
            if self.ho_active is True or (
                (self.ho_active is False) and (self.check_for_new_handover())
            ):
                if (
                    self.ue.get_upcoming_eNB().calc_RSRP(self.ue.get_location())
                    >= self.ue.get_eNB().calc_RSRP(self.ue.get_location())
                    + environment.HYSTERESIS
                    + environment.A3_OFFSET
                ):
                    pStates[currentHOState] += 1
                    currentHOState += 1
                    prevHOF = False

                else:
                    if prevHOF is False:
                        failedHO = 0

                    failedHO += 1
                    if failedHO >= 3:
                        failedHO = 0
                        self.ho_active = False
                        currentHOState = 0
                        continue
                    else:
                        prevHOF = True
                        pStates[currentHOState] += 1
                        currentHOState += 1

                if (
                    self.ue.get_eNB().calc_RSRP(self.ue.get_location())
                    < environment.RLF_THRESHOLD
                ):
                    resultRLF += 1
                    if resultRLF >= 3 and prevRLF is True:
                        rlfPStates[currentHOState] += 1
                        resultRLF = 0
                        self.totalRLF += 1
                        self.ho_active = False
                        self.ue.set_upcoming_eNB(None)
                        self.associate_ue_with_bs()
                        currentHOState = 0
                        continue
                    else:
                        if prevRLF is False:
                            resultRLF = 1
                        prevRLF = True
                else:
                    prevRLF = False
                    resultRLF = 0

            self.ue.update_UE_location(self.Ticker)

        print("Total Handover triggers:", self.totalHO)
        print("Total Handover transitions at each state:", pStates)
        print("Probability of successful transition at state: [", end="")
        for i in range(len(pStates)):
            print(round(pStates[i] / self.totalHO, 3), end=",")
        print("\b]")
        print("Total Radio Link Failures:", self.totalRLF)
        print("Total Radio Link Failures on each state:", rlfPStates)

    def search_for_bs(self):
        nearby_bs = []
        for e_nb in self.e_nbs:
            dist = math.fabs(self.ue.get_location() - e_nb.get_location())
            if dist <= 20000:
                nearby_bs.append(e_nb)
        return nearby_bs

    def associate_ue_with_bs(self):
        """
        This function associates the UE with the base station, it also checks if the UE is in range of the base station,
        if it is then it keeps a record of the eNB in the list of eNBs
        """
        nearby_bs = self.search_for_bs()
        if len(nearby_bs) == 0:
            print("UE %s is out of range" % self.ue.get_location())
            return Exception("UE is out of range")
        sorted_nearby_bs = sorted(
            nearby_bs, key=lambda x: x.calc_RSRP(self.ue.get_location()), reverse=True
        )
        # TODO: add a minimum RSRP threshold to consider
        # print sorted_nearby_bs with their RSRP
        self.ue.set_eNB(sorted_nearby_bs[0])
        self.ue.set_nearby_bs(nearby_bs)

    def trigger_motion(self, time=1000000):
        while self.Ticker.time < time:
            if self.ho_active is True:
                self.check_handover_completion()
            self.ue.update_UE_location(self.Ticker)
            self.check_for_new_handover()
        print(
            "Successful HOs [lte2lte, lte2nr, nr2lte, nr2nr]: %s"
            % self.ue.get_HO_success()
        )
        print(
            "Failed HOs [lte2lte, lte2nr, nr2lte, nr2nr]: %s" % self.ue.get_HO_failure()
        )
        return [
            self.ue.get_HO_success(),
            self.ue.get_HO_failure(),
            self.throughput_aggregate / self.readings,
        ]

    def check_for_new_handover(self):
        """
        Handover occurs when the UE is in area of another base station with higher RSRP for TTT
        """
        nearby_bs = self.ue.get_nearby_bs()
        if len(nearby_bs) == 0:
            self.ue.set_HO_failure(2)
            print("UE %s is out of range" % self.ue.get_location())
        else:
            source_rsrp = self.ue.get_eNB().calc_RSRP(self.ue.get_location())
            for e_nb in nearby_bs:
                if e_nb.get_id() != self.ue.get_eNB().get_id():
                    target_rsrp = e_nb.calc_RSRP(self.ue.get_location())
                    if target_rsrp > source_rsrp + environment.HYSTERESIS:
                        # if self.ho_active is False:
                        self.totalHO += 1
                        self.ho_active = True
                        self.ho_trigger_time = self.Ticker.time
                        self.ue.set_upcoming_eNB(e_nb)
                        return True
            else:
                return False

                # print("UE %s is in area of eNB %s" % (ue.get_id(), e_nb.get_id()))

            # # Average throughput calculation
            # self.readings += 1
            # sinr = calc_power_in_mw(source_rsrp) / self.interference
            # throughput = calc_throughput(sinr, self.ue.associated_eNB.get_bandwidth())
            # if self.ho_active is True:
            #     throughput = 0
            # self.throughput_aggregate += throughput
            # self.throughput.append(throughput)

    def check_handover_completion(self):
        if self.Ticker.time - self.ho_trigger_time >= environment.TTT:
            if (
                self.ue.get_upcoming_eNB().calc_RSRP(self.ue.get_location())
                >= self.ue.get_eNB().calc_RSRP(self.ue.get_location())
                + environment.HYSTERESIS
                + environment.A3_OFFSET
            ):
                self.ho_active = False
                self.ue.set_HO_success(self.ue.get_handover_type())
                self.ue.set_eNB(self.ue.get_upcoming_eNB())
                # print("UE %s is connected to eNB %s" % (self.ue.get_id(), self.ue.get_eNB().get_id()))
            else:
                self.ue.set_HO_failure(self.ue.get_handover_type())
                self.ho_active = False
            self.ue.set_upcoming_eNB(None)
            self.ho_trigger_time = -1
            self.associate_ue_with_bs()
        else:
            return

    def discover_bs(self):
        self.e_nbs.sort(key=lambda x: x.get_location())
