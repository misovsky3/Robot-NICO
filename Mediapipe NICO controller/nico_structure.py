import numpy as np


def calculate_nico_joint(angle, angle_range, nico_joint_range ):
    x1, x2 = angle_range
    y1, y2 = nico_joint_range

    if angle < x1:
        return y1
    if angle > x2:
        return y2


    k = (y2 - y1) / (x2 - x1)
    q = y1 - (k * x1)
    y = k * angle + q

    
    return round(y)


# functions for converting angles to NICO's ranges

def convert_r_shoulder_fwd_bwd(value):
    return calculate_nico_joint(value, [100, 200], [12, 4088])


def convert_r_shoulder_left_right(value):
    return calculate_nico_joint(value, [100, 200], [12, 4088])


def convert_r_elbow(value):
    return calculate_nico_joint(value, [100, 200], [12, 4088])


def convert_r_wrist_rotate(value):
    return calculate_nico_joint(value, [100, 200], [12, 4088])


def convert_r_wrist_left_right(value):
    return calculate_nico_joint(value, [115, 160], [15, 4090])


def convert_r_index_finger(value):
    return calculate_nico_joint(value, [52, 167], [3000, 8])


def convert_r_other_fingers(value):
    return calculate_nico_joint(value, [32, 168], [3000, 0])


def convert_r_thumb_lift(value):
    return calculate_nico_joint(value, [41, 76], [4000, 0])


def convert_r_thumb_close(value):
    return calculate_nico_joint(value, [97, 155], [3000, 0])
