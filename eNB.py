import math
import random

import environment
from utils import freq_to_wavelength


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
            self.wavelength = freq_to_wavelength(environment.FREQ_NR)
        elif self.bs_type == "lte":
            self.wavelength = freq_to_wavelength(environment.FREQ_LTE)

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

    def calc_RSS(self, ueLocation):
        """
        This function calculates the Received Signal Strength of the base station in dB
        This value is calculated using the Friis equation, i.e. RSS = Ptx - Gtx - Grx - L
        :param ueLocation: Location of the UE
        :return: RSS in dB

        Here it is assumed that Gtx = Grx = 0 dB
        """
        if self.location != ueLocation:

            rss = 46 - (
                    20 * math.log10(4 * math.pi * math.fabs(self.location - ueLocation) / self.wavelength))
        else:
            rss = 0

        return rss
