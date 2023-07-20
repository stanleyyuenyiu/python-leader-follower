from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging
from interface import IZkClient

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zookepper')
logger.setLevel('DEBUG')

class ZkClient(IZkClient):
    def __init__(self, hosts) -> None:
        self.zk = KazooClient(hosts=hosts)
        self.node_path = []

    def _state_listener(self, state):
        if state == KazooState.LOST:
            logger.debug('Connection lost')
        elif state == KazooState.SUSPENDED:
            logger.debug('Connection suspended')
        else:
            logger.debug('Connection established')

    def start(self, node_path = ['/node', 'leader']):
        self.node_path = node_path

        self.zk.start()
        self.curr_node = self._create_node(self.node_path)
        
        self.zk.add_listener(self._state_listener)

    def _watcher(self, *args, **kwargs):
        logger.debug("Data changed: %s" % (args[0]))

    def _create_node(self, path = []):
        if not path:
            raise Exception('path is empty')
        self.zk.ensure_path(path[0])
        return self.zk.create('/'.join(path), value=b'data', ephemeral=True, sequence=True)

    def is_leader(self):
        nodes = self.zk.get_children(self.node_path[0])
        # Sort the nodes by their sequence number
        nodes.sort()
        # If this instance is the first node in the list, it becomes the leader
        if self.curr_node == self.node_path[0] + '/' + nodes[0]:
            logger.debug('Instance is the leader')
            return True
        else:
            logger.debug('Instance is a follower')
            return False
        
    def close(self):
        self.zk.stop()
        self.zk.close()