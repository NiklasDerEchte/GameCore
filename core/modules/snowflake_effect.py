from core.core import *
class SnowflakeEffect(Engine):
    def awake(self):
        self.is_enabled = False
        self.priority_layer = 2

    def start(self):
        self.surface = self.core.create_surface()

        # config props
        self.flakes_size_range = (1, 2) # blink fx range
        self.flakes_move_range = 2 # higher is wider
        self.flake_wiggle_speed = 4 # lower is faster
        self.flakes_fall_speed = 2 # higher is faster

        # private props
        self._flakes = []
        self._spawn_timer = 0

    def update(self):
        self.core.draw_surface(self.surface)

    def fixed_update(self):
        # print("{}ms | {}s".format(core.elapsed_delta_time, core.elapsed_time_seconds))
        self.surface.fill(self.core.background_color)
        self.spawn_timer = self._spawn_timer - self.core.delta_time
        if self.spawn_timer <= 0:
            self.spawn_timer = random.randint(1, 4)
            self._flakes.append((random.randint(0, self.core.window_size[0]+1), random.randint(0, 25)))

        removingFlakes = []
        for i in range(len(self._flakes)):
            position = self._flakes[i]
            wiggle = round((math.sin(position[1]/self.flake_wiggle_speed) * self.flakes_move_range), 2)
            next_x = position[0]+wiggle
            next_y = position[1]+self.flakes_fall_speed
            if next_x < 0:
                next_x = 0
            if next_x > self.core.window_size[0]:
                next_x = self.core.window_size[0] - 1

            pygame.draw.circle(self.surface, (180, 207, 250), (position[0], position[1]), random.randint(self.flakes_size_range[0], self.flakes_size_range[1]))

            position = (round(next_x), round(next_y))
            if position[1] > self.core.window_size[1]:
                removingFlakes.append(i)
            else:
                self._flakes[i] = position

        for i in removingFlakes:
            del self._flakes[i]

