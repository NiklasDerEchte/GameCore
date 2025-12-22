import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *
from .network import *

@scene("network")
class ServerNetworkModule(RPCEngine):
    def start(self):
        NetworkEngine.instance.startServer()
        print("ServerNetworkModule started...")
        self._position = SyncVar()
        #engine = (self.core.get_scene_manager().scene().get_engine_by_class(NetworkModule))
        #result = engine.client_rpc()
        #print("Client RPC result:", result)

Core(background_color=(255, 255, 255, 0), fps=60)
