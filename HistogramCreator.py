
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import math
import plotly.plotly as py
zenith = []
azimuth = []

def addZenith(val):
    zenith.append(val)
def addAzimuth(val):
    azimuth.append(val)
def plotZenith():
    # plt.hist(zenith, bins=10, edgecolor='black', linewidth=1, orientation='horizontal', color='#00FFFF')
    # plt.title("Zenith data of HTC Wildfire")
    # plt.ylabel("Zenith (Degrees)")
    # plt.xlabel("Frequency")
    # plt.yticks(range(0, 95, 5))
    # plt.xticks(range(0, 5, 1))
    # plt.show()

    h = np.histogram(zenith, bins = 9)
    print h
    bins = h[1]
    theta = np.radians((bins[1:] + bins[:-1]) / 2)
    width = np.pi / 25
    radii = h[0]
    color = []
    print "radii", radii
    for i in range(len(radii)):
        if(radii[i] == 0):
            color.append('#000000')
        elif(radii[i] == 1):
            color.append('#FFCCCC')
        elif (radii[i] == 2):
            color.append('#FF9999')
        elif (radii[i] == 3):
            color.append('#FF6666')
        elif (radii[i] == 4):
            color.append('#FF3333')
        elif (radii[i] == 5):
            color.append('#FF0000')
        elif (radii[i] == 6):
            color.append('#CC0000')
        elif (radii[i] == 7):
            color.append('#990000')
        elif (radii[i] == 8):
            color.append('#660000')
        elif (radii[i] == 9):
            color.append('#330000')
        elif (radii[i] == 10):
            color.append('#1A0000')
    for i in radii:
        print"yeet"
        radii[i] = 1


    ax = plt.subplot(111, projection='polar')
    ax.set_yticks(range(0, 15, 7))
    ax.set_xticks(np.arange(0, np.pi * 2, np.pi/18))
    bars = ax.bar(theta, radii, width=width, bottom=0.0, color=color)
    count = 0
    print "COLOR LENGTH", len(color)
    for r, bar in zip(radii, bars):
        bar.set_facecolor(color[count])
        # bar.set_alpha(0.5)
        count += 1
    plt.show()

def plotAzimuth():
    plt.hist(azimuth, bins=30, edgecolor='black', linewidth=1, orientation='horizontal', color='#00FFFF')
    plt.title("Azimuth data of HTC Wildfire")
    plt.ylabel("Azimuth (Degrees)")
    plt.xlabel("Frequency")
    plt.show()



    # plt.hist(zenith, bins=30, edgecolor='black', linewidth=1, orientation='horizontal', color='#00FFFF')
    # plt.title("Zenith data of HTC Wildfire")
    # plt.ylabel("Zenith (Degrees)")
    # plt.xlabel("Frequency")
    # plt.show()


    #h[0] = counts
    #h[1] = bins
    # theta = bins[1:] + bins[:-1] \ 2
