import math
import random
import environment

class eNB:
    """
    This class defines properties of a base station.
    It has a location, type
    """
    
    def __init__(self, x, type):
        self.id = random.randint(0, 1000)
        self.location = x
        self.type = type # "nr" or "lte"
        if self.type == "nr":
            self.wavelength = self.freq_to_wavelength(environment.FREQ_NR)
        elif self.type == "lte":
            self.wavelength = self.freq_to_wavelength(environment.FREQ_LTE)
        
    def __str__(self):
        return "eNB located at %s of type: %s" % (self.location, self.type)
    
    def get_location(self):
        return self.location
    
    def get_type(self):
        return self.type
    
    def set_location(self, x):
        self.location = x
        
    def set_type(self, type):
        self.type = type
        
    def freq_to_wavelength(self, frequency):
        """
        This function converts frequency provided in MHz to wavelength in meters
        """
        wavelength = 3e8 / (frequency * 1e6)
        return wavelength        
    
    # TODO: Clarify RSS and received power from Shankar Sir
    
    def calc_received_power(self, distance):
        """
        This function calculates the power of the base station
        """
        path_loss =  (20 * math.log10(4 * math.pi * math.fabs(self.location - distance) / self.wavelength)) +30
        received_power = 46 - path_loss # 46 dBm is a common transmit power of the base station
        return received_power
    

p = eNB(0, "lte")
q = eNB(0, "nr")

print(p.calc_received_power(1))
print(q.calc_received_power(1))

# Use matplotlib to plot the received power of the base station 
# as a function of distance from the base station

import matplotlib.pyplot as plt
import numpy as np

x = [i for i in range(1, 2000)]
y1 = [p.calc_received_power(i) for i in x]
y2 = [q.calc_received_power(i) for i in x]

plt.plot(x, y1, label = "LTE")
plt.plot(x, y2, label = "NR")
plt.xlabel("Distance from eNB")
plt.ylabel("Received power")
plt.legend()
plt.show()