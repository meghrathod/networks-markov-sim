import math


def freq_to_wavelength(frequency):
    """This function converts frequency provided in MHz to wavelength in meters"""
    wavelength = 3e8 / (frequency * 1e6)
    return wavelength


def calc_power_in_dbm(power):
    """
    This function calculates the transmitted power of the base station in dBm given the value in mW
    :param power: Transmitted power in mW
    """
    return 10 * math.log10(power)


def calc_power_in_mw(power):
    """
    This function calculates the transmitted power of the base station in mW given the value in dBm
    :param power: Transmitted power in dBm
    """
    return 10 ** (power / 10)


def gigahertz_to_megahertz(frequency):
    """This function converts frequency provided in GHz to MHz"""
    frequency = frequency * 1e3
    return frequency


def kmph_to_mpms(speed):
    """This function converts speed provided in kmph to m/ms"""
    speed = speed / 3600
    return speed


def calc_throughput(sinr: float, bandwidth: float) -> float:
    """
    This function calculates the throughput of the base station
    :param sinr: SINR of the base station
    :param bandwidth: Bandwidth of the base station
    :return: Throughput of the base station
    """

    # Calculate the throughput
    throughput = 0
    if sinr > 0:
        throughput = bandwidth * math.log2(1 + sinr)
    return throughput


def calc_SINR(ueLocation: float, rsrp: float, interference: float) -> float:
    """
    This function calculates the SINR of the base station in dB
    :param ueLocation: Location of the UE
    :param rsrp: RSRP of the base station
    :param interference: Interference from other base stations
    :return: SINR(Signal to Interference plus Noise Ratio) in dBm
    Here it is assumed that Gtx = Grx = 0 dB (Gains of the transmitter and receiver)
    """
    sinr = rsrp / interference
    return sinr
