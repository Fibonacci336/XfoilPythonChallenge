# -*- coding: utf-8 -*-
# FILE: runXFOIL_alphaSweep.py

import xfoil_module
import matplotlib.pyplot as plt
import numpy as np
import os

aoaLowerBound = -10
aoaUpperBound = 20

aoaValues = np.arange(aoaLowerBound, aoaUpperBound+1, 1)

airfoilFile = 'naca633618.dat'

rValues = [3e6, 10e6, 15e6]

rValSize = len(rValues)

def parseDATFile(filePath):
    f = open(filePath, "r")

    xVals = []
    yVals = []

    airfoilName = ""

    for line in f:
        if "NACA" in line:
            airfoilName = line
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
    return xVals,yVals, airfoilName

def plotAirfoil(datFilePath):
    x, y, name = parseDATFile(datFilePath)

    plt.plot(x, y)
    plt.title(name)
    plt.ylim(-.1, 0.75)
    plt.show()


def plotCoeffGraphs(AoA, Cl, Cd, Cm, Reynolds):
    fig, axs = plt.subplots(2, 2)
    fig.set_figwidth(8)
    fig.set_figheight(8)
    fig.suptitle("Plots for R={:.1e}".format(Reynolds))

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


def getTrailingEdgeProperties(airfoilDAT, alphas, Reynolds):

    alphaList = alphas

    displacementThicknessArray = []
    momentumThicknessArray = []
    shapeFactorArray = []

    if not isinstance(alphas, list) and not isinstance(alphas, np.ndarray):
        alphaList = [alphas]

    for alpha in alphaList:
        xfoil_module.call(airfoilDAT, alpha, output='Dump', Reynolds=Reynolds, NACA=False)
        fileName = xfoil_module.file_name(airfoilDAT, alfas=alpha, output='Dump')

        #Get Final Line of File
        with open(fileName, 'r') as file:
            for trailingLine in file:
                pass

        trailingArray = trailingLine.split()
        #Hardcoded column locations due to XFoil consistancy (Others not nescessary)
        displacementThicknessArray.append(trailingArray[4])
        momentumThicknessArray.append(trailingArray[5])
        shapeFactorArray.append(trailingArray[7])
        os.remove(fileName)


    displacementThicknessArray = [float(i) for i in displacementThicknessArray]
    momentumThicknessArray = [float(i) for i in momentumThicknessArray]
    shapeFactorArray = [float(i) for i in shapeFactorArray]

    return displacementThicknessArray, momentumThicknessArray, shapeFactorArray



#Plot Boundary layer properties at the trailing edge
def plotBoundaryProperties(airfoilDAT):

    fig, axs = plt.subplots(rValSize, 3)
    fig.set_figwidth(10)
    fig.set_figheight(10)

    for rIndex in range(0, rValSize):
        rNum = rValues[rIndex]

        dStars, thetas, Hs = getTrailingEdgeProperties(airfoilDAT, aoaValues, rNum)

        axs[rIndex, 0].plot(dStars, aoaValues)
        axs[rIndex, 0].set_title('D-Thickness vs AoA\nR={:.1e}'.format(rNum))
        axs[rIndex, 0].set_xlabel("D-Thickness")
        axs[rIndex, 0].set_ylabel("AoA")

        axs[rIndex, 1].plot(thetas, aoaValues)
        axs[rIndex, 1].set_title('M-Thickness vs AoA\nR={:.1e}'.format(rNum))
        axs[rIndex, 1].set_xlabel("M-Thickness")
        axs[rIndex, 1].set_ylabel("AoA")

        axs[rIndex, 2].plot(Hs, aoaValues)
        axs[rIndex, 2].set_title('Shape Factor vs AoA\nR={:.1e}'.format(rNum))
        axs[rIndex, 2].set_xlabel("Shape Factor")
        axs[rIndex, 2].set_ylabel("AoA")

    plt.show()


def plotPressureDistributions(airfoilDAT):
    pressureAoAs = [0, 4, 8, 12]
    aoaSize = len(pressureAoAs)

    fig, axs = plt.subplots(aoaSize, rValSize)
    fig.subplots_adjust(hspace=1)
    fig.set_figwidth(10)
    fig.set_figheight(10)

    for alphaIndex in range(0, aoaSize):
        aoa = pressureAoAs[alphaIndex]

        for rNumIndex in range(0, rValSize):
            rNum = rValues[rNumIndex]

            pressureCoeffs = xfoil_module.find_pressure_coefficients(airfoil=airfoilDAT, Reynolds=rNum, alpha=aoa,
                                                                     NACA=False)
            xVals = pressureCoeffs['x']
            CpVals = pressureCoeffs['Cp']

            axs[alphaIndex, rNumIndex].plot(xVals, CpVals)
            axs[alphaIndex, rNumIndex].set_title("AoA=" + str(aoa) + " R=" + str(rNum))
            axs[alphaIndex, rNumIndex].set_xlabel("X")
            axs[alphaIndex, rNumIndex].set_ylabel("Cp")
            axs[alphaIndex, rNumIndex].invert_yaxis()

    plt.show()


def plotPolarCoefficients(airfoilDAT):
    # Plot aerodynamic polar coefficients
    for rNum in rValues:
        polarCoeffs = xfoil_module.find_coefficients(airfoil=airfoilDAT, Reynolds=rNum, alpha=aoaValues, NACA=False,
                                                     delete=True)

        cm = polarCoeffs['CM']
        cl = polarCoeffs['CL']
        cd = polarCoeffs['CD']
        AoA = polarCoeffs['alpha']

        plotCoeffGraphs(AoA, cl, cd, cm, rNum)




#Main Execution
plotAirfoil(airfoilFile)
plotPolarCoefficients(airfoilFile)
plotPressureDistributions(airfoilFile)
plotBoundaryProperties(airfoilFile)






