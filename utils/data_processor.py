import numpy as np
import pandas as pd


def createDataFrame(countMatrix):
    numpyTable = np.array(countMatrix)

    return pd.DataFrame(numpyTable)


def createProbabilityMatrix(countMatrix):
    probabilityMatrix = [[0 for x in range(11)] for y in range(11)]
    for i in range(0, 11):
        rowSum = sum(countMatrix[i])
        if rowSum == 0:
            continue
        for j in range(0, 11):
            probabilityMatrix[i][j] = countMatrix[i][j] / rowSum
    return probabilityMatrix


def createCountMatrix(initHiCounter, prepSuccess, prepFailure, execSuccess, execFailure, RLF_at_NORM, RLF, success):
    #     11x11 grid
    countMatrix = [[0 for x in range(11)] for y in range(11)]
    for i in range(0, 4):
        countMatrix[i + 2][1] = RLF[i]
        countMatrix[i + 2][i + 3] = prepSuccess[i + 1]
        countMatrix[i + 7][1] = RLF[i + 4]
        countMatrix[i + 6][i + 7] = execSuccess[i]

    for i in range(0, 3):
        countMatrix[i + 7][6] = execFailure[i + 1]
        countMatrix[i + 3][2] = prepFailure[i + 1]
    countMatrix[0][1] = RLF_at_NORM
    countMatrix[0][2] = initHiCounter
    countMatrix[10][0] = success
    return countMatrix


def createProbabilitySumMatrix(initialMatrix, probabilityMatrix):
    for i in range(0, 11):
        for j in range(0, 11):
            initialMatrix[i][j] += probabilityMatrix[i][j]
    return initialMatrix


def averageProbabilityMatrix(matrix, count):
    for i in range(0, 11):
        for j in range(0, 11):
            matrix[i][j] /= count
    return matrix


def vector_calc(p):
    alpha = p[2][2] - 1 + (p[3][2] * p[2][3]) + (p[4][2] * p[3][4] * p[2][3]) + (p[5][2] * p[4][5] * p[3][4] * p[2][3])
    beta = 1 + p[2][3] + (p[3][4] * p[2][3]) + (p[4][5] * p[3][4] * p[2][3])
    gamma = 1 + p[6][7] + (p[7][8] * p[6][7]) + (p[8][9] * p[7][8] * p[6][9]) + (
            p[10][0] * p[9][10] * p[8][9] * p[7][8] * p[6][7])
    lamb = p[5][6] * p[4][5] * p[3][4] * p[2][3]
    delta = p[6][6] - 1 + (p[7][6] * p[6][9]) + (p[8][6] * p[7][8] * p[6][7]) + (p[9][6] * p[8][9] * p[7][8] * p[6][7])

    # Make an array of 11 values
    x = [0 for a in range(11)]
    x[0] = (alpha * delta) / ((2 * alpha * delta) + (p[0][2] * lamb * gamma) - (delta * beta * p[0][2]))
    x[2] = delta / ((delta * beta) - (lamb * gamma) - ((2 * alpha * delta) / p[0][2]))
    x[6] = lamb / (((2 * alpha * delta) / p[0][2]) + (lamb * gamma) - (delta * beta))
    x[10] = p[9][10] * p[8][9] * p[7][8] * p[6][7] * x[6]
    x[1] = x[0] - p[10][0] * x[10]
    x[3] = x[2] * p[2][3]
    x[4] = x[3] * p[3][4]
    x[5] = x[4] * p[4][5]
    x[7] = x[6] * p[6][9]
    x[8] = x[6] * p[7][8] * p[6][7]
    x[9] = x[6] * p[8][9] * p[7][8] * p[6][7]

    return x


def extract_data(x, p):
    # Extract the data from the vector
    RLF = x[1]
    initHiCounter = x[2]
    HOF = x[2] * p[2][1] + x[3] * p[3][1] + x[4] * p[4][1] + x[5] * p[5][1] + x[6] * p[6][1] + x[7] * p[7][1] + x[8] * \
          p[8][1] + x[9] * p[9][1] + x[10] * p[10][1]

    return RLF, initHiCounter, HOF
