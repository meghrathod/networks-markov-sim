import random
import threading

import utils.Result
from Simulate_UE import Simulate_UE
from UE import UE
from eNB import eNBs
from utils.Ticker import Ticker


def main(lock_mutex: threading.Lock, ue_arg: UE, enbs_arg: eNBs, ticker: Ticker) -> utils.Result.Result:
    # Define the UEs
    u1 = ue_arg

    # seed(42)
    # graph_rsrp(enbs_arg)
    S = Simulate_UE(u1, enbs_arg)
    res = S.run(ticker, time=1000000)
    lock_mutex.acquire()
    try:
        utils.Result.Result.save_to_file(res, "results.xlsx")
    finally:
        lock_mutex.release()
    return res


# Create a lock to synchronize access to the file
lock = threading.Lock()

# Define the number of threads to run
num_threads = 5

# Create and start the threads

threads = []
for i in range(num_threads):
    # Create a new UE and eNBs object for each thread
    ue = UE(random.randint(0, 50000))
    enbs = eNBs
    t = Ticker()
    thread = threading.Thread(target=main, args=(lock, ue, enbs, t))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish

for thread in threads:
    thread.join()
