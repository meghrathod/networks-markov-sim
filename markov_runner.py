import pandas as pd

import eNB_environments
import environment
import utils.misc
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
offsets = [3, 4, 5, 6, 7]


def simulate(iterations):
    probabilitySumMatrix = [[0 for x in range(11)] for y in range(11)]
    for i in range(iterations):
        u1 = UE(25000)
        s = Simulate_UE(u1, enbs[1])
        try:
            matrix = s.run(Ticker(), 1000000, False)
            probabilitySumMatrix = createProbabilitySumMatrix(
                probabilitySumMatrix, matrix)
        except:
            iterations -= 1

    p = averageProbabilityMatrix(probabilitySumMatrix, iterations)
    x = vector_calc(p)
    RLF, Hi, HOF = extract_data(x, p)
    # print(RLF, Hi, HOF)
    return RLF, Hi, HOF


data_vel = {"velocity": [], "RLF": [], "Hi": [], "HOF": []}
df_vel = pd.DataFrame(data_vel)
x = 0

for i in velocities:
    environment.MIN_SPEED = utils.misc.kmph_to_mpms(i)
    environment.MAX_SPEED = utils.misc.kmph_to_mpms(i)
    a, b, c = simulate(25)
    print(a, b, c)

    df_vel.loc[x] = [i, a, b, c]
    x = x + 1

print(df_vel)

df_vel.to_csv("vel.csv", header=True, index=False)

data_offset = {"offset": [], "RLF": [], "Hi": [], "HOF": []}
df_offset = pd.DataFrame(data_offset)

x = 0

for i in offsets:
    environment.PREP_THRESHOLD = i
    simulate(25)
    a, b, c = simulate(25)
    print(a, b, c)

    df_offset.loc[x] = [i, a, b, c]
    x = x + 1

df_offset.to_csv("prep_offset.csv", header=True, index=False)

data_exec_offset = {"offset": [], "RLF": [], "Hi": [], "HOF": []}
df_exec_offset = pd.DataFrame(data_exec_offset)

x = 0

for i in offsets:
    environment.EXEC_THRESHOLD = i
    simulate(25)
    a, b, c = simulate(25)
    print(a, b, c)

    df_exec_offset.loc[x] = [i, a, b, c]
    x = x + 1

df_exec_offset.to_csv("exec_offset.csv", header=True, index=False)

# df = pd.DataFrame(p)
# #  save to xlsx file
# filepath = '/Users/meghrathod/code/research/nr-simulator/markov_results/result_vel.csv'
# # add column and row labels to the dataframe
# df.to_excel(filepath)
# # print(iterations)
# print(df)
