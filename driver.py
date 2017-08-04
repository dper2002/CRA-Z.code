import glob
import math
from lineReg import findLine
from plotBlobs import doThisFirst
import numpy as np
import HistogramCreator as hc
from purge_zeros import deco


def findAzimuth(slope):
    return math.degrees(math.atan(1/slope))


def findZenith(distance):
    print "distance", distance
    return math.degrees(math.atan(26/distance))


# pitch creates a matrix that effects a pitch by a given angle
# (similarly for roll and yaw functions)
# Davis's Code


def pitch(p_angle):
    pitch_matrix = np.array(
        [[1, 0, 0], [0, math.cos(p_angle), -math.sin(p_angle)],
         [0, math.sin(p_angle), math.cos(p_angle)]])
    return pitch_matrix


def roll(r_angle):
    roll_matrix = np.array([[math.cos(r_angle), 0, math.sin(r_angle)], [0, 1, 0],
                            [-math.sin(r_angle), 0, math.cos(r_angle)]])
    return roll_matrix


def yaw(y_angle):
    yaw_matrix = np.array([[math.cos(y_angle), -math.sin(y_angle), 0],
                           [math.sin(y_angle), math.cos(y_angle), 0], [0, 0, 1]])
    return yaw_matrix


def spherical_to_cartesian(zenith, azimuth):
    x = math.cos(azimuth) * math.cos(zenith)
    y = math.sin(azimuth) * math.cos(zenith)
    z = math.sin(zenith)
    return np.array([x, y, z])


def return_row(image_name):
    n = 0
    image_name = int(image_name[image_name.index("/") + 1:image_name.index(".")])
    print "NAME OF IMAGE SEARCHING FOR", image_name
    while True:
        eid = deco.iloc[n]["event_id"]
        print "eid", eid, "imagename", image_name
        if eid == image_name:
            print "IN IN IN "
            return deco.iloc[n]
        else:
            n = n + 1


def world_frame(direction, img):
    deco_world = np.dot(pitch(-(np.pi / 180) * return_row(img)["pitch"]),
                        np.dot(-roll((np.pi / 180) * return_row(img)["roll"]),
                               np.dot(-yaw((np.pi / 180) * return_row(img)["yaw"]),
                                      direction)))
    return deco_world


def convert_to_world_frame(zenith, azimuth, img):
    deco_world = world_frame(spherical_to_cartesian(zenith, azimuth), img)
    phi = math.atan2(deco_world[1], deco_world[0])
    theta = math.atan2(deco_world[2], 1)
    if phi > np.pi / 2:
        phi = np.pi - phi
        theta = np.pi + theta
    elif phi == np.pi / 2:
        theta = 0
    return np.array([phi * (180 / np.pi), theta * (180 / np.pi)])


# pics = glob.glob("images/*.jpg")
# d = {}
# d['Zenith'] = []
# d['Azimuth'] = []
# d['R2'] = []
# for i in pics:
#     print i
#     blobs = doThisFirst(i)
#     print(len(blobs))
#     if(len(blobs) > 0):
#         track = findLine(blobs)
#         print "track:", track
#         if track != "null":
#             print(track.lineEquation[0])
#             azimuth = findAzimuth(track.lineEquation[0])
#             print "distance", track.distance
#             zenith = findZenith(track.distance)
#             newAzAndZe = convert_to_world_frame(zenith, azimuth, i)
#             print"HIT"
#             print newAzAndZe[0]
#             d["Zenith"].append(newAzAndZe[0])
#             d["Azimuth"].append(newAzAndZe[1])
#             d["R2"].append(track.r2)
#             print newAzAndZe
#             hc.addAzimuth(newAzAndZe[0])
#             hc.addZenith(newAzAndZe[1])
# np.save('outFile2.npy', d)
# hc.plotAzimuth()
# hc.plotZenith()

d = np.load("outFile2.npy")
d = d.item()
i = 0
while i < len(d['R2']):
    if(d['R2'][i] >= .25):
        if(d['Zenith'][i] < 0 and d['Zenith'][i] >= -90):
            hc.addZenith(d['Zenith'][i] * -1)
        elif(d['Zenith'][i] < -90 and d['Zenith'][i] >= -180):
            hc.addZenith(180 + d['Zenith'][i])
        elif (d['Zenith'][i] < -180 and d['Zenith'][i] >= -270):
            hc.addZenith(180 - d['Zenith'][i])
        elif (d['Zenith'][i] < -270 and d['Zenith'][i] >= -360):
            hc.addZenith(360 + d['Zenith'][i])
        elif (d['Zenith'][i] > 0 and d['Zenith'][i] <= 90):
            hc.addZenith(d['Zenith'][i])
        elif (d['Zenith'][i] > 90 and d['Zenith'][i] <= 180):
            hc.addZenith(180 - d['Zenith'][i])
        elif (d['Zenith'][i] > 90 and d['Zenith'][i] <= 180):
            hc.addZenith(180 - d['Zenith'][i])
        elif (d['Zenith'][i] > 180 and d['Zenith'][i] <= 270):
            hc.addZenith(d['Zenith'][i] - 180)
        elif (d['Zenith'][i] > 270 and d['Zenith'][i] <= 360):
            hc.addZenith(360 - d['Zenith'][i])
    i += 1
hc.plotZenith()


#azimuth to tan then slope/ 1

