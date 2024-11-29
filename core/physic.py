from core.core import *
from core.math import *

def addVectors(v1: tuple, v2: tuple): # (angle_radians, length)
    """ Returns the sum of two vectors """

    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x * p1.mass + p2.x * p2.mass) / total_mass
        p1.y = (p1.y * p1.mass + p2.y * p2.mass) / total_mass
        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed * p1.mass / total_mass),
                                          (p2.angle, p2.speed * p2.mass / total_mass))
        p1.speed = p1.speed * (p1.elasticity * p2.elasticity)
        p1.mass = p1.mass + p2.mass
        p1.collide_with = p2


def collide(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce, i.e. update their angle, speed and position """
# TODO collision auf die pygame rect collision umstellen, generell modul auf pygame standarts ändern
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass),
                                          (angle, 2 * p2.speed * p2.mass / total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass),
                                          (angle + math.pi, 2 * p1.speed * p1.mass / total_mass))
        elasticity = p1.elasticity * p2.elasticity
        p1.speed = p1.speed * elasticity
        p2.speed = p2.speed * elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x = p1.x + (math.sin(angle) * overlap)
        p1.y = p1.y - (math.cos(angle) * overlap)
        p2.x = p2.x - (math.sin(angle) * overlap)
        p2.y = p2.y + (math.cos(angle) * overlap)


class PhysicBody:
    def __init__(self, position, size, mass=1, gravity: pygame.math.Vector2 = None):
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
        self.gravity_v = gravity

    def update(self):
        """ Update position based on speed, angle """
        move_v = pygame.math.Vector2()
        move_v.from_polar((self.speed, math.degrees(self.angle)))
        if self.gravity_v is not None:
            (self.angle, self.speed) = vec_as_polar(move_v, self.gravity_v)
        self.x = self.x + (math.sin(self.angle) * self.speed)
        self.y = self.y - (math.cos(self.angle) * self.speed)

    def update_drag(self):
        self.speed = self.speed * self.drag

    def move_to(self, position):
        """ Change angle and speed to move towards a given point """

        dx = position[0] - self.x
        dy = position[1] - self.y
        self.angle = 0.5 * math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

    def accelerate(self, vector):
        """ Change angle and speed by a given vector """
        (self.angle, self.speed) = addVectors((self.angle, self.speed), vector)

    def attract(self, other):
        """" Change velocity based on gravatational attraction between two particle"""

        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist = math.hypot(dx, dy)

        if dist < self.size + other.size:
            return True

        theta = math.atan2(dy, dx)
        force = 0.1 * self.mass * other.mass / dist ** 2
        self.accelerate((theta - 0.5 * math.pi, force / self.mass))
        other.accelerate((theta + 0.5 * math.pi, force / other.mass))


class Spring:
    def __init__(self, p1, p2, length=50, strength=0.5):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.strength = strength

    def update(self):
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        force = (self.length - dist) * self.strength

        self.p1.accelerate((theta + 0.5 * math.pi, force / self.p1.mass))
        self.p2.accelerate((theta - 0.5 * math.pi, force / self.p2.mass))


class Space:
    """ Defines the boundary of a simulation and its properties """

    def __init__(self,
                 size: tuple,
                 gravity: tuple = None,
                 collision_enabled=True,
                 bounce_enabled=True,
                 attract_enabled=False,
                 combine_enabled=False
                 ):
        self.width = size[0]
        self.height = size[1]
        self.gravity = gravity
        self.bodies = []
        self.springs = []

        self.color = (255, 255, 255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = (0, 0)

        self.collision_enabled = collision_enabled
        self.bounce_enabled = bounce_enabled
        self.attract_enabled = attract_enabled
        self.combine_enabled = combine_enabled


    def update(self):
        for i, body in enumerate(self.bodies, 1):
            if self.bounce_enabled:
                self.bounce(body)
            #body.accelerate(self.acceleration)
            for body2 in self.bodies[i:]:
                if body != body2:
                    if self.collision_enabled:
                        collide(body, body2)
                    if self.combine_enabled:
                        combine(body, body2)
                    if self.attract_enabled:
                        body.attract(body2)
            body.update_drag()
            body.update()

        for spring in self.springs:
            spring.update()

    def create_body(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """
        induction_created_bodies = []
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            physic_body = PhysicBody((x, y), size, mass)
            physic_body.speed = kargs.get('speed', random.random())
            physic_body.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            physic_body.color = kargs.get('color', (0, 0, 255))
            physic_body.elasticity = kargs.get('elasticity', self.elasticity)
            physic_body.drag = (physic_body.mass / (physic_body.mass + self.mass_of_air)) ** physic_body.size

            if self.gravity is not None:
                gravity_direction_v = pygame.math.Vector2(x=self.gravity[0], y=self.gravity[1])
                gravity_direction_v.from_polar((gravity_direction_v.length(), math.degrees(0.5 * math.pi - math.atan2(y, x))))
                if gravity_direction_v.length() > 0:
                    gravity_direction_v = gravity_direction_v.normalize()

                physic_body.gravity_v = gravity_direction_v

            induction_created_bodies.append(physic_body)
            self.bodies.append(physic_body)

        return induction_created_bodies


    def set_gravity(self, x=0, y=0):
        """ y=1 -> up; y=-1 -> down; x=-1 -> left; x=1 -> right; the number declare the strength """
        direction_v = pygame.math.Vector2(x=x, y=y)
        direction_v.from_polar((direction_v.length(), math.degrees(0.5 * math.pi - math.atan2(y,x))))
        if direction_v.length() > 0:
            direction_v = direction_v.normalize()
        print(direction_v)
        for i, particle in enumerate(self.bodies, 1):
            particle.gravity_v = direction_v

    def addSpring(self, p1, p2, length=50, strength=0.5):
        """ Add a spring between particles p1 and p2 """
        self.springs.append(Spring(self.bodies[p1], self.bodies[p2], length, strength))

    def bounce(self, body):
        """ Tests whether a particle has hit the boundary of the environment """
        if body.x > self.width - body.size:
            body.x = 2 * (self.width - body.size) - body.x
            body.angle = - body.angle
            body.speed = body.speed * body.elasticity

        elif body.x < body.size:
            body.x = 2 * body.size - body.x
            body.angle = - body.angle
            body.speed = body.speed * body.elasticity

        if body.y > self.height - body.size:
            body.y = 2 * (self.height - body.size) - body.y
            body.angle = math.pi - body.angle
            body.speed = body.speed * body.elasticity

        elif body.y < body.size:
            body.y = 2 * body.size - body.y
            body.angle = math.pi - body.angle
            body.speed = body.speed * body.elasticity

    def get_body_at_pos(self, position):
        """ Returns any particle that occupies position x, y """

        for body in self.bodies:
            if math.hypot(body.x - position[0], body.y - position[1]) <= body.size:
                return body
        return None




# https://github.com/petercollingridge/code-for-blog/tree/master/pygame%20physics%20simulation

#test_v1 = pygame.math.Vector2(x=1, y=1)
#test_v2 = pygame.math.Vector2(x=5, y=5)
#
def vec_as_polar(v1: pygame.math.Vector2, v2: pygame.math.Vector2):
    v3 = v1 + v2
    r, phi = v3.as_polar()
    return (math.radians(phi), r)

#print("vec_as_polar", vec_as_polar(test_v1, test_v2))
#
#v1 = (math.atan2(test_v1.x, test_v1.y), test_v1.length())
#v2 = (math.atan2(test_v2.x, test_v2.x), test_v2.length())
#print("addVectors", addVectors(v1, v2))
#
#re_v = pygame.math.Vector2(x=0, y=0)
#print(test_v1.as_polar())
#re_v.from_polar(test_v1.as_polar())
#
#print(re_v.x, re_v.y)

