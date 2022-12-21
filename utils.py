import math

import environment


def freq_to_wavelength(frequency):
    """This function converts frequency provided in MHz to wavelength in meters"""
    wavelength = 3e8 / (frequency * 1e6)
    return wavelength


def gigahertz_to_megahertz(frequency):
    """This function converts frequency provided in GHz to MHz"""
    frequency = frequency * 1e3
    return frequency


def calc_power_in_dbm(power):
    """
    This function calculates the transmitted power of the base station in dBm given the value in mW
    :param power: Transmitted power in mW
    """
    return 10 * math.log10(power)


class Ticker:
    """
    This class defines the properties of a ticker, i.e. a timer that ticks at a certain interval.
    """

    def __init__(self):
        self.ticker_duration = environment.TICKER_INTERVAL
        self.time = 0

    def tick(self):
        self.time += self.ticker_duration

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time
