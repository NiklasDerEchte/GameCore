from core import *

class Physics(Engine, Prefab):
    def start(self):
        self._physic_space = Space(self.core.window_size)
        self._physic_space.create_body(50, elasticity=.9, speed=10, mass=30, size=15)
        self._surface = self.core.create_layer_surface()
        #self._physic_space.set_gravity(y=-0.02)
        self._selected_body = None

    def fixed_update(self):
        self._physic_space.update()

    def update(self):
        for event in self.core.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._selected_body = self._physic_space.get_body_at_pos(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._selected_body:
                    self._selected_body.elasticity = .6
                self._selected_body = None

        if self._selected_body:
            self._selected_body.elasticity = 0
            self._selected_body.move_to(pygame.mouse.get_pos())

        for p in self._physic_space.bodies:
            pygame.draw.circle(self._surface, p.color, (int(p.x), int(p.y)), p.size, p.thickness)
