Basics
======

Game engines are structured to provide a framework for creating and managing the various components of a game, such as rendering, physics, input, and scripting. The core idea is to streamline development by offering reusable systems and tools.

Start and Update Methods
^^^^^^^^^^^^^^^^^^^^^^^^

* ``Start Method``: Used for initialization logic. It runs once when an object is first created or activated in the game.
* ``Update Method``: Used for per-frame logic. It runs repeatedly, usually once per frame, and handles dynamic behaviors like movement or input processing.

Prefabs
^^^^^^^

Prefabs are preconfigured templates for game objects. They allow developers to create reusable objects with predefined properties, behaviors, and hierarchies, making it easier to replicate consistent objects throughout the game.

Sample Project Structure
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    project-root/
    │
    ├── assets/               # All resources like images, sounds, fonts, etc.
    │   ├── images/           # Graphics like sprites, backgrounds
    │   ├── sounds/           # Audio files like music and sound effects
    │   ├── fonts/            # Fonts
    │   └── animations/       # Animations for player, enemy, objects, etc.
    │
    ├── docs/                 # Project documentation
    |
    ├── src/                  # Source code of the project
    │   ├── __init__.py       # Makes src a Python package
    │   ├── game.py           # Main game logic
    │   ├── settings.py       # Game configurations and settings
    │   ├── player.py         # Player character and logic
    │   ├── enemy.py          # Enemy logic
    │   ├── level.py          # Level data and logic
    │   ├── ui.py             # User interface components (menus, HUD, etc.)
    │   └── utils.py          # Helper functions like collision detection, random numbers
    │
    ├── tests/                # Tests for the project (if applicable)
    │   ├── __init__.py
    │   ├── test_game.py      # Tests for the main game logic
    │   ├── test_player.py    # Tests for the player character
    │   └── test_enemy.py     # Tests for enemies
    │
    ├── requirements.txt      # Project dependencies
    ├── README.md             # Project description and instructions
    ├── LICENCE.txt           # Project license
    ├── main.py               # Entry point
    └── .gitignore            # Git ignore rules for files/folders that shouldn't be versioned