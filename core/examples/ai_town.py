from core.core import *
from core.state_machine import *

class AiTownSpawner(Engine):
    def awake(self):
        self.is_enabled = False
        self.priority_layer = 50

    def start(self):
        print("Start spawner")
        self.max_units = 100
        self.units = []
        self.coroutines = [
            Coroutine(func=self.spawn, interval=900, call_delay=1200, loop_condition=lambda: len(self.units) < self.max_units)
        ]

    def spawn(self):
        self.units.append(self.core.instantiate(DefaultAiUnit))
        print("Units Alive {}".format(len(self.units)))

##############################
#           prefab           #
##############################
class DefaultAiUnit(Engine):
    def awake(self):
        self.is_enabled = False

    def start(self):
        print("Start AI with id {}!".format(id(self)))
        self.countdown = 0
        self.pos = (random.randint(0, self.core.window_size[0]), random.randint(0, self.core.window_size[1]))
        self.size = 9
        self.destination_pos = (0, 0)
        self.move_range = 30

        self.surface = self.core.create_surface()

        idleState = State(name='idle', init=True, start=self.idle_start, update=self.idle_update, transitions=[Transition(lambda: self.countdown <= 0, 'walk')])
        movingState = State(name='walk', start=self.walk_start, update=self.walk_update, transitions=[Transition(lambda: self.steps_number <= 0, 'idle')])

        self.state_machines = [
            StateMachine([idleState, movingState])
        ]

    def update(self):
        self.surface.fill(self.core.background_color)
        pygame.draw.circle(self.surface, (200,29,235), self.pos, self.size)
        pygame.draw.circle(self.surface, (0,0,0), self.pos, self.size, width=3)
        self.core.draw_surface(self.surface)

    # idle state functions
    def idle_start(self):
        self.countdown = random.randint(1200, 3200)

    def idle_update(self):
        self.countdown = self.countdown - self.core.delta_time

    # walk state functions
    def walk_start(self):
        self.destination_pos = self.random_position_within_radius(self.pos, self.move_range)

        self.steps_number = max(abs(self.destination_pos[0] - self.pos[0]), abs(self.destination_pos[1] - self.pos[1]))

        self.step_x = float(self.destination_pos[0] - self.pos[0]) / self.steps_number
        self.step_y = float(self.destination_pos[1] - self.pos[1]) / self.steps_number

    def walk_update(self):
        self.pos = (self.pos[0]+self.step_x, self.pos[1]+self.step_y)
        self.steps_number = self.steps_number - 1

    def random_position_within_radius(self, center, radius):
        min_distance = radius * 0.2
        new_position = center

        while True:
            distance = random.uniform(min_distance, radius)
            angle = random.uniform(0, 2 * math.pi)

            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)

            if self.size <= x <= self.core.window_size[0]-self.size and self.size <= y <= self.core.window_size[1]-self.size:
                new_position = (x, y)
                break

        return new_position
