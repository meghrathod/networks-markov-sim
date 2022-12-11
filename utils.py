def freq_to_wavelength(frequency):
    """
    This function converts frequency provided in MHz to wavelength in meters
    """
    wavelength = 3e8 / (frequency * 1e6)
    return wavelength


def gigahertz_to_megahertz(frequency):
    """
    This function converts frequency provided in GHz to MHz
    """
    frequency = frequency * 1e3
    return frequency
