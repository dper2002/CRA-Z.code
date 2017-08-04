import numpy as np
import math
import random
import time
from scipy import stats

def findLine(blobList):
    # fit with np.polyfit
    blobsThatAreTracks = []
    oneBlobIsTrack = False
    for i in blobList:
        # xArr = []
        # yArr = []
        # if len(i.x) > len(i.y):
        #     xArrAux = i.x[:]
        #     for j in i.y:
        #         randNum = random.randint(0, len(xArrAux) - 1)
        #         xArr.append(xArrAux[randNum])
        #         xArrAux = np.delete(xArrAux, randNum)
        #         yArr.append(j)
        # if len(i.y) >= len(i.x):
        #     yArrAux = i.y[:]
        #     for j in i.x:
        #         randNum = random.randint(0, len(yArrAux) - 1)
        #         yArr.append(yArrAux[randNum])
        #         yArrAux = np.delete(yArrAux, randNum)
        #         xArr.append(j)
        r = stats.linregress(i.x, i.y)
        print 'r val:', r[2] ** 2
        if(r[2] ** 2 >= .10):
            blobsThatAreTracks.append(i)
            i.setR2Val(r[2] ** 2)
            oneBlobIsTrack = True
        else:
            print 'WORM WORM WORM WORM WORM'
            i.setTrack(False)
            return "null"
    if(oneBlobIsTrack):
        maxR = blobsThatAreTracks[0]
        for track in blobsThatAreTracks:
            if track.r2 > maxR.r2:
                maxR = track
        maxR.setTrack(True)
        if(maxR.isTrack):
            equation = np.polyfit(maxR.x, maxR.y, 1)
            xMin = maxR.x[0]
            xMax = maxR.x[len(maxR.x) - 1]
            yMin = maxR.y[0]
            yMax = maxR.y[len(maxR.y) - 1]
            for x in maxR.x:
                if x < xMin:
                    xMin = x
                if x > xMax:
                    xMax = x
            for y in maxR.y:
                if y < yMin:
                    yMin = y
                if y > yMax:
                    yMax = y
            distance = math.sqrt((xMax - xMin)**2 + (yMax - yMin)**2)
            distance = distance * .9
            maxR.setLength(distance)
            print distance
            maxR.setLineEquation(equation[0], equation[1])
            print 'y = ', maxR.lineEquation[0],'x +', maxR.lineEquation[1]
            return maxR