from websockets.sync.client import connect
import logging
from interface import ISocketClient

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zookepper')
logger.setLevel('DEBUG')

class SocketClient(ISocketClient):
    def __init__(self, endpoint:str) -> None:
        self.endpoint = endpoint
    
    def start(self, handler):
        with connect(self.endpoint) as websocket:
            self.websocket = websocket
            while True:
                handler(self.send, self.recv)
    
    def send(self, msg):
        self.websocket.send(msg)
        logger.debug("send message")

    def recv(self):
        message = self.websocket.recv()
        logger.debug(f"Received: {message}")