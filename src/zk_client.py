from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging
from interface import IZkClient
from datetime import datetime
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('zookepper')
logger.setLevel('DEBUG')

class ZkClient(IZkClient):
    def __init__(self, hosts) -> None:
        self.zk = KazooClient(hosts=hosts)
        self.server_id = None
        self._is_leader = False
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
        self._register(self.node_path)
        self._watch_application_nodes()
        self._watch_state()

    def _watch_state(self):
        self.zk.add_listener(self._state_listener)

    def _watch_application_nodes(self):
        self.zk.ChildrenWatch(path='/node', func=self._election)
        
    def _election(self, children):
        children.sort()
        server_id = self.server_id.split('/')[-1]
        if children[0] == server_id:
            self._is_leader = True
            logger.debug('Instance is the leader')
        else:
            self._is_leader = False
            logger.debug('Instance is the follower')

    def _register(self, path = []):
        if not path:
            raise Exception('path is empty')
        self.zk.ensure_path(path[0])
        self.server_id = self.zk.create('/'.join(path), value=b'data', ephemeral=True, sequence=True)

    def is_leader(self):
        return self._is_leader
        
    def close(self):
        self.zk.stop()
        self.zk.close()