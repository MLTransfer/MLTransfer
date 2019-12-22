from twisted.protocols import amp


class Count(amp.Command):
    arguments = [(b'n', amp.Integer())]
    response = [(b'ok', amp.Boolean())]


class Counter(amp.AMP):
    @Count.responder
    def count(self, n):
        print(f'received:{n}')
        n += 1

        if n < 10:
            print(f'sending:{n}')
            self.callRemote(Count, n=n)

        return {'ok': True}
