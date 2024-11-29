NavAgent
========

The ``NavAgent`` class is used for controlled approximation from one position to another. Ideal for players, enemies and everything that should move.

.. code-block:: python

    self.random_destination_position = (random.randint(0, self.core.window_size[0]), random.randint(0, self.core.window_size[1]))
    self.agent = NavAgent(
            position=random_position,
            speed=.75
        )

.. code-block:: python

    def update(self):
        self.agent.move(destination=self.random_destination_position)
        if self.agent.distance <= 1:
            # destination reached