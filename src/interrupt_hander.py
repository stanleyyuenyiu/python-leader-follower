import sys
import signal
import logging
from abc import ABC , abstractmethod

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zookepper')
logger.setLevel('DEBUG')

class InterruptHandler(ABC):

    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_interrupts)

    def handle_interrupts(self, signum, frame, ask=True):
        self.on_interrupt(signum, frame, ask)
        sys.exit(0)

    @abstractmethod
    def on_interrupt(self, signum, frame, ask=True):
        pass
