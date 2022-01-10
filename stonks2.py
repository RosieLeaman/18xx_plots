import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def read_stonks(filename):
    roundNames = []
    roundValues = []
    playerNames = []

    with open(filename, "r") as f:
        line = f.readline()
        playerNames = line.split("\t")
        playerNames[-1] = playerNames[-1].rstrip()

        while True:
            line = f.readline()

            if line == "":
                break

            line = line.split("\t")

            roundNames.append(line[0])
            roundValues.append([int(line[x][1:]) for x in range(1, len(line))])

    roundNames.reverse()
    roundValues.reverse()

    return roundNames, roundValues, playerNames

def plot_stonks(roundNames, roundValues, playerNames):
    numRounds = len(roundNames)

    x = np.arange(0, numRounds)

    fig, ax = plt.subplots()

    for i in range(0, len(roundValues[0])):
        y = [roundValues[x][i] for x in range(0, numRounds)]
        ax.plot(x, y, marker = 'o', label = playerNames[i])

    ax.set_xticks(x)
    ax.set_xticklabels(roundNames, rotation = 60)

    plt.legend()

    plt.show()

def plot_stonks_minus_avg(roundNames, roundValues, playerNames):
    numRounds = len(roundNames)

    x = np.arange(0, numRounds)

    normalisedRoundValues = [[0 for y in range(0, len(roundValues[0]))] for x in range(0, numRounds)]

    # print(roundValues)

    for i in range(0, numRounds):
        roundAvg = np.mean(roundValues[i])
        normalisedRoundValues[i] = [x - roundAvg for x in roundValues[i]]

    # then plot as normal

    fig, ax = plt.subplots()

    for i in range(0, len(normalisedRoundValues[0])):
        y = [normalisedRoundValues[x][i] for x in range(0, numRounds)]
        ax.plot(x, y, marker = 'o', label = playerNames[i])

    ax.set_xticks(x)
    ax.set_xticklabels(roundNames, rotation = 60)

    ax.set_ylabel("Value - average round value")

    plt.legend()

    plt.show()

def plot_stonks_deriv(roundNames, roundValues, playerNames):
    newRoundNames = [roundNames[i] + " -> " + roundNames[i + 1] for i in range(0, len(roundNames) - 1)]

    numRounds = len(newRoundNames)

    x = np.arange(0, numRounds)

    fig, ax = plt.subplots()

    for i in range(0, len(roundValues[0])):
        y = [roundValues[x + 1][i] - roundValues[x][i] for x in range(0, numRounds)]
        ax.plot(x, y, marker = 'o', label = playerNames[i])

    ax.set_xticks(x)
    ax.set_xticklabels(newRoundNames, rotation = 90)
    plt.tick_params(labelsize=6)

    plt.legend()

    plt.show()

def plot_stonks_deriv2(roundNames, roundValues, playerNames):
    # get just the SRs
    roundIndices = [0]
    for i in range(0, len(roundNames)):
        if roundNames[i][0:2] == 'SR':
            roundIndices.append(i)

    # add finale if not already there
    if len(roundNames) - 1 not in roundIndices:
        roundIndices.append(len(roundNames) - 1)

    newRoundNames = [roundNames[x] for x in roundIndices]
    newRoundValues = [roundValues[x] for x in roundIndices]

    # now get the change
    newRoundNames = [newRoundNames[i] + " - " + newRoundNames[i + 1] for i in range(0, len(newRoundNames) - 1)]

    numRounds = len(newRoundNames)

    x = np.arange(0, numRounds)

    fig, ax = plt.subplots()

    for i in range(0, len(roundValues[0])):
        y = [newRoundValues[x + 1][i] - newRoundValues[x][i] for x in range(0, numRounds)]
        ax.plot(x, y, marker = 'o', label = playerNames[i])

    ax.set_xticks(x)
    ax.set_xticklabels(newRoundNames, rotation = 30)
    plt.tick_params(labelsize=10)
    plt.grid()

    plt.ylabel("Change in value")
    plt.legend()

    plt.show()


def make_df_from_stonks(roundNames, roundValues, playerNames):

    df = pd.DataFrame(roundValues, columns = playerNames)
    df["round"] = roundNames

    print(df)

    # alternative

    df = df.melt(id_vars = "round", var_name = "player", value_name = "value")

    print(df)

def history_stonks(roundNames, roundValues, playerNames):

    numRounds = len(roundNames)
    numPlayers = len(playerNames)

    normalisedCumulative = []

    for i in range(0, numRounds):
        totalVal = sum(roundValues[i])
        normalised = [roundValues[i][x]/totalVal for x in range(0, numPlayers)]
        cumulative = [normalised[0]]

        for j in range(1, len(normalised)):
            cumulative.append(cumulative[j-1] + normalised[j])

        normalisedCumulative.append(cumulative)

    bottomX = [x for x in range(0, numRounds)]

    topX = [x for x in range(0, numRounds)]
    topX.reverse()

    bottomY = [0 for x in range(0, numRounds)]

    fig, ax = plt.subplots()

    for i in range(0, numPlayers):
        topY = [normalisedCumulative[x][i] for x in range(0, numRounds)]
        topY.reverse()

        polyX = bottomX[:]
        polyX.extend(topX)

        polyY = bottomY[:]
        polyY.extend(topY)

        ax.fill(polyX, polyY)

        # top becomes bottom
        topY.reverse()
        bottomY = topY

    ax.set_xticks(bottomX)
    ax.set_xticklabels(roundNames, rotation = 60)

    yticks = [(2*x+1)/(2*numPlayers) for x in range(0, numPlayers)]
    ax.set_yticks(yticks)
    ax.set_yticklabels(playerNames, rotation = 60, va = 'center')

    ax.set_title("Relative Player Value")

    plt.show()

# fileLoc = "stonks.txt" # test
# fileLoc = "stonks_38624_sixplayer.txt"
# fileLoc = "stonks_40893_3player.txt"
# fileLoc = "stonks_43266.txt"
# fileLoc = "stonks_43808.txt"
# fileLoc = "stonks_43531.txt"
# fileLoc = "stonks_53873.txt"
# fileLoc = "stonks_50964.txt"
# fileLoc = "stonks_50964_bez_raven.txt"
# fileLoc = "stonks_50963.txt"
fileLoc = "stonks_59458.txt"

roundNames, roundValues, playerNames = read_stonks(fileLoc)
#
# print(roundNames)
# print(roundValues)
# print(playerNames)

plot_stonks(roundNames, roundValues, playerNames)
history_stonks(roundNames, roundValues, playerNames)
plot_stonks_minus_avg(roundNames, roundValues, playerNames)
plot_stonks_deriv2(roundNames, roundValues, playerNames)
