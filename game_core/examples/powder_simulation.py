from game_core.src import *
import random
from enum import Enum

class Material(Enum):
    EMPTY = 0
    SAND = 1
    WATER = 2
    STONE = 3
    WOOD = 4
    FIRE = 5
    SMOKE = 6
    PLANT = 7
    ICE = 8
    ACID = 9

class PowderSimulationPrefab(Engine):
    
    def awake(self, width=300, height=300):
        self.width = width
        self.height = height
        self.cell_size = 3
        self.grid = None
        self.temp_grid = None
        self.color_map = {
            Material.EMPTY: (0, 0, 0, 0),
            Material.SAND: (194, 178, 128),
            Material.WATER: (64, 164, 223, 150),
            Material.STONE: (128, 128, 128),
            Material.WOOD: (101, 67, 33),
            Material.FIRE: (226, 88, 34),
            Material.SMOKE: (100, 100, 100, 150),
            Material.PLANT: (34, 139, 34),
            Material.ICE: (200, 200, 255, 180),
            Material.ACID: (100, 255, 50, 200)
        }
        self.current_material = Material.SAND
        self.simulation_speed = 3
        self.is_running = True
        self.surface = None
        self.brush_size = 5
        self.show_debug = False
        self.frames_since_last_update = 0
        self.update_interval = 1
    
        self.density_map = {
            Material.EMPTY: 0,
            Material.SAND: 5,
            Material.WATER: 2,
            Material.STONE: 10,
            Material.WOOD: 3,
            Material.FIRE: -1,
            Material.SMOKE: -2,
            Material.PLANT: 2,
            Material.ICE: 3,
            Material.ACID: 2
        }
        
        self.flammability = {
            Material.WOOD: 0.8,
            Material.PLANT: 0.9,
            Material.ICE: 0.0,
            Material.SAND: 0.0,
            Material.STONE: 0.0,
            Material.WATER: 0.0,
            Material.ACID: 0.3
        }

        self.melting_point = {
            Material.ICE: 5,
            Material.WOOD: 200
        }
        
        self.burn_duration = {
            Material.WOOD: 300,
            Material.PLANT: 150,
            Material.ACID: 50
        }

    def start(self):
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.grid = [[Material.EMPTY for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        self.temp_grid = [[0.0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        self.surface = self.core.create_layer_surface(width=self.width, height=self.height)
        
        for x in range(self.cell_width):
            self._set_material(x, 0, Material.STONE)
            self._set_material(x, self.cell_height-1, Material.STONE)
        for y in range(self.cell_height):
            self._set_material(0, y, Material.STONE)
            self._set_material(self.cell_width-1, y, Material.STONE)
    
    def _place_material(self, x, y, material):
        radius = self.brush_size // 2
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                dist = dx*dx + dy*dy
                if dist <= radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
                        if material == Material.FIRE:
                            if self.grid[ny][nx] in self.flammability and self.flammability[self.grid[ny][nx]] > 0:
                                self._set_material(nx, ny, material)
                                self.temp_grid[ny][nx] = 300
                        else:
                            self._set_material(nx, ny, material)
    
    def _set_material(self, x, y, material):
        self.grid[y][x] = material
        if material in [Material.STONE, Material.WATER, Material.ICE]:
            self.temp_grid[y][x] = 0
    
    def _clear_grid(self):
        for y in range(1, self.cell_height-1):
            for x in range(1, self.cell_width-1):
                self._set_material(x, y, Material.EMPTY)
    
    def _randomize_grid(self):
        for y in range(1, self.cell_height-1):
            for x in range(1, self.cell_width-1):
                r = random.random()
                if r < 0.1:
                    self._set_material(x, y, Material.SAND)
                elif r < 0.2:
                    self._set_material(x, y, Material.WATER)
                elif r < 0.21:
                    self._set_material(x, y, Material.WOOD)
                elif r < 0.22:
                    self._set_material(x, y, Material.PLANT)
                else:
                    self._set_material(x, y, Material.EMPTY)
    
    def update(self):
        self._handle_keys()
        if not self.is_running:
            self._draw_grid()
            return
            
        self.frames_since_last_update += 1
        if self.frames_since_last_update < self.update_interval:
            self._draw_grid()
            return
            
        self.frames_since_last_update = 0
        
        for _ in range(self.simulation_speed):
            self._update_physics()
            self._update_temperature()
        
        self._draw_grid()

    def _handle_keys(self):
        if self.surface is not None:
            surface_offset = self.surface.get_offset()
            surface_pos = (
                self.core.mouse_position[0] - surface_offset[0],
                self.core.mouse_position[1] - surface_offset[1]
            )
            
            grid_x = int(surface_pos[0] // self.cell_size)
            grid_y = int(surface_pos[1] // self.cell_size)

            if 0 <= grid_x < self.cell_width and 0 <= grid_y < self.cell_height:
                if self.core.pressed_mouse[0]:
                    self._place_material(grid_x, grid_y, self.current_material)
                
                elif self.core.pressed_mouse[2]:
                    self._place_material(grid_x, grid_y, Material.EMPTY)
        
        for event in self.core.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.current_material = Material.SAND
                elif event.key == pygame.K_2: self.current_material = Material.WATER
                elif event.key == pygame.K_3: self.current_material = Material.STONE
                elif event.key == pygame.K_4: self.current_material = Material.WOOD
                elif event.key == pygame.K_5: self.current_material = Material.FIRE
                elif event.key == pygame.K_6: self.current_material = Material.PLANT
                elif event.key == pygame.K_7: self.current_material = Material.ICE
                elif event.key == pygame.K_8: self.current_material = Material.ACID

                elif event.key == pygame.K_SPACE: self.is_running = not self.is_running
                elif event.key == pygame.K_UP: self.simulation_speed = min(10, self.simulation_speed + 1)
                elif event.key == pygame.K_DOWN: self.simulation_speed = max(1, self.simulation_speed - 1)
                elif event.key == pygame.K_d: self.show_debug = not self.show_debug
                elif event.key == pygame.K_c: self._clear_grid()
                elif event.key == pygame.K_r: self._randomize_grid()

    
    def _update_physics(self):
        for y in range(self.cell_height-2, 0, -1):
            for x in range(1, self.cell_width-1):
                material = self.grid[y][x]
                
                if material == Material.SAND:
                    self._update_sand(x, y)
                elif material == Material.WATER:
                    self._update_water(x, y)
                elif material == Material.FIRE:
                    self._update_fire(x, y)
                elif material == Material.SMOKE:
                    self._update_smoke(x, y)
                elif material == Material.ICE:
                    self._update_ice(x, y)
                elif material == Material.ACID:
                    self._update_acid(x, y)
    
    def _update_sand(self, x, y):
        if self._try_move(x, y, 0, 1):
            return
            
        if random.random() < 0.5:
            if self._try_move(x, y, -1, 1) or self._try_move(x, y, 1, 1):
                return
        else:
            if self._try_move(x, y, 1, 1) or self._try_move(x, y, -1, 1):
                return
    
    def _update_water(self, x, y):
        if self._try_move(x, y, 0, 1):
            return
            
        directions = [-1, 1]
        random.shuffle(directions)
        
        for dx in directions:
            if self._try_move(x, y, dx, 0):
                return
                
        for dx in directions:
            if self._try_move(x, y, dx, 1):
                return
    
    def _update_fire(self, x, y):
        if self.temp_grid[y][x] <= 0:
            self._set_material(x, y, Material.EMPTY)
            return
            
        self.temp_grid[y][x] -= 1
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
                    neighbor_mat = self.grid[ny][nx]
                    
                    if neighbor_mat in self.flammability and random.random() < self.flammability[neighbor_mat]:
                        if neighbor_mat == Material.WOOD and self.temp_grid[ny][nx] < 100:
                            self.temp_grid[ny][nx] += 5
                        elif self.temp_grid[ny][nx] > 150 and random.random() < 0.1:
                            self._set_material(nx, ny, Material.FIRE)
                            self.temp_grid[ny][nx] = 200
                    
                    if neighbor_mat == Material.WATER and random.random() < 0.3:
                        self._set_material(x, y, Material.EMPTY)
                        self.temp_grid[y][x] = 0
                        if random.random() < 0.5:
                            self._set_material(nx, ny, Material.EMPTY)
                        return
        
        if y > 0 and self.grid[y-1][x] == Material.EMPTY and random.random() < 0.2:
            self._set_material(x, y-1, Material.FIRE)
            self.temp_grid[y-1][x] = self.temp_grid[y][x] * 0.9
        
        if random.random() < 0.05:
            if y > 0 and self.grid[y-1][x] == Material.EMPTY:
                self._set_material(x, y-1, Material.SMOKE)
    
    def _update_smoke(self, x, y):
        if y > 0 and self._try_move(x, y, 0, -1):
            return
        
        directions = [-1, 1]
        random.shuffle(directions)
        for dx in directions:
            if self._try_move(x, y, dx, -1):
                return
                
        if random.random() < 0.1:
            self._set_material(x, y, Material.EMPTY)
    
    def _update_ice(self, x, y):
        if self.temp_grid[y][x] > self.melting_point[Material.ICE]:
            self._set_material(x, y, Material.WATER)
    
    def _update_acid(self, x, y):
        if random.random() < 0.3:
            directions = [(0, 1), (-1, 0), (1, 0), (-1, 1), (1, 1)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
                    neighbor_mat = self.grid[ny][nx]
                    if neighbor_mat in [Material.STONE, Material.WOOD, Material.PLANT]:
                        if random.random() < 0.5:
                            self._set_material(nx, ny, Material.EMPTY)
                        break
        
        if self._try_move(x, y, 0, 1):
            return
            
        directions = [-1, 1]
        random.shuffle(directions)
        for dx in directions:
            if self._try_move(x, y, dx, 0):
                return
            if self._try_move(x, y, dx, 1):
                return
    
    def _try_move(self, x, y, dx, dy):
        nx, ny = x + dx, y + dy
        
        if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
            current_mat = self.grid[y][x]
            target_mat = self.grid[ny][nx]
        
            if (target_mat == Material.EMPTY or 
                (self.density_map[current_mat] > self.density_map[target_mat] and 
                 target_mat not in [Material.STONE, Material.ICE])):
                
                self.grid[y][x], self.grid[ny][nx] = self.grid[ny][nx], self.grid[y][x]
                self.temp_grid[y][x], self.temp_grid[ny][nx] = self.temp_grid[ny][nx], self.temp_grid[y][x]
                return True
                
        return False
    
    def _update_temperature(self):
        new_temp = [row[:] for row in self.temp_grid]
        
        for y in range(1, self.cell_height-1):
            for x in range(1, self.cell_width-1):
                if self.grid[y][x] == Material.EMPTY:
                    continue
                    
                temp_sum = 0
                count = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                            
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.cell_width and 0 <= ny < self.cell_height:
                            temp_sum += self.temp_grid[ny][nx]
                            count += 1
                
                if count > 0:
                    avg_temp = temp_sum / count
                    if self.grid[y][x] in [Material.STONE, Material.WOOD]:
                        new_temp[y][x] = avg_temp * 0.9
                    elif self.grid[y][x] == Material.WATER:
                        new_temp[y][x] = avg_temp * 0.7
                    else:
                        new_temp[y][x] = avg_temp * 0.95
                    
                    new_temp[y][x] = max(0, new_temp[y][x] - 0.1)
        
        self.temp_grid = new_temp
    
    def _draw_grid(self):
        self.surface.fill((0, 0, 0, 0))
        
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                material = self.grid[y][x]
                color = self.color_map[material]
                
                if material not in [Material.FIRE, Material.EMPTY, Material.SMOKE] and self.temp_grid[y][x] > 50:
                    heat = min(200, self.temp_grid[y][x])
                    color = (
                        min(255, color[0] + heat * 0.7),
                        max(0, color[1] - heat * 0.3),
                        max(0, color[2] - heat * 0.3),
                        color[3] if len(color) > 3 else 255
                    )
                
                pygame.draw.rect(
                    self.surface,
                    color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )
        
        if self.show_debug:
            font = pygame.font.SysFont('Arial', 16)
            debug_text = [
                f"Material: {self.current_material.name}",
                f"Brush: {self.brush_size}px",
                f"Speed: {self.simulation_speed}x",
                f"State: {'RUNNING' if self.is_running else 'PAUSED'}"
            ]
            
            for i, text in enumerate(debug_text):
                text_surface = font.render(text, True, (255 - self.core.background_color[0], 255  - self.core.background_color[1], 255  - self.core.background_color[2]))
                self.surface.blit(text_surface, (5, 5 + i * 20))