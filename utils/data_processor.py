import numpy as np
import pandas as pd


def createDataFrame(countMatrix):
    numpyTable = np.array(countMatrix)

    return pd.DataFrame(numpyTable)


def createProbabilityMatrix(countMatrix):
    probabilityMatrix = [[0 for x in range(14)] for y in range(14)]
    for i in range(0, 14):
        rowSum = sum(countMatrix[i])
        if rowSum == 0:
            continue
        for j in range(0, 14):
            probabilityMatrix[i][j] = countMatrix[i][j] / rowSum
    return probabilityMatrix


def createCountMatrix(initHiCounter, prepSuccess, prepFailure, execSuccess, execFailure, RLF_at_NORM, RLF):
    #     14x14 grid
    countMatrix = [[0 for x in range(14)] for y in range(14)]
    for i in range(0, 5):
        countMatrix[i + 3][1] = RLF[i]
        countMatrix[i + 3][2] = prepFailure[i + 1]
        countMatrix[i + 2][i + 3] = prepSuccess[i]
        countMatrix[i + 8][i + 9] = execSuccess[i]
        countMatrix[i + 9][1] = RLF[i + 5]
    for i in range(0, 4):
        countMatrix[i + 9][8] = execFailure[i + 1]
    countMatrix[0][1] = RLF_at_NORM
    countMatrix[0][2] = initHiCounter
    countMatrix[13][0] = 1
    return countMatrix


def createProbabilitySumMatrix(initialMatrix, probabilityMatrix):
    for i in range(0, 14):
        for j in range(0, 14):
            initialMatrix[i][j] += probabilityMatrix[i][j]
    return initialMatrix


def averageProbabilityMatrix(matrix, count):
    for i in range(0, 14):
        for j in range(0, 14):
            matrix[i][j] /= count
    return matrix
