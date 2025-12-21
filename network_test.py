from game_core import *

@scene("network")
class NetworkModule(NetworkEngine):
    def start(self):
        print("NetworkModule started")

        self._position = SyncVar()


Core(
    background_color=(255, 255, 255, 0), 
    fps=60
)
