from game_core.core import *
class ScreenBlink(Engine, Prefab):
    def start(self):
        self.coroutines = [
            Coroutine(
                func=self.change,
                interval=15*1000,
                call_delay=30,
            )
        ]

    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def change(self):
        self.core.background_color = self.random_color()