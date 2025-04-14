from .core.core import *
import random
import math
from enum import Enum
from collections import deque

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
    def __init__(self, core):
        super().__init__(core)
        self.width = 0
        self.height = 0
        self.cell_size = 3  # Größe jedes Partikels in Pixeln
        self.grid = None
        self.temp_grid = None  # Für Temperaturberechnungen
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
        self.update_interval = 1  # Update every X frames
        
        # Materialeigenschaften
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
        
        # Flammbarkeit (0 = nicht brennbar, 1 = sehr brennbar)
        self.flammability = {
            Material.WOOD: 0.8,
            Material.PLANT: 0.9,
            Material.ICE: 0.0,
            Material.SAND: 0.0,
            Material.STONE: 0.0,
            Material.WATER: 0.0,
            Material.ACID: 0.3
        }
        
        # Schmelzpunkt (Temperatur bei der das Material schmilzt)
        self.melting_point = {
            Material.ICE: 5,
            Material.WOOD: 200
        }
        
        # Brenndauer (in Frames)
        self.burn_duration = {
            Material.WOOD: 300,
            Material.PLANT: 150,
            Material.ACID: 50
        }

    def awake(self, width=300, height=300):
        self.width = width // self.cell_size
        self.height = height // self.cell_size
        self.grid = [[Material.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.temp_grid = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        self.surface = self.core.create_layer_surface(width=width, height=height)
        
        # Wände hinzufügen
        for x in range(self.width):
            self._set_material(x, 0, Material.STONE)
            self._set_material(x, self.height-1, Material.STONE)
        for y in range(self.height):
            self._set_material(0, y, Material.STONE)
            self._set_material(self.width-1, y, Material.STONE)
    
    def _place_material(self, x, y, material):
        radius = self.brush_size // 2
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                dist = dx*dx + dy*dy
                if dist <= radius*radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if material == Material.FIRE:
                            # Feuer kann nur auf brennbaren Materialien platziert werden
                            if self.grid[ny][nx] in self.flammability and self.flammability[self.grid[ny][nx]] > 0:
                                self._set_material(nx, ny, material)
                                self.temp_grid[ny][nx] = 300  # Starttemperatur für Feuer
                        else:
                            self._set_material(nx, ny, material)
    
    def _set_material(self, x, y, material):
        self.grid[y][x] = material
        # Temperatur zurücksetzen bei bestimmten Materialien
        if material in [Material.STONE, Material.WATER, Material.ICE]:
            self.temp_grid[y][x] = 0
    
    def _clear_grid(self):
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self._set_material(x, y, Material.EMPTY)
    
    def _randomize_grid(self):
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
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
    
    def _update_physics(self):
        # Wir gehen von unten nach oben durch das Grid für realistischere Physik
        for y in range(self.height-2, 0, -1):
            for x in range(1, self.width-1):
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
        # Sand fällt nach unten
        if self._try_move(x, y, 0, 1):
            return
            
        # Sand kann seitlich rutschen
        if random.random() < 0.5:
            if self._try_move(x, y, -1, 1) or self._try_move(x, y, 1, 1):
                return
        else:
            if self._try_move(x, y, 1, 1) or self._try_move(x, y, -1, 1):
                return
    
    def _update_water(self, x, y):
        # Wasser fließt nach unten
        if self._try_move(x, y, 0, 1):
            return
            
        # Wasser fließt seitlich
        directions = [-1, 1]
        random.shuffle(directions)
        
        for dx in directions:
            if self._try_move(x, y, dx, 0):
                return
                
        # Wasser kann auch diagonal fließen
        for dx in directions:
            if self._try_move(x, y, dx, 1):
                return
    
    def _update_fire(self, x, y):
        # Feuer breitet sich aus
        if self.temp_grid[y][x] <= 0:
            self._set_material(x, y, Material.EMPTY)
            return
            
        # Temperatur verringern
        self.temp_grid[y][x] -= 1
        
        # Nachbarmaterialien entzünden
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor_mat = self.grid[ny][nx]
                    
                    # Brennbares Material entzünden
                    if neighbor_mat in self.flammability and random.random() < self.flammability[neighbor_mat]:
                        if neighbor_mat == Material.WOOD and self.temp_grid[ny][nx] < 100:
                            self.temp_grid[ny][nx] += 5  # Holz erwärmen
                        elif self.temp_grid[ny][nx] > 150 and random.random() < 0.1:
                            self._set_material(nx, ny, Material.FIRE)
                            self.temp_grid[ny][nx] = 200
                    
                    # Wasser löscht Feuer
                    if neighbor_mat == Material.WATER and random.random() < 0.3:
                        self._set_material(x, y, Material.EMPTY)
                        self.temp_grid[y][x] = 0
                        if random.random() < 0.5:
                            self._set_material(nx, ny, Material.EMPTY)
                        return
        
        # Feuer kann nach oben steigen (als Flamme)
        if y > 0 and self.grid[y-1][x] == Material.EMPTY and random.random() < 0.2:
            self._set_material(x, y-1, Material.FIRE)
            self.temp_grid[y-1][x] = self.temp_grid[y][x] * 0.9
        
        # Manchmal Rauch erzeugen
        if random.random() < 0.05:
            if y > 0 and self.grid[y-1][x] == Material.EMPTY:
                self._set_material(x, y-1, Material.SMOKE)
    
    def _update_smoke(self, x, y):
        # Rauch steigt auf
        if y > 0 and self._try_move(x, y, 0, -1):
            return
            
        # Rauch kann sich seitlich ausbreiten
        directions = [-1, 1]
        random.shuffle(directions)
        for dx in directions:
            if self._try_move(x, y, dx, -1):
                return
                
        # Rauch verschwindet nach einer Weile
        if random.random() < 0.1:
            self._set_material(x, y, Material.EMPTY)
    
    def _update_ice(self, x, y):
        # Eis schmilzt bei hoher Temperatur
        if self.temp_grid[y][x] > self.melting_point[Material.ICE]:
            self._set_material(x, y, Material.WATER)
    
    def _update_acid(self, x, y):
        # Säure frisst sich durch bestimmte Materialien
        if random.random() < 0.3:
            directions = [(0, 1), (-1, 0), (1, 0), (-1, 1), (1, 1)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor_mat = self.grid[ny][nx]
                    if neighbor_mat in [Material.STONE, Material.WOOD, Material.PLANT]:
                        if random.random() < 0.5:
                            self._set_material(nx, ny, Material.EMPTY)
                        break
        
        # Säure verhält sich ähnlich wie Wasser, aber aggressiver
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
        
        if 0 <= nx < self.width and 0 <= ny < self.height:
            current_mat = self.grid[y][x]
            target_mat = self.grid[ny][nx]
            
            # Leerer Platz oder Material mit geringerer Dichte?
            if (target_mat == Material.EMPTY or 
                (self.density_map[current_mat] > self.density_map[target_mat] and 
                 target_mat not in [Material.STONE, Material.ICE])):
                
                # Materialien tauschen
                self.grid[y][x], self.grid[ny][nx] = self.grid[ny][nx], self.grid[y][x]
                self.temp_grid[y][x], self.temp_grid[ny][nx] = self.temp_grid[ny][nx], self.temp_grid[y][x]
                return True
                
        return False
    
    def _update_temperature(self):
        # Temperaturberechnung (einfache Wärmeausbreitung)
        new_temp = [row[:] for row in self.temp_grid]
        
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.grid[y][x] == Material.EMPTY:
                    continue
                    
                # Wärme von Nachbarn übernehmen
                temp_sum = 0
                count = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                            
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            temp_sum += self.temp_grid[ny][nx]
                            count += 1
                
                if count > 0:
                    avg_temp = temp_sum / count
                    # Material-spezifische Wärmeleitung
                    if self.grid[y][x] in [Material.STONE, Material.WOOD]:
                        new_temp[y][x] = avg_temp * 0.9
                    elif self.grid[y][x] == Material.WATER:
                        new_temp[y][x] = avg_temp * 0.7
                    else:
                        new_temp[y][x] = avg_temp * 0.95
                    
                    # Abkühlung
                    new_temp[y][x] = max(0, new_temp[y][x] - 0.1)
        
        self.temp_grid = new_temp
    
    def _draw_grid(self):
        # Grid auf Surface zeichnen
        self.surface.fill((0, 0, 0, 0))
        
        for y in range(self.height):
            for x in range(self.width):
                material = self.grid[y][x]
                color = self.color_map[material]
                
                # Temperatur-Effekte
                if material not in [Material.FIRE, Material.EMPTY, Material.SMOKE] and self.temp_grid[y][x] > 50:
                    # Material erwärmen (Rot-Ton hinzufügen)
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
        
        # Debug-Info anzeigen
        if self.show_debug:
            font = pygame.font.SysFont('Arial', 16)
            debug_text = [
                f"Material: {self.current_material.name}",
                f"Brush: {self.brush_size}px",
                f"Speed: {self.simulation_speed}x",
                f"State: {'RUNNING' if self.is_running else 'PAUSED'}"
            ]
            
            for i, text in enumerate(debug_text):
                text_surface = font.render(text, True, (255, 255, 255))
                self.surface.blit(text_surface, (5, 5 + i * 20))