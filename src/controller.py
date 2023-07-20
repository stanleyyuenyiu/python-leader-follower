import time
import logging
from interface import IZkClient, ISocketClient
from interrupt_hander import InterruptHandler

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zookepper')
logger.setLevel('DEBUG')

class ZKController(InterruptHandler):
    def __init__(self, zk:IZkClient, socket_listener:ISocketClient) -> None:
        super().__init__() 
        self.zk = zk
        self.socket_listener = socket_listener
        
    def start(self):
        self.zk.start()
        self.socket_listener.start(self.socket_handler)

    def socket_handler(self, send, rcev):
        if self.zk.is_leader():
            send('{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}')
            rcev()
        time.sleep(2)

    def on_interrupt(self, signum, frame, ask=True):
        self.zk.close()

