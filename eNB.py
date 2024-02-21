import math
import random

import numpy.random

import environment
import utils
import utils.misc

# random.seed(42)
numpy.random.seed(42)


class eNB:
    """
    This class defines properties of a base station.
    It has a location, id, type and wavelength.
    """

    def __init__(self, x, bs_type):
        self.id = random.randint(0, 1000)
        self.location = x
        self.bs_type = bs_type  # "nr" or "lte"
        if self.bs_type == "nr":
            self.wavelength = utils.misc.freq_to_wavelength(environment.FREQ_NR)
        elif self.bs_type == "lte":
            self.wavelength = utils.misc.freq_to_wavelength(environment.FREQ_LTE)

    def __str__(self):
        return "eNB located at %s of type: %s" % (self.location, self.bs_type)

    def get_location(self):
        return self.location

    def get_id(self):
        return self.id

    def get_type(self):
        return self.bs_type

    def set_location(self, x):
        self.location = x

    def calc_RSRP(self, ueLocation: int):
        """
        This function calculates the Received Signal Strength of the base station in dB
        This value is calculated using the Friis equation, i.e. RSS = Ptx - Gtx - Grx - L
        :param ueLocation: Location of the UE
        :return: RSRP(Reference Signal Received Power ) in dBm

        Here it is assumed that Gtx = Grx = 0 dB (Gains of the transmitter and receiver)
        """

        pt = utils.misc.calc_power_in_dbm(environment.PTX)
        if self.location != ueLocation:
            x = numpy.random.normal(0, 1)
            y = numpy.random.normal(0, 1)
            # make a complex number using the two random numbers

            # N = 1
            # K_dB = 3  # K factor in dB
            # K = 10 ** (K_dB / 10)  # K factor in linear scale
            # mu = math.sqrt(K / (2 * (K + 1)))  # mean
            # sigma = math.sqrt(1 / (2 * (K + 1)))  # sigma
            # z = (sigma * standard_normal(N) + mu) + 1j * (sigma * standard_normal(N) + mu)

            z = complex(x, y)
            # calculate the path loss using environment.PTX and distance between the base station and UE
            pl = (4 * math.pi * math.fabs(self.location - ueLocation) / self.wavelength)
            # print("Path Loss: %s" % pl)
            # calculate the shadowing using the path loss and the complex number
            fading = pl * z
            #  find square of the magnitude of the complex number
            fading = abs(fading) ** 2
            # print("Shadowing: %s" % fading)

            pr = environment.PTX * fading

            rsrp = pt - (20 * math.log10(pl))
            # print("RSRP: %s" % rsrp)
        else:
            rsrp = 0
        # print("ID: %s, Location: %s, RSRP: %s" % (self.id, self.location, rsrp))
        return rsrp

    def get_bandwidth(self):
        """
        This function returns the bandwidth of the base station
        :return: Bandwidth of the base station
        """
        if self.bs_type == "nr":
            return environment.BANDWIDTH_NR
        elif self.bs_type == "lte":
            return environment.BANDWIDTH_LTE
