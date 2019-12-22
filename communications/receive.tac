# from twisted.protocols.amp import AMP
from twisted.application.internet import StreamServerEndpointService
from twisted.application.service import Application
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.internet import reactor
import os
import sys
TWISTED_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(TWISTED_DIR)
from misc import Counter  # noqa


application = Application('test AMP server')

endpoint = TCP4ServerEndpoint(reactor, 8750)
factory = Factory()
factory.protocol = Counter
service = StreamServerEndpointService(endpoint, factory)
service.setServiceParent(application)
