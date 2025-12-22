import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *
from .network import *

# TODO
@scene("network")
class ServerNetworkModule(RPCEngine):
    def start(self):
        NetworkEngine.instance.startServer()
        print("ServerNetworkModule started...")
        self._position = SyncVar()


Core(background_color=(255, 255, 255, 0), fps=60)
