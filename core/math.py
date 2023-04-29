import math

def dist(p1, p2):
    p_d = (p2[0] - p1[0], p2[1] - p1[1])
    return math.sqrt((p_d[0] ** 2) + (p_d[1] ** 2))