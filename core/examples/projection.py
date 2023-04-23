from core.core import *

class Projection(Engine):

    def awake(self):
        self.is_enabled = False
        self.priority_layer = 5

    def start(self):
        self.TRANSPARENT_BG = (0, 0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)

        self.scale = 100

        self.circle_pos = [self.core.window_size[0]/2, self.core.window_size[1]/2]  # x, y

        self.angle = 0

        self.points = []

        # all the cube vertices
        self.points.append(np.matrix([-1, -1, 1]))
        self.points.append(np.matrix([1, -1, 1]))
        self.points.append(np.matrix([1,  1, 1]))
        self.points.append(np.matrix([-1, 1, 1]))
        self.points.append(np.matrix([-1, -1, -1]))
        self.points.append(np.matrix([1, -1, -1]))
        self.points.append(np.matrix([1, 1, -1]))
        self.points.append(np.matrix([-1, 1, -1]))

        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])

        self.projected_points = [
            [n, n] for n in range(len(self.points))
        ]
        self.surface = self.core.create_surface()

    def connect_points(self, i, j, points):
        pygame.draw.line(self.surface, self.BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

    def update(self):
        rotation_z = np.matrix([
            [math.cos(self.angle), -math.sin(self.angle), 0],
            [math.sin(self.angle), math.cos(self.angle), 0],
            [0, 0, 1],
        ])

        rotation_y = np.matrix([
            [math.cos(self.angle), 0, math.sin(self.angle)],
            [0, 1, 0],
            [-math.sin(self.angle), 0, math.cos(self.angle)],
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, math.cos(self.angle), -math.sin(self.angle)],
            [0, math.sin(self.angle), math.cos(self.angle)],
        ])
        self.angle += 0.01

        self.surface.fill(self.TRANSPARENT_BG)
        # drawining stuff

        i = 0
        for point in self.points:
            rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)

            projected2d = np.dot(self.projection_matrix, rotated2d)

            x = int(projected2d[0][0] * self.scale) + self.circle_pos[0]
            y = int(projected2d[1][0] * self.scale) + self.circle_pos[1]

            self.projected_points[i] = [x, y]
            pygame.draw.circle(self.surface, self.RED, (x, y), 5)
            i += 1

        for p in range(4):
            self.connect_points(p, (p+1) % 4, self.projected_points)
            self.connect_points(p+4, ((p+1) % 4) + 4, self.projected_points)
            self.connect_points(p, (p+4), self.projected_points)

        self.core.draw_surface(self.surface)
