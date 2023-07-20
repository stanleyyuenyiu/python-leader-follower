from abc import ABC , abstractmethod

class IZkClient(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def is_leader(self):
        pass

class ISocketClient:
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send(self, msg):
        pass

    @abstractmethod
    def recv(self):
        pass