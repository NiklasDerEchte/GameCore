import math

def distance(p1, p2):
    p_d = (math.fabs(p2[0] - p1[0]), math.fabs(p2[1] - p1[1]))
    return math.sqrt((p_d[0] ** 2) + (p_d[1] ** 2))


def direction(p1, p2):
    p_d = (p2[0] - p1[0], p2[1] - p1[1])
    dist = math.sqrt((p_d[0] ** 2) + (p_d[1] ** 2))
    return (p_d[0]/dist, p_d[1]/dist)

def clamp(n, min_n, max_n):
    return max(min(n, max_n), min_n)

def round_clamp(n, min_n, max_n, r=2):
    return round(max(min(n, max_n), min_n), r)