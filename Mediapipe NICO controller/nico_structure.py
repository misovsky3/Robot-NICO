import numpy as np


# functions for converting angles to NICO's ranges

def convert_r_shoulder_fwd_bwd(value):
    return np.interp(value, [100, 200], [12, 4088])


def convert_r_shoulder_left_right(value):
    return np.interp(value, [100, 200], [12, 4088])


def convert_r_elbow(value):
    return np.interp(value, [100, 200], [12, 4088])


def convert_r_wrist_rotate(value):
    return np.interp(value, [100, 200], [12, 4088])


def convert_r_wrist_left_right(value):
    return int(np.interp(value, [115, 160], [15, 4090]))


def convert_r_index_finger(value):
    return int(np.interp(value, [52, 167], [3000, 8]))


def convert_r_other_fingers(value):
    return int(np.interp(value, [32, 168], [3000, 0]))


def convert_r_thumb_lift(value):
    return int(np.interp(value, [41, 76], [4000, 0]))


def convert_r_thumb_close(value):
    return int(np.interp(value, [97, 155], [3000, 0]))
