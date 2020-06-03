# -*- coding: utf-8 -*-
# FILE: runXFOIL_alphaSweep.py

from aeropy import xfoil_module
import matplotlib.pyplot as plt


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

coeff = xfoil_module.find_pressure_coefficients(airfoil='naca633618.dat', alpha=0,NACA=False)
print(coeff.keys())
