from utils.misc import gigahertz_to_megahertz

# DEFINE constants for the environment
FREQ_NR = gigahertz_to_megahertz(25)  # MHz
FREQ_LTE = gigahertz_to_megahertz(2.5)  # MHz
TTT = 800  # ms
HYSTERESIS = 15  # dB
PTX = 10  # mW
TICKER_INTERVAL = 400  # ms
A3_OFFSET = 0  # dB
MIN_SPEED = 0.01  # m/ms
MAX_SPEED = 0.05  # m/ms
MIN_PAUSE = 10  # ms
MAX_PAUSE = 100  # ms
BANDWIDTH_NR = 100  # MHz
BANDWIDTH_LTE = 20  # MHz
RLF_THRESHOLD = -130.0  # dBm
TPREP = 2400  # ms
TEXEC = 2000  # ms
PREP_THRESHOLD = 3
EXEC_THRESHOLD = 2
