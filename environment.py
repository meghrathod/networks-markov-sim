from eNB import eNB
from utils import gigahertz_to_megahertz

# DEFINE constants for the environment
VELOCITY = 30000  # m/ms
FREQ_NR = gigahertz_to_megahertz(25)  # MHz
FREQ_LTE = gigahertz_to_megahertz(2.5)  # MHz
TTT = 5000  # ms
HYSTERESIS = 10  # dB

en1 = eNB(10000, "lte")
en2 = eNB(40000, "lte")
en3 = eNB(5000, "nr")
en4 = eNB(15000, "nr")
en5 = eNB(25000, "nr")
en6 = eNB(35000, "nr")

eNBs = [en1, en2, en3, en4, en5, en6]
