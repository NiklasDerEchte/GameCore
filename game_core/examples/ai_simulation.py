from game_core.core import *

#######################################
# implements also the NavAgent module #
#######################################

FOOD_UNITS = []
AI_UNITS = []

class AiSimulationSpawner(Engine, Prefab):
    def awake(self):
        self.priority_layer = 50

    def start(self):
        self.max_units = 100
        self.surface = self.core.create_surface()
        self.coroutines = [
            Coroutine(func=self.spawn_unit, interval=900, call_delay=1200),
            Coroutine(func=self.spawn_food, interval=1100, call_delay=6000)
        ]
        self.fog = self.core.instantiate(Fog)
        self.core.instantiate(StatsDisplay)
        self.fog.enable()

    def update(self):
        if self.fog.is_enabled:
            for unit in AI_UNITS:
                self.fog.erase((unit.agent.position[0], unit.agent.position[1] + 8), 20)

        self.core.draw_surface(self.surface)
        self.surface.fill(self.core.background_color)

    def spawn_food(self):
        for unit in FOOD_UNITS:
            if unit.is_dead:
                self.core.destroy(unit)
                FOOD_UNITS.remove(unit)
        food_unit = self.core.instantiate(FoodAiUnit)
        food_unit.surface = self.surface
        FOOD_UNITS.append(food_unit)

    def spawn_unit(self):
        for unit in AI_UNITS:
            if unit.is_dead:
                AI_UNITS.remove(unit)

        if len(AI_UNITS) < self.max_units:
            sim = self.core.instantiate(SimulationAiUnit)
            AI_UNITS.append(sim)
            sim.surface = self.surface


##############################
#           prefab           #
##############################
class FoodAiUnit(Engine, Prefab):
    def start(self):
        self.countdown = 0
        self.size = 5
        self.move_range = 7
        self.view_range = 12
        self.surface = None
        self.is_dead = False

        self.agent = NavAgent(position=(random.randint(0, self.core.window_size[0]), random.randint(0, self.core.window_size[1])), speed=.75)

        self.destination_pos = self.random_position_within_radius(self.agent.position, self.move_range)

    def update(self):
        self.agent.move(destination=self.destination_pos)
        if self.agent.distance <= 1:
            self.destination_pos = self.random_position_within_radius(self.agent.position, self.move_range)
        closest_unit = self.search_closest_enemy()
        if closest_unit != None:
            dir = direction(closest_unit.agent.position, self.agent.position)

            self.destination_pos = (
            self.agent.position[0] + dir[0] * self.move_range, self.agent.position[1] + dir[1] * self.move_range)
            self.destination_pos = (round_clamp(self.destination_pos[0], 0+1, self.core.window_size[0]-1),
                                    round_clamp(self.destination_pos[1], 0+1, self.core.window_size[1]-1))
        if self.surface != None:
            pygame.draw.circle(self.surface, (79, 213, 142), self.agent.position, self.size)

    def random_position_within_radius(self, center, radius):
        min_distance = radius * 0.2
        new_position = center

        while True:
            distance = random.uniform(min_distance, radius)
            angle = random.uniform(0, 2 * math.pi)

            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)

            if self.size <= x <= self.core.window_size[0] - self.size and self.size <= y <= self.core.window_size[1] - self.size:
                new_position = (x, y)
                break

        return new_position

    def search_closest_enemy(self):
        closest_unit = None
        unit_distance = 0
        for unit in AI_UNITS:
            dist = distance(self.agent.position, unit.agent.position)
            if dist <= self.view_range:
                if closest_unit == None:
                    closest_unit = unit
                    unit_distance = dist
                else:
                    if dist < unit_distance:
                        closest_unit = unit
                        unit_distance = dist
        return closest_unit



