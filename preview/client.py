import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *
from .network import *

@scene("network")
class ClientNetworkModule(RPCEngine):
    def start(self):
        NetworkEngine.instance.startClient()
        print("ClientNetworkModule started...")
        engine = self.core.get_scene_manager().scene().get_engine_by_class(NetworkModule)
        result = engine.server_rpc()
        print("Server RPC result:", result)

Core(background_color=(255, 255, 255, 0), fps=60)
