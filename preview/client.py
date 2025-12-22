import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *

# TODO
@scene("network")
class ClientNetworkModule(RPCEngine):
    def start(self):
        client = NetworkEngine.instance.startClient()
        try:
            request = game_service_pb2.RPCRequest(
                method_name="server_rpc", payload=json.dumps({}).encode("utf-8")
            )
            response = client.CallMethod(request)
            print("RPC Response:", json.loads(response.payload.decode("utf-8")))
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")

# TODO - Client -> Server Klappt aber wie geht von Server -> Client?
Core(background_color=(255, 255, 255, 0), fps=60)
