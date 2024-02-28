from utils.misc import gigahertz_to_megahertz, kmph_to_mpms

# DEFINE constants for the environment
FREQ_NR = gigahertz_to_megahertz(25)  # MHz
FREQ_LTE = gigahertz_to_megahertz(2.5)  # MHz
TTT = 80  # ms
HYSTERESIS = 10  # dB
PTX = 10  # mW
TICKER_INTERVAL = 20  # ms
A3_OFFSET = 0  # dB
MIN_SPEED = kmph_to_mpms(40)
MAX_SPEED = kmph_to_mpms(50)
MIN_PAUSE = 10  # ms
MAX_PAUSE = 100  # ms
BANDWIDTH_NR = 100  # MHz
BANDWIDTH_LTE = 20  # MHz
RLF_THRESHOLD = -130.0  # dBm
TPREP = 100  # ms
TEXEC = 80  # ms
PREP_THRESHOLD = 5
EXEC_THRESHOLD = 3
