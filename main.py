import random
import threading

import eNB_environments
import utils.Result
from Simulate_UE import Simulate_UE
from UE import UE
from utils.Ticker import Ticker


def main(lock_mutex: threading.Lock) -> utils.Result.Result:
    # Define the UEs
    u1 = UE(random.randint(0, 50000))
    # print(id(u1))
    enbs = eNB_environments.eNBs_mix1
    ticker = Ticker()
    # print(id(ticker))

    # seed(42)
    # graph_rsrp(enbs)
    S = Simulate_UE(u1, enbs[1])
    res = S.run(ticker, time=10000000)
    lock_mutex.acquire()
    try:
        utils.Result.Result.save_to_file(res, "results_TTT_at_5dB.xlsx", enbs[0])
    finally:
        lock_mutex.release()
    return res


# Create a lock to synchronize access to the file
lock = threading.Lock()

# Define the number of threads to run
num_threads = 30
threads = []
for i in range(num_threads):
    # Create a new UE and eNBs object for each thread
    thread = threading.Thread(target=main, args=(lock,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish

for thread in threads:
    thread.join()
