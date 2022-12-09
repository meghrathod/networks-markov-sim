import UE
import eNB

class Simulator:
    """
    This class defines an enviroment for the simulator
    """
    
    def __init__(self, eNBs, UEs):
        self.eNBs = eNBs
        self.UEs = UEs
        self.time = 0
        self.UEs_in_range = []
        self.UEs_out_of_range = []
        
    def run(self):
        self.associate_UEs()
        
        
    def associate_UEs(self):
        for UE in self.UEs:
            for eNB in self.eNBs:
                if eNB.get_location() - 300 <= UE.get_location() <= eNB.get_location() + 300:
                    self.UEs_in_range.append(UE)
                    UE.set_eNB(eNB)
                else:
                    self.UEs_out_of_range.append(UE)
        

# Define the main function
def main():
    # Define the eNBs
    eNB1 = eNB.eNB(0, 1, "lte")
    eNB2 = eNB.eNB(500, 2, "nr")
    eNB3 = eNB.eNB(1000, 3, "nr")
    eNB4 = eNB.eNB(1500, 4, "lte")
    
    eNBs = [eNB1, eNB2, eNB3, eNB4]
    
    # Define the UEs
    UE = UE.UE(300)
    UEs = [UE]
    
    Simulator = Simulator(eNBs, UEs)
main()