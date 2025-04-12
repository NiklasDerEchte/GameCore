import math
import random

def get_center(top_left_position, width, height):
    return (top_left_position[0]-(width/2), top_left_position[1]-(height/2))


def distance(p1, p2):
    p_d = (math.fabs(p2[0] - p1[0]), math.fabs(p2[1] - p1[1]))
    return math.sqrt((p_d[0] ** 2) + (p_d[1] ** 2))

def direction(p1, p2):
    p_d = (p2[0] - p1[0], p2[1] - p1[1])
    dist = math.sqrt((p_d[0] ** 2) + (p_d[1] ** 2))
    return (p_d[0]/dist, p_d[1]/dist)

def angle_degree(p1, p2):
    d = direction(p1, p2)
    rad = math.atan2(d[1], d[0])
    if rad == 0.0:
        return 0
    deg = rad / math.pi * 180
    return deg

def clamp(n, min_n, max_n):
    return max(min(n, max_n), min_n)

def round_clamp(n, min_n, max_n, r=2):
    return round(max(min(n, max_n), min_n), r)

def random_position_within_radius(center, size, radius, max_width, max_height):
    min_distance = radius * 0.2
    new_position = center

    while True:
        distance = random.uniform(min_distance, radius)
        angle = random.uniform(0, 2 * math.pi)

        x = center[0] + distance * math.cos(angle)
        y = center[1] + distance * math.sin(angle)

        if size <= x <= max_width - size and size <= y <= max_height - size:
            new_position = (x, y)
            break
    return new_position

def random_position_in_ellipse_with_size(width, height):
    rho = random.uniform(0.0, 1.0)
    phi = random.uniform(0.0, 2.0*math.pi)

    x = math.sqrt(rho) * math.cos(phi)
    y = math.sqrt(rho) * math.sin(phi)

    x = x * (width / 2.0)
    y = y * (height / 2.0)
    return (x, y)