##############################
#           prefab           #
##############################
class SimulationAiUnit(Engine, Prefab):

    def start(self):
        self.countdown = 0
        self.agent = NavAgent(
            position=(random.randint(0, self.core.window_size[0]), random.randint(0, self.core.window_size[1])))
        self.size = 9
        self.destination_pos = (0, 0)
        self.move_range = 30
        self.view_range = 80
        self.age = 0
        self.max_age = 200

        self.stomach = 20
        self.surface = None
        self.found_food_unit = None
        self.is_dead = False

        self.font = pygame.font.SysFont('arialblack', 12)

        idleState = State(name='idle', init=True, start=self.idle_start, update=self.idle_update,
                          transitions=[Transition(lambda: self.found_food_unit != None, 'hunt'),
                                       Transition(lambda: self.countdown <= 0, 'walk')])
        movingState = State(name='walk', start=self.walk_start, update=self.walk_update,
                            transitions=[Transition(lambda: self.found_food_unit != None, 'hunt'),
                                         Transition(lambda: self.agent.distance <= 1, 'idle')])
        huntState = State(name='hunt', update=self.hunt_update, transitions=[
            Transition(lambda: self.agent.distance <= 1 or self.found_food_unit == None, 'walk')])

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
            pygame.draw.circle(self.surface, (200, (self.age / self.max_age) * 255, 235), self.agent.position,
                               self.size)
            r = 0
            pygame.draw.circle(self.surface, (0, 0, 0), self.agent.position, self.size + 1, width=5)
            if self.stomach > 0:
                factor = (self.stomach / 20)
                if factor > 1.0:
                    factor = 1
                hunger = 255 - (255 * factor)
                r = hunger
            else:
                r = 255
            self.agent.position = (clamp(self.agent.position[0], 0+1, self.core.window_size[0]-1), clamp(self.agent.position[1], 0+1, self.core.window_size[1]-1))
            pygame.draw.circle(self.surface, (r, 0, 0), self.agent.position, self.size, width=3)

            text_surface = self.font.render(' {} '.format(self.age), False, (123, 166, 222), (26, 70, 128))
            self.surface.blit(text_surface,
                              (self.agent.position[0] - (text_surface.get_width() / 2), self.agent.position[1] + 10))

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

    # hunt state functions
    def hunt_update(self):
        self.agent.move(destination=self.found_food_unit.agent.position)

        food = self.search_food()
        if food != None and id(food) != id(self.found_food_unit):
            self.found_food_unit = food
        if self.found_food_unit.is_dead:
            self.found_food_unit = None
        else:
            if distance(self.agent.position, self.found_food_unit.agent.position) <= 1:
                self.eat()

    def eat(self):
        for unit in FOOD_UNITS:
            if id(unit) == id(self.found_food_unit):
                self.core.destroy(self.found_food_unit)
                FOOD_UNITS.remove(self.found_food_unit)
                self.stomach = self.stomach + 20
                self.max_age = self.max_age + 3
                self.found_food_unit = None

    # idle state functions
    def idle_start(self):
        self.countdown = random.randint(600, 3200)

    def idle_update(self):
        self.countdown = self.countdown - self.core.delta_time
        self.found_food_unit = self.search_food()

    # walk state functions
    def walk_start(self):
        self.destination_pos = self.random_position_within_radius(self.agent.position, self.move_range)

    def walk_update(self):
        self.agent.move(destination=self.destination_pos)
        self.found_food_unit = self.search_food()

    def random_position_within_radius(self, center, radius):
        min_distance = radius * 0.2
        new_position = center

        while True:
            distance = random.uniform(min_distance, radius)
            angle = random.uniform(0, 2 * math.pi)

            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)

            if self.size <= x <= self.core.window_size[0] - self.size and self.size <= y <= self.core.window_size[1] - self.size:
                new_position = (x, y)
                break

        return new_position

    def search_food(self):
        found_unit = None
        dist = -1
        for food_unit in FOOD_UNITS:
            cur_dis = distance(self.agent.position, food_unit.agent.position)
            if cur_dis <= self.view_range and food_unit.is_dead == False:
                if dist == -1 or cur_dis < dist:
                    found_unit = food_unit
                    dist = cur_dis

        return found_unit


class StatsDisplay(Engine, Prefab):
    def awake(self):
        self.priority_layer = 81

    def start(self):
        self.font = pygame.font.SysFont('Arial Black', 24)
        self.surface = self.core.create_surface()

    def update(self):
        self.surface.blit(self.font.render("Food Ai alive {}".format(len(FOOD_UNITS)), False, (0, 0, 0)), (10, 6))
        self.surface.blit(self.font.render("Units alive {}".format(len(AI_UNITS)), False, (0, 0, 0)), (10, 26))

        self.core.draw_surface(self.surface)
        self.surface.fill(self.core.background_color)

