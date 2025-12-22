import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *

@scene("network")
class NetworkModule(RPCEngine):
    def start(self):
        print("NetworkModule started")
        # if isServer:
        #     client_rpc()
        # elif isClient:
        #     server_rpc()
        pass
    
    # TODO bei einem Scenen wechsel oder onDestroy muss auch automatisch die rpc verbindung wieder geschlossen werden

    @client_rpc
    def client_rpc(self):
        print("Client RPC")
        return {"status": "client_success"}

    @server_rpc
    def server_rpc(self):
        print("Server RPC")
        return {"status": "server_success"}
