import os
import random
import threading

import eNB_environments
import utils.Result
from Simulate_UE import Simulate_UE
from UE import UE
from utils.Ticker import Ticker


def main(lock_mutex: threading.Lock, time_to_trigger: int, hysteresis: int, velocity_min: float,
         velocity_max) -> utils.Result.Result:
    u1 = UE(random.randint(0, 50000))
    enbs = eNB_environments.eNBs_mix1
    ticker = Ticker()
    S = Simulate_UE(u1, enbs[1])
    res = S.run(ticker, time=100000)
    lock_mutex.acquire()
    try:
        file_name = "Results/results_with_throughput_hys_new.xlsx"
        file_name = os.path.join(os.path.dirname(__file__), file_name)
        utils.Result.Result.save_to_file(res, file_name, enbs[0], time_to_trigger, hysteresis, velocity_min,
                                         velocity_max)
    finally:
        lock_mutex.release()
    return res


# Define the number of threads to run
def run_threads(time_to_trigger: int, hysteresis: int, velocity_min: float, velocity_max: float):
    """
    This function runs the main function in multiple threads
    """
    # Create a lock to synchronize access to the file
    lock = threading.Lock()

    # Create a list of threads
    num_threads = 30
    threads = []
    for i in range(num_threads):
        # Create a new UE and eNBs object for each thread
        thread = threading.Thread(target=main, args=(lock, time_to_trigger, hysteresis, velocity_min, velocity_max))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish

    for thread in threads:
        thread.join()
