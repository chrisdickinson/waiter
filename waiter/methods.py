
class Method(object):
    def __init__(self, method):
        self.method = method

    def accept_waiter(self, waiter):
        waiter._chef.method = self.method
        return waiter

POST = Method('POST')
PUT = Method('PUT')
DELETE = Method('DELETE')
GET = Method('GET')

