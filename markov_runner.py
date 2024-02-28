import numpy as np
import pandas as pd

import eNB_environments
import environment
from Simulate_UE import Simulate_UE
from UE import UE
from utils.data_processor import (
    averageProbabilityMatrix,
    createProbabilitySumMatrix,
    extract_data,
    vector_calc,
)
from utils.Ticker import Ticker

enbs = eNB_environments.eNBs_mix1

# probabilitySumMatrix = [[0 for x in range(11)] for y in range(11)]

velocities = [10, 50, 100, 150, 200]
prep_offsets = [4, 5, 6, 7, 8]
exec_offsets = [1, 2, 3, 4, 5]
ttt = [50, 60, 70, 80, 90, 100]


def simulate(iterations):
    probabilitySumMatrix = [[0 for x in range(11)] for y in range(11)]
    RLF_sum = [0 for x in range(iterations)]
    Hi_sum = [0 for x in range(iterations)]
    HOF_sum = [0 for x in range(iterations)]
    total_sum = [0 for x in range(iterations)]
    average_latencies = [0 for x in range(iterations)]
    num_of_handovers = [0 for x in range(iterations)]
    all_latencies = []

    for i in range(iterations):
        u1 = UE(25000)
        s = Simulate_UE(u1, enbs[1])

        # try:
        matrix, count, average_latency, success, latency_array = s.run(
            Ticker(), 1000000, False
        )
        # concat all_latencies and average_latency
        all_latencies = all_latencies + latency_array
        num_of_handovers[i] = success
        average_latencies[i] = average_latency
        for j in range(11):
            RLF_sum[i] += count[j][1]
            Hi_sum[i] += count[j][2]
            if j == 0:
                continue
            HOF_sum[i] += count[j][1]
        # calculate total sum of all the values in the matrix
        for m in range(11):
            total_sum[i] += sum(count[m])
        probabilitySumMatrix = createProbabilitySumMatrix(probabilitySumMatrix, matrix)
        # except Exception as e:
        #     # print("Error", e)
        #     iterations -= 1

    for k in range(len(total_sum)):
        if total_sum[k] != 0:
            RLF_sum[k] /= total_sum[k]
            Hi_sum[k] /= total_sum[k]
            HOF_sum[k] /= total_sum[k]
            total_sum[k] /= total_sum[k]
        else:
            RLF_sum[k] = 0
            Hi_sum[k] = 0
            HOF_sum[k] = 0
            total_sum[k] = 0

    latency_average = sum(all_latencies) / len(all_latencies)
    print(all_latencies)
    print(latency_average)
    RLF_time = sum(RLF_sum) / len(total_sum)
    Hi_time = sum(Hi_sum) / len(total_sum)
    HOF_time = sum(HOF_sum) / len(total_sum)
    num_of_handovers_average = sum(num_of_handovers) / len(num_of_handovers)

    p = averageProbabilityMatrix(probabilitySumMatrix, iterations)
    # print p as dataframe
    df = pd.DataFrame(p)
    print(df)
    x = vector_calc(p)
    # expect = sum(x[6:10]) / 5 * 1000000
    RLF, Hi, HOF = extract_data(x, p)
    # print(RLF, Hi, HOF)
    return RLF, Hi, HOF, RLF_time, Hi_time, HOF_time, latency_average, all_latencies
    # return expect, num_of_handovers_average


data_vel = {
    "velocity": [],
    "RLF": [],
    "Hi": [],
    "HOF": [],
    "RLF_time": [],
    "Hi_time": [],
    "HOF_time": [],
    "avg_latency": [],
}
df_vel = pd.DataFrame(data_vel)
x = 0

for i in velocities:
    environment.MIN_SPEED = utils.misc.kmph_to_mpms(i)
    environment.MAX_SPEED = utils.misc.kmph_to_mpms(i)
    a, b, c, d, e, f, g, i = simulate(25)
    print(i)

    df_vel.loc[x] = [i, a, b, c, d, e, f, g]
    x = x + 1

print(df_vel)

df_vel.to_csv("markov_result/packet_rate/all_latency_vel.csv", header=True, index=False)

data_ttt = {
    "TTT": [],
    "RLF": [],
    "Hi": [],
    "HOF": [],
    "RLF_time": [],
    "Hi_time": [],
    "HOF_time": [],
}
df_ttt = pd.DataFrame(data_ttt)
x = 0

for i in ttt:
    environment.TTT = i
    a, b, c, d, e, f = simulate(25)
    print(a, b, c, d, e, f)

    df_ttt.loc[x] = [i, a, b, c, d, e, f]
    x = x + 1

print(df_ttt)

df_ttt.to_csv("lte_ttt.csv", header=True, index=False)

data_offset = {"prep-offset": [], "latency": [], "num_of_samples": [], "std_dev": []}

df_offset = pd.DataFrame(data_offset)

x = 0

for i in prep_offsets:
    environment.PREP_THRESHOLD = i
    a, b, c, d, e, f, g, h = simulate(25)
    # print(a, b, c, d, e, f, g)
    samples = len(h)
    # calculate standard deviation of array h
    std_dev = np.std(np.array(h))

    df_offset.loc[x] = [i, g, samples, std_dev]
    x = x + 1

# print(df_offset)

df_offset.to_csv(
    "markov_result/re/prep-offset-latency-std.csv", header=True, index=False
)

data_exec_offset = {
    "offset": [],
    "RLF": [],
    "Hi": [],
    "HOF": [],
    "RLF_time": [],
    "Hi_time": [],
    "HOF_time": [],
    "latency": [],
}
df_exec_offset = pd.DataFrame(data_exec_offset)

x = 0

for i in exec_offsets:
    environment.EXEC_THRESHOLD = i
    a, b, c, d, e, f, g = simulate(25)
    print(a, b, c, d, e, f, g)

    df_exec_offset.loc[x] = [i, a, b, c, d, e, f, g]
    x = x + 1

print(df_exec_offset)
df_exec_offset.to_csv(
    "markov_result/latency_nofad_exec_offset.csv", header=True, index=False
)

data_exec_offset = {"offset": [], "expect_latency": []}
df_exec_offset = pd.DataFrame(data_exec_offset)

x = 0

for i in exec_offsets:
    environment.EXEC_THRESHOLD = i
    a, b = simulate(25)
    print(a, b)

    df_exec_offset.loc[x] = [i, a / b]
    x = x + 1

print(df_exec_offset)
df_exec_offset.to_csv(
    "markov_result/expect_latency_exec_offset3.csv", header=True, index=False
)

# df = pd.DataFrame(p)
# #  save to xlsx file
# filepath = '/Users/meghrathod/code/research/nr-simulator/markov_results/result_vel.csv'
# # add column and row labels to the dataframe
# df.to_excel(filepath)
# # print(iterations)
# print(df)
