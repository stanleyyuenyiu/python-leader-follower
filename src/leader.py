from controller import ZKController
from socket_client import SocketClient
from zk_client import ZkClient
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    zk = ZkClient(os.getenv('ZK_HOST', 'localhost:2181'))
    socket_listener = SocketClient(os.getenv('SOCKET_URI'))
    controller = ZKController(zk, socket_listener)
    controller.start()