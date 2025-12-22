from concurrent import futures
import json
import threading
import time

import grpc
from ..engine import Engine
from . import game_service_pb2
from . import game_service_pb2_grpc

registered_services = {}

# RPC decorators
def server_rpc(func):
    """Decorator for server RPC methods"""
    func._rpc_type = 'server'
    return func

def client_rpc(func):
    """Decorator for client RPC methods"""
    func._rpc_type = 'client'
    return func

class NetworkEngine:
    
    instance = None
    
    def __init__(self):
        NetworkEngine.instance = self
    
    def _start_engine_grpc_server(self, port=50051):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        game_service_pb2_grpc.add_EngineRPCServicer_to_server(EngineServicer(), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"gRPC is running on port {port}...")
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)

    def startServer(self):
        threading.Thread(target=self._start_engine_grpc_server, daemon=True).start()
        
    def startClient(self):
        channel = grpc.insecure_channel('localhost:50051')  # TODO ip durch variable ersetzen
        return game_service_pb2_grpc.EngineRPCStub(channel) # TODO struktur so überarbeiten, das beim aufrufen der methode der dekorator einschreitet und den rpc vollführt


class EngineServicer(game_service_pb2_grpc.EngineRPCServicer):
    def CallMethod(self, request, context):
        print("CallMethod")
        method_name = request.method_name
        payload = json.loads(request.payload)
        if method_name not in registered_services:
            context.abort(grpc.StatusCode.NOT_FOUND, "Method not found")
        result = registered_services[method_name](**payload)
        response = game_service_pb2.RPCResponse()
        response.payload = json.dumps(result).encode("utf-8")
        return response

class RPCEngine(Engine):
    def __init__(self, core):
        super().__init__(core)
        # TODO struktur überarbeiten
        for rpc_type, methods in self.get_rpc_methods().items():
            for method in methods:
                registered_services[method.__name__] = method

    def get_rpc_methods(self):
        """Returns all methods decorated with @server_rpc or @client_rpc"""
        rpc_methods = {}
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_rpc_type'):
                rpc_type = getattr(attr, '_rpc_type')
                if rpc_type not in rpc_methods:
                    rpc_methods[rpc_type] = []
                rpc_methods[rpc_type].append(attr)
        return rpc_methods

class SyncVar:
    def __init__(self):
        pass

    def sync(self):
        pass
