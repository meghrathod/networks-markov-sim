import pandas as pd

import eNB_environments
import environment
import utils.misc
from Simulate_UE import Simulate_UE
from UE import UE
from utils.Ticker import Ticker
from utils.data_processor import createProbabilitySumMatrix, averageProbabilityMatrix, vector_calc, extract_data

enbs = eNB_environments.eNBs_mix1

# probabilitySumMatrix = [[0 for x in range(11)] for y in range(11)]

velocities = [10, 50, 100, 150, 200]
prep_offsets = [3, 4, 5, 6, 7]
exec_offsets = [1, 2, 3, 4, 5]


def simulate(iterations):
    probabilitySumMatrix = [[0 for x in range(11)] for y in range(11)]
    RLF_sum = [0 for x in range(iterations)]
    Hi_sum = [0 for x in range(iterations)]
    HOF_sum = [0 for x in range(iterations)]
    total_sum = [0 for x in range(iterations)]

    for i in range(iterations):
        u1 = UE(25000)
        s = Simulate_UE(u1, enbs[1])

        # try:
        matrix, count = s.run(Ticker(), 1000000, False)
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

    RLF_time = sum(RLF_sum) / len(total_sum)
    Hi_time = sum(Hi_sum) / len(total_sum)
    HOF_time = sum(HOF_sum) / len(total_sum)

    p = averageProbabilityMatrix(probabilitySumMatrix, iterations)
    x = vector_calc(p)
    RLF, Hi, HOF = extract_data(x, p)
    # print(RLF, Hi, HOF)
    return RLF, Hi, HOF, RLF_time, Hi_time, HOF_time


data_vel = {'velocity': [], 'RLF': [], 'Hi': [], 'HOF': [], 'RLF_time': [], 'Hi_time': [], 'HOF_time': []}
df_vel = pd.DataFrame(data_vel)
x = 0

for i in velocities:
    environment.MIN_SPEED = utils.misc.kmph_to_mpms(i)
    environment.MAX_SPEED = utils.misc.kmph_to_mpms(i)
    a, b, c, d, e, f = simulate(25)
    print(a, b, c, d, e, f)

    df_vel.loc[x] = [i, a, b, c, d, e, f]
    x = x + 1

print(df_vel)

df_vel.to_csv('vel.csv', header=True, index=False)

data_offset = {'offset': [], 'RLF': [], 'Hi': [], 'HOF': [], 'RLF_time': [], 'Hi_time': [], 'HOF_time': []}
df_offset = pd.DataFrame(data_offset)

x = 0

for i in prep_offsets:
    environment.PREP_THRESHOLD = i
    simulate(25)
    a, b, c, d, e, f = simulate(25)
    print(a, b, c, d, e, f)

    df_offset.loc[x] = [i, a, b, c, d, e, f]
    x = x + 1

df_offset.to_csv('prep_offset.csv', header=True, index=False)

data_exec_offset = {'offset': [], 'RLF': [], 'Hi': [], 'HOF': [], 'RLF_time': [], 'Hi_time': [], 'HOF_time': []}
df_exec_offset = pd.DataFrame(data_exec_offset)

x = 0

for i in exec_offsets:
    environment.EXEC_THRESHOLD = i
    simulate(25)
    a, b, c, d, e, f = simulate(25)
    print(a, b, c, d, e, f)

    df_exec_offset.loc[x] = [i, a, b, c, d, e, f]
    x = x + 1

df_exec_offset.to_csv('exec_offset.csv', header=True, index=False)

# df = pd.DataFrame(p)
# #  save to xlsx file
# filepath = '/Users/meghrathod/code/research/nr-simulator/markov_results/result_vel.csv'
# # add column and row labels to the dataframe
# df.to_excel(filepath)
# # print(iterations)
# print(df)
