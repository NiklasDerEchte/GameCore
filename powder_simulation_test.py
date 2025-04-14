from game_core import *

class PowderGame(Engine):
    def awake(self):
        # Powder Simulation erstellen
        self.sim = self.core.instantiate(
            PowderSimulationPrefab,
            width=800,
            height=600
        )
        
    def start(self):
        # Tastatursteuerung
        self.coroutines = [
            Coroutine(
                func=self._handle_keys,
                interval=16  # ~60fps
            )
        ]
    
    def _handle_keys(self):
        # Mausabfrage
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Tastaturabfrage
        keys = pygame.key.get_pressed()

        # Mausposition auf das Simulations-Grid mappen
        if hasattr(self.sim, 'surface') and self.sim.surface is not None:
            surface_offset = self.sim.surface.get_offset()
            surface_pos = (
                mouse_pos[0] - surface_offset[0],
                mouse_pos[1] - surface_offset[1]
            )
            
            grid_x = int(surface_pos[0] // self.sim.cell_size)
            grid_y = int(surface_pos[1] // self.sim.cell_size)

            # Nur innerhalb des gültigen Bereichs arbeiten
            if 0 <= grid_x < self.sim.width and 0 <= grid_y < self.sim.height:
                # Linksklick - Aktuelles Material platzieren
                if mouse_buttons[0]:
                    self.sim._place_material(grid_x, grid_y, self.sim.current_material)
                
                # Rechtsklick - Material entfernen
                elif mouse_buttons[2]:
                    self.sim._place_material(grid_x, grid_y, Material.EMPTY)
        
        # Materialauswahl
        if keys[pygame.K_1]: self.sim.current_material = Material.SAND
        if keys[pygame.K_2]: self.sim.current_material = Material.WATER
        if keys[pygame.K_3]: self.sim.current_material = Material.STONE
        if keys[pygame.K_4]: self.sim.current_material = Material.WOOD
        if keys[pygame.K_5]: self.sim.current_material = Material.FIRE
        if keys[pygame.K_6]: self.sim.current_material = Material.PLANT
        if keys[pygame.K_7]: self.sim.current_material = Material.ICE
        if keys[pygame.K_8]: self.sim.current_material = Material.ACID
        
        # Simulation steuern
        if keys[pygame.K_SPACE]: self.sim.is_running = not self.sim.is_running
        if keys[pygame.K_UP]: self.sim.simulation_speed = min(10, self.sim.simulation_speed + 1)
        if keys[pygame.K_DOWN]: self.sim.simulation_speed = max(1, self.sim.simulation_speed - 1)
        if keys[pygame.K_d]: self.sim.show_debug = not self.sim.show_debug
        if keys[pygame.K_c]: self.sim._clear_grid()
        if keys[pygame.K_r]: self.sim._randomize_grid()

# Hauptprogramm
if __name__ == "__main__":
    core = Core(
        title="Advanced Powder Simulation",
        size=(800, 600),
        fps=60
    )