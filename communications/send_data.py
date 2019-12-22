from sys import stdout

from twisted.python.log import startLogging, err
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from misc import Count, Counter

if __name__ == '__main__':
    import send_data
    raise SystemExit(send_data.main())


def connect():
    endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 8750)
    factory = Factory()
    factory.protocol = Counter
    return endpoint.connect(factory)


def main():
    startLogging(stdout)

    d = connect()
    d.addErrback(err, 'connection failed')
    d.addCallback(lambda p: p.callRemote(Count, n=1))
    d.addErrback(err, 'call failed')

    reactor.run()
