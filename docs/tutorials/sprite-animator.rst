SpriteAnimator
==============

With the ``SpriteAnimator`` you can animate a surface. For example, to animate your player, the individual images of the animation must be entered into a ``List``. If several images are required per frame, this can easily be solved with a sub-``List``. These methods can also be mixed. The state names are required to control the animation.

.. code-block:: python

    def start(self):
        anim = [
            "state-name-1": [full_body_1_img, full_body_2_img, full_body_3_img],
            "state-name-2": [[body_1_img, hair_1_img], [body_2_img, hair_2_img]],
            "state-name-3": [full_body_1_img, [body_2_img, hair_2_img]]
        ]
        self.simpleSpriteAnimator = SimpleSpriteAnimator(
                                anim_sprites=anim,
                                start_state='state-name-1',
                                anim_state_decision=self.anim_sate_decision,
                                sprite_size=(32,32),
                                fps=.2
                        )

.. code-block:: python

    def anim_sate_decision(self): # Decide which animation should be played
        if(velocity < 1):
            return "state-name-1"
        else:
            if(jumping):
                return "state-name-2"
            else:
                return "state-name-3"

.. code-block:: python

    def update(self):
        surface = self.simpleSpriteAnimator.animate(self.core.delta_time)
        self.core.draw_surface(surface, draw_position)