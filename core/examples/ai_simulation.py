from core.core import *
from core.state_machine import *


FOOD_POSITIONS = []

class AiSimulationSpawner(Engine):
    def awake(self):
        self.is_enabled = False
        self.priority_layer = 50

    def start(self):
        print("Start spawner")
        self.max_units = 100
        self.units = []
        self.surface = self.core.create_surface()
        self.coroutines = [
            Coroutine(func=self.spawn_unit, interval=900, call_delay=1200),
            Coroutine(func=self.spaw_food, interval=1100, call_delay=6000)
        ]

    def update(self):
        for food_pos in FOOD_POSITIONS:
            pygame.draw.circle(self.surface, (79, 213, 142), food_pos, 5)
        self.core.draw_surface(self.surface)
        self.surface.fill(self.core.background_color)

    def spaw_food(self):
        FOOD_POSITIONS.append((random.randint(0, self.core.window_size[0]-15), random.randint(0, self.core.window_size[1]-15)))

    def spawn_unit(self):
        for unit in self.units:
            if unit.is_dead:
                self.units.remove(unit)

        if len(self.units) < self.max_units:
            sim = self.core.instantiate(SimulationAiUnit)
            self.units.append(sim)
            sim.surface = self.surface
            print("Units Alive {}".format(len(self.units)))


##############################
#           prefab           #
##############################
class SimulationAiUnit(Engine):
    def awake(self):
        self.is_enabled = False

    def start(self):
        print("Start AI with id {}!".format(id(self)))
        self.countdown = 0
        self.pos = (random.randint(0, self.core.window_size[0]), random.randint(0, self.core.window_size[1]))
        self.size = 9
        self.destination_pos = (0, 0)
        self.move_range = 30
        self.view_range = 200
        self.age = 0
        self.max_age = 200
 
        self.stomach = 20
        self.surface = None
        self.found_food_pos = None
        self.is_dead = False

        self.font = pygame.font.SysFont('arialblack', 12)

        idleState = State(name='idle', init=True, start=self.idle_start, update=self.idle_update, transitions=[Transition(lambda: self.found_food_pos != None, 'hunt'), Transition(lambda: self.countdown <= 0, 'walk')])
        movingState = State(name='walk', start=self.walk_start, update=self.walk_update, transitions=[Transition(lambda: self.found_food_pos != None, 'hunt'), Transition(lambda: self.steps_number <= 0, 'idle')])
        huntState = State(name='hunt', start=self.hunt_start, update=self.hunt_update, transitions=[Transition(lambda: self.steps_number <= 0 or self.found_food_pos == None, 'walk')])

        self.machine = StateMachine([idleState, movingState, huntState])

        self.state_machines = [
            self.machine
        ]

        self.coroutines = [
            Coroutine(func=self.older_tick, interval=2000),
            Coroutine(func=self.stomach_tick, interval=1000)
        ]

    def update(self):
        if self.surface is not None:
            pygame.draw.circle(self.surface, (200,(self.age/self.max_age)*255,235), self.pos, self.size)
            r = 0
            pygame.draw.circle(self.surface, (0, 0, 0), self.pos, self.size+1, width=5)
            if self.stomach > 0:
                factor = (self.stomach/20)
                if factor > 1.0:
                    factor = 1
                hunger = 255 - (255 * factor)
                r = hunger
            else:
                r = 255
            pygame.draw.circle(self.surface, (r,0,0), self.pos, self.size, width=3)

            text_surface = self.font.render(' {} '.format(self.age), False, (123, 166, 222), (26, 70, 128))
            self.surface.blit(text_surface, (self.pos[0]-(text_surface.get_width()/2), self.pos[1]+10))

    def older_tick(self):
        self.age = self.age + 5
        if self.age >= self.max_age:
            self.core.destroy(self)
            self.is_dead = True

    def stomach_tick(self):
        self.stomach = self.stomach - 1
        if self.stomach <= 0:
            self.core.destroy(self)
            self.is_dead = True

    def search_food(self):
        found_food = None
        distance = -1
        for food_pos in FOOD_POSITIONS:
            cur_dis = math.dist(food_pos, self.pos)
            if cur_dis <= self.view_range:
                if distance == -1 or cur_dis < distance:
                    found_food = food_pos
                    distance = cur_dis

        return found_food


    # hunt state functions
    def hunt_start(self):
        self.destination_pos = self.found_food_pos

        self.steps_number = max(abs(self.destination_pos[0] - self.pos[0]), abs(self.destination_pos[1] - self.pos[1]))

        self.step_x = float(self.destination_pos[0] - self.pos[0]) / self.steps_number
        self.step_y = float(self.destination_pos[1] - self.pos[1]) / self.steps_number

    def hunt_update(self):
        self.pos = (self.pos[0]+self.step_x, self.pos[1]+self.step_y)
        self.steps_number = self.steps_number - 1
        food = self.search_food()
        if food != None and food != self.found_food_pos:
            self.found_food_pos = food
            self.machine.activate_state('hunt') # reactivate couse of new food found
        if self.found_food_pos not in FOOD_POSITIONS:
            self.found_food_pos = None
        else:
            if math.dist(self.found_food_pos, self.pos) <= 1:
                if self.found_food_pos in FOOD_POSITIONS: # eat
                    FOOD_POSITIONS.remove(self.found_food_pos)
                    self.stomach = self.stomach + 20
                    self.max_age = self.max_age + 3
                    self.found_food_pos = None


    # idle state functions
    def idle_start(self):
        self.countdown = random.randint(1200, 3200)

    def idle_update(self):
        self.countdown = self.countdown - self.core.delta_time
        self.found_food_pos = self.search_food()

    # walk state functions
    def walk_start(self):
        self.destination_pos = self.random_position_within_radius(self.pos, self.move_range)

        self.steps_number = max(abs(self.destination_pos[0] - self.pos[0]), abs(self.destination_pos[1] - self.pos[1]))

        self.step_x = float(self.destination_pos[0] - self.pos[0]) / self.steps_number
        self.step_y = float(self.destination_pos[1] - self.pos[1]) / self.steps_number

    def walk_update(self):
        self.pos = (self.pos[0]+self.step_x, self.pos[1]+self.step_y)
        self.steps_number = self.steps_number - 1
        self.found_food_pos = self.search_food()

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

