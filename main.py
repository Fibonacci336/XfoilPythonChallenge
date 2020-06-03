# -*- coding: utf-8 -*-
# FILE: runXFOIL_alphaSweep.py

import xfoil_module
import matplotlib.pyplot as plt
import numpy as np

#This code does work
def parseDATFile(filePath):
    f = open(filePath, "r")

    xVals = []
    yVals = []

    for line in f:
        if "NACA" in line:
            continue
        line = line.strip()
        split = line.split(sep='     ')
        coords = list(map(float, split))
        xVals.append(coords[0])
        yVals.append(coords[1])

    if len(xVals) != len(yVals):
        print("DAT not formatted correctly!")
        exit(1)


    print("DAT successfully loaded")
    f.close()
    return xVals,yVals

def plotAirfoil(datFilePath):
    x, y = parseDATFile(datFilePath)

    plt.plot(x, y)
    plt.ylim(-.1, 0.75)
    plt.show()

#plotAirfoil('naca633618.dat')
#End working code


def plotCoeffGraphs(AoA, Cl, Cd, Cm):
    fig, axs = plt.subplots(2, 2)

    #Cl vs AoA graph
    axs[0, 0].plot(Cl, AoA)
    axs[0, 0].set_title('Cl vs AoA')
    axs[0, 0].set_xlabel("Cl")
    axs[0, 0].set_ylabel("AoA")

    #Cd vs AoA graph
    axs[0, 1].plot(Cd, AoA)
    axs[0, 1].set_title('Cd vs AoA')
    axs[0, 1].set_xlabel("Cd")
    axs[0, 1].set_ylabel("AoA")

    #Cm vs AoA graph
    axs[1, 0].plot(Cm, AoA)
    axs[1, 0].set_title('Cm vs AoA')
    axs[1, 0].set_xlabel("Cm")
    axs[1, 0].set_ylabel("AoA")

    #Cl/Cd vs AoA graph
    dividedValues = [i / j for i, j in zip(Cl, Cd)]
    axs[1, 1].plot(dividedValues, AoA)
    axs[1, 1].set_title('Cl/Cd vs AoA')
    axs[1, 1].set_xlabel("Cl/Cd")
    axs[1, 1].set_ylabel("AoA")

    plt.show()




aoaLowerBound = -10
aoaUpperBound = 20

aoaValues = np.arange(aoaLowerBound, aoaUpperBound+1, 1)

airfoilFile = 'naca633618.dat'

rValues = [3e6, 10e6, 15e6]

M = []
L = []
D = []
A = []

#Plot aerodynamic polar coefficients
for rNum in rValues:
    polarCoeffs = xfoil_module.find_coefficients(airfoil=airfoilFile, Reynolds=rNum, alpha=aoaValues, NACA=False, delete= True)

    cm = polarCoeffs['CM']
    cl = polarCoeffs['CL']
    cd = polarCoeffs['CD']
    AoA = polarCoeffs['alpha']

    plotCoeffGraphs(AoA, cl, cd, cm)



pressureAoAs = [0, 4, 8, 12]
aoaSize = len(pressureAoAs)
rValSize = len(rValues)
fig, axs = plt.subplots(aoaSize, rValSize)
fig.subplots_adjust(hspace=1)
fig.set_figwidth(10)
fig.set_figheight(10)

for alphaIndex in range(0, aoaSize):
    aoa = pressureAoAs[alphaIndex]

    for rNumIndex in range(0, rValSize):
        rNum = rValues[rNumIndex]

        pressureCoeffs = xfoil_module.find_pressure_coefficients(airfoil=airfoilFile, Reynolds=rNum, alpha=aoa, NACA=False)
        xVals = pressureCoeffs['x']
        CpVals = pressureCoeffs['Cp']

        axs[alphaIndex, rNumIndex].plot(xVals, CpVals)
        axs[alphaIndex, rNumIndex].set_title("AoA=" + str(aoa) + " R=" + str(rNum))
        axs[alphaIndex, rNumIndex].set_xlabel("X")
        axs[alphaIndex, rNumIndex].set_ylabel("Cp")
        axs[alphaIndex, rNumIndex].invert_yaxis()



plt.show()






