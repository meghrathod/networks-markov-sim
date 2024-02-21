import math
from typing import List

import environment
from UE import UE
from eNB import eNB
from utils.Ticker import Ticker
from utils.data_processor import createProbabilityMatrix, createCountMatrix


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

    def run(self, t: Ticker, time=10000000, verbose=False):
        # Create an empty 14x14 matrix
        self.Ticker = t
        self.discover_bs()
        self.associate_ue_with_bs()
        probabilityMatrix, count, average, success, latency_array = self.simulate_motion(time, verbose)
        return probabilityMatrix, count, average, success, latency_array

    def simulate_motion(self, time=100000, verbose=False):
        start = self.Ticker.time
        end = 0
        success = 0
        totalCount = 0
        prepComplete = False
        initHiCounter = 0
        handover_check = False
        a3_counter = 0
        currentState = 0
        prepSuccess = [0] * int(environment.TPREP / environment.TICKER_INTERVAL)
        prepFailure = [0] * int(environment.TPREP / environment.TICKER_INTERVAL)
        execSuccess = [0] * int(environment.TEXEC / environment.TICKER_INTERVAL)
        execFailure = [0] * int(environment.TEXEC / environment.TICKER_INTERVAL)
        RLF = [0] * (int(environment.TEXEC / environment.TICKER_INTERVAL) * 2)
        RLF_at_NORM = 0
        a3_required = environment.TTT / environment.TICKER_INTERVAL
        prepFailureCount = 0
        execFailureCount = 0
        latency_sum = 0
        latency_array = []

        while self.Ticker.time < time:
            self.ue.update_UE_location(self.Ticker)
            totalCount += 1  # state 0, the start

            # Check for RLF
            source = self.ue.get_eNB().calc_RSRP(self.ue.get_location())
            threshold = environment.RLF_THRESHOLD
            if source < threshold:
                self.totalRLF += 1
                if self.ho_active is False:
                    RLF_at_NORM += 1
                else:
                    if prepComplete is False:
                        RLF[currentState] += 1
                    else:
                        RLF[currentState + len(prepSuccess) - 2] += 1
                self.ue.set_upcoming_eNB(None)
                handover_check = False
                self.associate_ue_with_bs()
                self.ho_active = False
                continue

            # Check for handover
            if self.ho_active is False:
                if handover_check is False:
                    handover_check = self.check_for_new_handover()
                else:
                    if a3_counter < a3_required:
                        source = self.ue.get_eNB().calc_RSRP(self.ue.get_location())
                        target = self.ue.get_upcoming_eNB().calc_RSRP(
                            self.ue.get_location()) + environment.HYSTERESIS + environment.A3_OFFSET
                        if target > source:
                            a3_counter += 1
                        else:
                            self.ue.set_upcoming_eNB(None)
                            handover_check = False
                            self.ho_active = False
                            a3_counter = 0
                            continue
                    else:
                        self.ho_active = True
                        initHiCounter += 1
                        handover_check = False
                        self.totalHO += 1
                        start = self.Ticker.time

            else:
                # Check for prep state

                if prepComplete is False:
                    if currentState == len(prepSuccess):
                        currentState = 0
                        prepComplete = True
                        continue
                    if self.ue.get_upcoming_eNB().calc_RSRP(self.ue.get_location()) >= \
                            self.ue.get_eNB().calc_RSRP(
                                self.ue.get_location()) + environment.PREP_THRESHOLD:
                        prepSuccess[currentState] += 1
                        currentState += 1
                    else:
                        # if prepFailureCount < 3:
                        #     prepFailureCount += 1
                        #     continue
                        # else:
                        #     prepFailureCount = 0
                        prepFailure[currentState] += 1
                        currentState = 0
                        continue
                else:
                    # Check for exec state

                    if currentState == len(execSuccess):
                        currentState = 0
                        prepComplete = False
                        success += 1
                        self.ho_active = False
                        end = self.Ticker.time
                        latency_sum += end - start
                        latency_array.append(end - start)
                        self.ue.set_eNB(self.ue.get_upcoming_eNB())
                        self.ue.set_upcoming_eNB(None)
                        continue

                    if self.ue.get_upcoming_eNB().calc_RSRP(self.ue.get_location()) >= \
                            self.ue.get_eNB().calc_RSRP(
                                self.ue.get_location()) + environment.EXEC_THRESHOLD:
                        execSuccess[currentState] += 1
                        currentState += 1
                    else:
                        # if execFailureCount < 3:
                        #     execFailureCount += 1
                        #     continue
                        # else:
                        #     execFailureCount = 0
                        execFailure[currentState] += 1
                        currentState = 0
                        continue

        if verbose:
            print("Total ticks", totalCount)
            print("Total Handover triggers:", initHiCounter)
            print("Total Handover transitions at each prep state:", prepSuccess)
            print("Total Handover Termination at each prep state:", prepFailure)
            print("Total Handover transitions at each execution state:", execSuccess)
            print("Total Handover Termination at each execution state:", execFailure)
            print("Total Radio Link Failures:", self.totalRLF)
            print("Total Radio Link Failures at each state:", RLF)
            print("Total Radio Link Failures at each state when in normal state:", RLF_at_NORM)
            print("Total Successful Handovers:", success)

        countMatrix = createCountMatrix(initHiCounter, prepSuccess, prepFailure, execSuccess, execFailure,
                                        RLF_at_NORM, RLF, success)

        probabilityMatrix = createProbabilityMatrix(countMatrix)
        if success == 0:
            return probabilityMatrix, countMatrix, 0, 0, []
        else:
            return probabilityMatrix, countMatrix, latency_sum / success, success, latency_array

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
        sorted_nearby_bs = sorted(nearby_bs, key=lambda x: x.calc_RSRP(self.ue.get_location()), reverse=True)
        # TODO: add a minimum RSRP threshold to consider
        # print sorted_nearby_bs with their RSRP
        self.ue.set_eNB(sorted_nearby_bs[0])
        self.ue.set_nearby_bs(nearby_bs)

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

    def discover_bs(self):
        self.e_nbs.sort(key=lambda x: x.get_location())
