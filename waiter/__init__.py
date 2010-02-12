import httplib2
import urllib
import simplejson

class Chef(object):
    def __init__(self, method):
        self.method = method
        self.errors = []
        self.cooked_data = {}

    def cook_data(self, stack, params):
        uri = ''.join(stack)
        body = None
        urlencoded_params = urllib.urlencode(params)
        if self.method != 'POST':
            uri += '?%s' % urlencoded_params
        else:
            body = urlencoded_params
        return {
            'uri':uri,
            'body':body,
            'method':self.method,
        } 

    def cooks(self, stack, params):
        self.errors = []
        self.cooked_data = self.cook_data(stack, params)
        return not self.errors

class Consumer(object):
    def __init__(self):
        pass
    def handle(self, response, data):
        return data

class JSONConsumer(object):
    def __init__(self):
        pass

    def handle(self, response, data):
        return simplejson.loads(data)    

class Waiter(object):
    class Error(Exception):
        pass

    def __init__(self, http=None, method='GET', chef=None, consumer=None):
        self._chef = chef if chef else Chef(method)
        self._consumer = consumer if consumer else JSONConsumer() 

        self._http = http if http else httplib2.Http()
        self._stack = []
        self._payload = {}

    def accept_str(self, rhs):
        self._stack = self._stack + ['/', rhs] if self._stack else [rhs]
        return self

    def accept_dict(self, rhs):
        self._payload.update(rhs)
        return self()

    def __div__(self, rhs):
        if hasattr(self, 'accept_%s' % rhs.__class__.__name__.lower()):
            return getattr(self, 'accept_%s' % rhs.__class__.__name__.lower())(rhs)
        raise TypeError 

    def __call__(self, *args, **kwargs):
        self._payload.update(kwargs)
        if self._chef.cooks(self._stack, self._payload):
            self._stack, self._payload = [], {}
            httplib_kwargs = self._chef.cooked_data
            response, data = self._http.request(**httplib_kwargs)
            return self._consumer.handle(response, data)
        else:
            raise Waiter.Error("Invalid waiter stack -> your chef found errors in your order: %s" % self._chef.errors)
