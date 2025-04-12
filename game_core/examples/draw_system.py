from game_core.src import *

class DrawSystem(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_MainDrawSurface",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )

        self.blue_box_sprite = SimpleSprite(color=(54, 117, 221))
        self.blue_box_sprite.update_rect(
            self.blue_box_sprite.get_rect().move((50, 50))
        )

    def update(self):
        self.surface.blit(self.blue_box_sprite.get_image(), self.blue_box_sprite.get_rect())



class DrawSystemImage(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_MainDrawSurfaceImage",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )
        self.image_sprite = SimpleImageSprite(os.path.join(LIB_DIR, "examples/assets/pixel-adventure/Main Characters/Ninja Frog/Idle/tile000.png"))
        coords = get_center(
            (size[0] / 2, size[1] / 2),
            self.image_sprite.get_rect().width,
            self.image_sprite.get_rect().height
        )
        self.image_sprite.update_rect(
            self.image_sprite.get_rect().move(coords)
        )

    def update(self):
        self.surface.blit(self.image_sprite.get_image(), self.image_sprite.get_rect())

class DrawSystemAnimationImage(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_DrawSystemAnimationImage",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )
        anim = {
            "idle": [SimpleImageSprite(os.path.join(LIB_DIR, "examples/assets/pixel-adventure/Main Characters/Ninja Frog/Idle/tile{:03}.png".format(index))).get_image() for index in range(11)]
        }
        self.simple_sprite_animator = SimpleSpriteAnimator(
            anim_sprites=anim,
            start_state="idle",
            anim_state_decision=self.anim_sate_decision,
            sprite_size=(32, 32),
            fps=1
        )
        coords = get_center(
            (size[0] / 2, size[1] / 2),
            self.simple_sprite_animator.get_rect().width,
            self.simple_sprite_animator.get_rect().height
        )
        self.simple_sprite_animator.update_rect(
            self.simple_sprite_animator.get_rect().move(coords)
        )

    def update(self):
        self.surface.blit(
            self.simple_sprite_animator.animate(self.core.delta_time),
            self.simple_sprite_animator.get_rect()
        )

    def anim_sate_decision(self):
        return "idle"

class DrawSystemAnimationImageSliced(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_DrawSystemAnimationImageSliced",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )
        anim = {
            "idle": SimpleImageSprite(os.path.join(LIB_DIR, "examples/assets/pixel-adventure/Main Characters/Ninja Frog/Idle (32x32).png"), slicer=AmountSlicer(cols=11)).get_image()
        }
        self.simple_sprite_animator = SimpleSpriteAnimator(
            anim_sprites=anim,
            start_state="idle",
            anim_state_decision=self.anim_sate_decision,
            sprite_size=(32, 32),
            fps=1
        )
        coords = get_center(
            (size[0] / 2, size[1] / 2),
            self.simple_sprite_animator.get_rect().width,
            self.simple_sprite_animator.get_rect().height
        )
        self.simple_sprite_animator.update_rect(
            self.simple_sprite_animator.get_rect().move(coords)
        )

    def update(self):
        self.surface.blit(
            self.simple_sprite_animator.animate(self.core.delta_time),
            self.simple_sprite_animator.get_rect()
        )

    def anim_sate_decision(self):
        return "idle"

class DrawSystemAnimationImageSlicedWithPaddings(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_DrawSystemAnimationImageSlicedWithPaddings",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )
        anim = {
            "idle": SimpleImageSprite(os.path.join(LIB_DIR, "examples/assets/debug/image-with-padding.png"), slicer=AmountSlicer(
                cols=3,
                rows=3,
                top_padding=2,
                bottom_padding=2,
                left_padding=2,
                right_padding=2,
                x_gap=2,
                y_gap=2
            )).get_image()
        }
        self.simple_sprite_animator = SimpleSpriteAnimator(
            anim_sprites=anim,
            start_state="idle",
            anim_state_decision=self.anim_sate_decision,
            sprite_size=(32, 32),
            fps=.1
        )
        coords = get_center(
            (size[0] / 2, size[1] / 2),
            self.simple_sprite_animator.get_rect().width,
            self.simple_sprite_animator.get_rect().height
        )
        self.simple_sprite_animator.update_rect(
            self.simple_sprite_animator.get_rect().move(coords)
        )

    def update(self):
        self.surface.blit(
            self.simple_sprite_animator.animate(self.core.delta_time),
            self.simple_sprite_animator.get_rect()
        )

    def anim_sate_decision(self):
        return "idle"

class DrawSystemDirectoryAnimationImageSliced(Engine, Prefab):
    def start(self):
        size = self.core.window_size
        self.surface = self.core.create_layer_surface(
            name="_DrawSystemDirectoryAnimationImageSliced",
            width=size[0],
            height=size[1],
            x=0,
            y=0,
            render_layer=0,
            fill_after_draw=True
        )
        sprite_dir_anim = SpriteDirectoryAnimation(os.path.join(LIB_DIR, "examples/assets/pixel-adventure/Main Characters/Ninja Frog"), slicer=SizeSlicer(width=32, height=32))
        anim = sprite_dir_anim.parse()
        anim["idle"] = anim["Idle"]
        anim["run"] = anim["Run (32x32)"]
        self.simple_sprite_animator = SimpleSpriteAnimator(
            anim_sprites=anim,
            start_state="idle",
            anim_state_decision=self.anim_sate_decision,
            sprite_size=(32, 32),
            fps=2
        )
        coords = get_center(
            (size[0] / 2, size[1] / 2),
            self.simple_sprite_animator.get_rect().width,
            self.simple_sprite_animator.get_rect().height
        )
        self.simple_sprite_animator.update_rect(
            self.simple_sprite_animator.get_rect().move(coords)
        )
        self._is_idle = True
        self._timer = 0

    def update(self):
        self.surface.blit(
            self.simple_sprite_animator.animate(self.core.delta_time),
            self.simple_sprite_animator.get_rect()
        )
        if self._is_idle:
            self._timer += self.core.delta_time
            if self._timer >= 5000:
                self._is_idle = False
        else:
            self._timer -= self.core.delta_time
            if self._timer <= 0:
                self._is_idle = True
    def anim_sate_decision(self):
        if self._is_idle:
            return "idle"
        return "run"