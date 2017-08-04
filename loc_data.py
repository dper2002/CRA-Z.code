import numpy as np
import math
from purge_zeros import deco

# pitch creates a matrix that effects a pitch by a given angle
# (similarly for roll and yaw functions)


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
    while True:
        if deco.iloc[n]["event_id"] == image_name:
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
