from typing import TYPE_CHECKING
from concurrent import futures
import json
import threading
import time

import grpc
from ..engine import Engine
from . import game_service_pb2
from . import game_service_pb2_grpc

if TYPE_CHECKING:
    from core import Core

registered_services = {}

# RPC decorators
def server_rpc(func):
    """Decorator for server RPC methods - wraps to send RPC to server"""
    func._rpc_type = 'server'
    return func

def client_rpc(func):
    """Decorator for client RPC methods - wraps to send RPC to client"""
    func._rpc_type = 'client'
    return func

class NetworkEngine:

    instance = None

    def __init__(self, core: "Core"):
        NetworkEngine.instance = self
        self.server_stub = None
        self.client_stub = None
        self.core = core

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

    def startServer(self, client_port=50052):
        threading.Thread(target=self._start_engine_grpc_server, args=(50051,), daemon=True).start()
        self.client_stub = game_service_pb2_grpc.EngineRPCStub(grpc.insecure_channel(f'localhost:{client_port}'))
        for engine in self.core.get_scene_manager().scene().get_engines():
            engine.update_wrappers()

    def startClient(self, server_port=50051):
        threading.Thread(target=self._start_engine_grpc_server, args=(50052,), daemon=True).start()
        self.server_stub = game_service_pb2_grpc.EngineRPCStub(grpc.insecure_channel(f'localhost:{server_port}'))
        for engine in self.core.get_scene_manager().scene().get_engines():
            engine.update_wrappers()

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
        for rpc_type, methods in self.get_rpc_methods().items():
            for method in methods:
                registered_services[method.__name__] = method

    def update_wrappers(self):
        for rpc_type, methods in self.get_rpc_methods().items():
            for method in methods:
                if rpc_type == 'server' and hasattr(NetworkEngine.instance, 'server_stub') and NetworkEngine.instance.server_stub:
                    setattr(self, method.__name__, self._wrap_rpc(method, NetworkEngine.instance.server_stub))
                elif rpc_type == 'client' and hasattr(NetworkEngine.instance, 'client_stub') and NetworkEngine.instance.client_stub:
                    setattr(self, method.__name__, self._wrap_rpc(method, NetworkEngine.instance.client_stub))

    def _wrap_rpc(self, original_method, stub):
        def wrapped(*args, **kwargs):
            request = game_service_pb2.RPCRequest(
                method_name=original_method.__name__,
                payload=json.dumps(kwargs).encode("utf-8")
            )
            response = stub.CallMethod(request)
            return json.loads(response.payload.decode("utf-8"))
        return wrapped

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
