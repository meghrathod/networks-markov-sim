from utils.misc import gigahertz_to_megahertz

# DEFINE constants for the environment
FREQ_NR = gigahertz_to_megahertz(25)  # MHz
FREQ_LTE = gigahertz_to_megahertz(2.5)  # MHz
TTT = 25  # ms
HYSTERESIS = 20  # dB
PTX = 10  # mW
TICKER_INTERVAL = 10  # ms
A3_OFFSET = 0  # dB
MIN_SPEED = 0.01  # m/ms
MAX_SPEED = 0.05  # m/ms
MIN_PAUSE = 10  # ms
MAX_PAUSE = 100  # ms
BANDWIDTH_NR = 100  # MHz
BANDWIDTH_LTE = 20  # MHz
RLF_THRESHOLD = -130  # dBm
TPREP = 2000  # ms
