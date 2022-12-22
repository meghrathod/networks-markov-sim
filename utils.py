import numpy
from matplotlib import pyplot as plt

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
    return 10 * numpy.log10(power)


def graph_rsrp(eNBs):
    """This function plots the received signal strength as a
    function of distance from the base station"""
    x = list(range(1, 50000))

    # Add y-axis labels at increments of 5
    # add guidelines at increments of 5
    plt.yticks(list(range(-110, 0, 5)))
    for i in range(-110, 0, 5):
        plt.axhline(y=i, color="lightgrey", linestyle="-")

    def get_line_color(bs_type):
        if bs_type == "lte":
            return "orange"
        if bs_type == "nr":
            return "deepskyblue"

    for e in eNBs:
        plt.plot(
            x,
            [e.calc_RSRP(a) for a in x],
            label=e.get_type() + str(e.get_id()),
            markersize=1,
            color=get_line_color(e.get_type()),
        )

    plt.ylim(-120, -60)
    plt.xlabel("Distance from eNB(meters)")
    plt.ylabel("Estimated RSRP (dBm)")
    plt.legend()
    plt.show()


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
