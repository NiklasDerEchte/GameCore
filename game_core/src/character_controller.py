from .core import *
import math

class Direction:
    """Provides direction constants and utility methods for direction checking."""
    LEFT = -1
    RIGHT = 1
    
    def isDirection(self, input, direction, delta=0.01) -> bool:
        """
        Checks if an input value matches a specific direction within a tolerance.
        
        :param input: The input value to check.
        :type input: float
        :param direction: The target direction to compare against (either Direction.LEFT or Direction.RIGHT).
        :type direction: int
        :param delta: The maximum allowed difference between input and direction. Defaults to 0.01.
        :type delta: float, optional
        :return: True if input is within delta of direction, False otherwise.
        :rtype: bool
        """
        return math.isclose(input, direction, abs_tol=delta)

class PhysicsSettings:
    """Stores physics-related settings for platformer characters."""
    
    def __init__(self):
        """
        Initializes default physics settings.
        
        Attributes include:
        - gravity_enabled: Whether gravity affects the character (default: True)
        - gravity_force: The strength of gravity (default: 9.8)
        - max_fall_speed: Maximum falling speed (default: 15.0)
        - ground_friction: Friction when on ground (default: 0.8)
        - air_resistance: Air resistance when moving (default: 0.1)
        - mass: Character mass (default: 1.0)
        - bounciness: Bounce factor when hitting surfaces (default: 0.2)
        """
        self.gravity_enabled = True
        self.gravity_force = 9.8
        self.max_fall_speed = 15.0
        self.ground_friction = 0.8
        self.air_resistance = 0.1
        self.mass = 1.0
        self.bounciness = 0.2

class CharacterSettings:
    """Stores character-specific movement settings."""
    
    def __init__(self):
        """
        Initializes default character movement settings.
        
        Attributes include:
        - move_speed: Base movement speed (default: 5)
        - jump_force: Vertical force applied when jumping (default: 200.0)
        - friction: Movement friction coefficient (default: 0.1)
        """
        self.move_speed = 5
        self.jump_force = 200.0
        self.friction = 0.1

