import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from game_core import *
from .network import *

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

# TODO - Wenn Server und Client gestartet werden:
# RPC Error: <_InactiveRpcError of RPC that terminated with:
#         status = StatusCode.UNIMPLEMENTED
#         details = "Method not found!"
#         debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"Method not found!", grpc_status:12}"

Core(background_color=(255, 255, 255, 0), fps=60)
