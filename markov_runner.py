import pandas as pd

import eNB_environments
from Simulate_UE import Simulate_UE
from UE import UE
from utils.data_processor import averageProbabilityMatrix, createProbabilitySumMatrix
from utils.Ticker import Ticker

enbs = eNB_environments.eNBs_mix1

probabilitySumMatrix = [[0 for x in range(14)] for y in range(14)]

iterations = 100

for i in range(iterations):
    u1 = UE(25000)
    s = Simulate_UE(u1, enbs[1])
    try:
        matrix = s.run(Ticker(), 5000000, False)
        probabilitySumMatrix = createProbabilitySumMatrix(probabilitySumMatrix, matrix)
    except:
        iterations -= 1

averageMatrix = averageProbabilityMatrix(probabilitySumMatrix, iterations)

df = pd.DataFrame(averageMatrix)
#  save to xlsx file
filepath = "/Users/meghrathod/code/research/nr-simulator/Results/results_new.xlsx"
# add column and row labels to the dataframe
row_column_labels = [
    "N",
    "RL",
    "H",
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "B1",
    "B2",
    "B3",
    "B4",
    "B5",
]
df.to_excel(filepath, index=True, index_label=row_column_labels)
print(iterations)
print(df)