class PlatformerCharacterControllerPrefab(Engine):
    """A platformer character controller with physics and movement capabilities."""
    
    def awake(self,
              x=0,
              y=0,
              width=32,
              height=32,
              physics: PhysicsSettings=None,
              character: CharacterSettings=None):
        """
        Initializes the character controller with specified parameters.
        
        :param x: Initial x-position of the character. Defaults to 0.
        :type x: int, optional
        :param y: Initial y-position of the character. Defaults to 0.
        :type y: int, optional
        :param width: Width of the character's collision rect. Defaults to 32.
        :type width: int, optional
        :param height: Height of the character's collision rect. Defaults to 32.
        :type height: int, optional
        :param physics: Physics settings for the character. Uses defaults if None.
        :type physics: PhysicsSettings, optional
        :param character: Character movement settings. Uses defaults if None.
        :type character: CharacterSettings, optional
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.physics = physics if physics is not None else PhysicsSettings()
        self.character = character if character is not None else CharacterSettings()
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.horizontal_direction = 0
        
        self.is_grounded = True
        self.is_jumping = False
        self.facing_right = True
 
        self.colliders = []
        
    def fixed_update(self):
        """
        Updates physics and movement calculations in fixed time intervals.
        
        Handles:
        - Movement acceleration
        - Gravity application
        - Collision detection
        - Direction facing updates
        """
        dt = self.core.delta_time/1000
        self.acceleration = pygame.math.Vector2(self.character.move_speed * self.horizontal_direction, 0)
        self._apply_gravity()
        self._apply_movement(dt)
        self.rect.midbottom = self.position
        
        if self.colliders is not None and len(self.colliders) > 0:
            self._handle_collisions(self.colliders)
        
        if Direction().isDirection(self.horizontal_direction, Direction.RIGHT):
            self.facing_right = True
        elif Direction().isDirection(self.horizontal_direction, Direction.LEFT):
            self.facing_right = False
        self.horizontal_direction = 0
    
    def _apply_gravity(self):
        """
        Applies gravity force to the character's vertical velocity.
        
        Only affects the character when not grounded and gravity is enabled.
        """
        if self.physics.gravity_enabled and not self.is_grounded: 
            self.velocity.y += self.physics.gravity_force
    
    def _apply_movement(self, dt):
        """
        Applies movement physics based on current acceleration and velocity.
        
        :param dt: Delta time since last frame, used for time-correct movement.
        :type dt: float
        """
        self.acceleration.x += self.velocity.x * self.character.friction
        self.velocity += self.acceleration * (dt ** 2)
        self.position += self.velocity * dt + 0.5 * self.acceleration
        self.velocity = pygame.math.Vector2(round(self.velocity.x, 2), round(self.velocity.y, 2))
    
    def _handle_collisions(self, colliders):
        """
        Handles collision detection and response with provided colliders.
        
        :param colliders: List of pygame.Rect objects to check for collisions.
        :type colliders: list[pygame.Rect]
        """
        self.is_grounded = False
        
        for collider in colliders:
            if self.rect.colliderect(collider):
                overlap_x = min(self.rect.right - collider.left, collider.right - self.rect.left)
                overlap_y = min(self.rect.bottom - collider.top, collider.bottom - self.rect.top)
                
                if abs(overlap_x) < abs(overlap_y):
                    if self.rect.centerx < collider.centerx:
                        self.rect.right = collider.left
                    else:
                        self.rect.left = collider.right
                    self.velocity.x = 0
                else:
                    if self.rect.centery < collider.centery:
                        self.rect.bottom = collider.top
                        self.is_grounded = True
                        self.is_jumping = False
                    else:
                        self.rect.top = collider.bottom
                        self.is_jumping = False
                    self.velocity.y = 0
    
    def move_right(self):
        """
        Sets the character's horizontal movement direction to right.
        """
        self.horizontal_direction = Direction.RIGHT
        
    def move_left(self):
        """
        Sets the character's horizontal movement direction to left.
        """
        self.horizontal_direction = Direction.LEFT
        
    def jump(self):
        """
        Makes the character jump if currently grounded.
        
        Applies jump force vertically and updates grounded/jumping states.
        """
        if self.is_grounded and not self.is_jumping:
            self.velocity.y = -self.character.jump_force
            self.is_jumping = True
            self.is_grounded = False
            
    def force(self, force: pygame.math.Vector2):
        """
        Applies an immediate force to the character's velocity.
        
        :param force: The force vector to apply.
        :type force: pygame.math.Vector2
        """
        self.velocity += force
    
    def get_velocity(self) -> pygame.math.Vector2:
        """
        Gets the character's current velocity.
        
        :return: The current velocity vector.
        :rtype: pygame.math.Vector2
        """
        return self.velocity
    
    def get_position(self) -> pygame.math.Vector2:
        """
        Gets the character's current position.
        
        :return: The current position vector.
        :rtype: pygame.math.Vector2
        """
        return self.position
    
    def get_rect(self):
        """
        Gets the character's collision rectangle.
        
        :return: The character's pygame.Rect.
        :rtype: pygame.Rect
        """
        return self.rect
    
    def set_position(self, x: int, y: int):
        """
        Sets the character's position and resets velocity.
        
        :param x: New x-position.
        :type x: int
        :param y: New y-position.
        :type y: int
        """
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """
        Draws the character and direction indicator to the specified surface.
        
        :param surface: The surface to draw onto.
        :type surface: pygame.Surface
        :param camera_offset: Offset to apply for camera positioning. Defaults to (0, 0).
        :type camera_offset: tuple[int, int], optional
        """
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (255, 0, 0), offset_rect)
        
        direction = 1 if self.facing_right else -1
        start_pos = (offset_rect.centerx, offset_rect.centery)
        end_pos = (offset_rect.centerx + 20 * direction, offset_rect.centery)
        pygame.draw.line(surface, (0, 0, 255), start_pos, end_pos, 2)