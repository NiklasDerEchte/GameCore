
from game_core.src import *

class PlatformCharacterPrefab(Engine):
    def start(self):
        self.player: PlatformerCharacterControllerPrefab = self.core.instantiate(
            PlatformerCharacterControllerPrefab,
            x=100,
            y=100
        )
        self.surface = self.core.create_layer_surface(
            name="_MainDrawSurface",
            width=self.core.window_size[0],
            height=self.core.window_size[1],
            fill_after_draw=True
        )
        character_anim = SpriteDirectoryAnimation(os.path.join(LIB_DIR, "examples/assets/pixel-adventure/Main Characters/Ninja Frog"), slicer=SizeSlicer(width=32, height=32)).parse()
        anim = {}
        for key, value in character_anim.items():
            base_key = key.split()[0].lower()
            anim[base_key] = value
            anim[f"{base_key}_left"] = [pygame.transform.flip(sprite, True, False) for sprite in value]
        
        self.character_sprite_animator = SimpleSpriteAnimator(
            anim_sprites=anim,
            start_state="idle",
            anim_state_decision=self.anim_sate_decision,
            sprite_size=(32, 32),
            fps=1
        )
        self.ground = pygame.Rect(0, self.core.window_size[1]-50, self.core.window_size[0], 10)
        self.player.colliders = [self.ground]
        
    def anim_sate_decision(self):
        prefix = "" if self.player.facing_right else "_left"
        vel = self.player.get_velocity()
        abs_direction = abs(self.player.horizontal_direction)
        if self.player.is_jumping:
            if vel.y > 0.1:
                return f"fall{prefix}"
            return f"jump{prefix}"   
        if abs_direction > 0.1:
            return f"run{prefix}"
        return f"idle{prefix}"
    
    def update(self):
        keys = self.core.pressed_keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_SPACE]:
            self.player.jump()
        
        # Draw character
        self.surface.blit(
            self.character_sprite_animator.animate(self.core.delta_time),
            self.player.get_rect()
        )
        pygame.draw.rect(self.surface, (255, 255, 0), self.ground)