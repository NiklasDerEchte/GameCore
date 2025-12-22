import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *

# TODO
@scene("network")
class NetworkModule(RPCEngine):
    def start(self):
        print("NetworkModule started...")
        # TODO hier will ich hin, sodass die RPC calls von den dekoratoren ausgeführt werden
        # if isServer:
        #     client_rpc()
        # elif isClient:
        #     server_rpc()
        pass

    @client_rpc
    def client_rpc(self):
        print("Client RPC")
        
    @server_rpc
    def server_rpc(self):
        print("Server RPC")
        return {"status": "success"}