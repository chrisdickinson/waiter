from waiter import Waiter, Chef, Consumer, JSONConsumer, Menu
import simplejson
import mox
import unittest
import random
import httplib2
import urllib

class TestOfChef(unittest.TestCase):
    def test_init_sets_correct_fields(self):
        random_value = random.randint(1,100)
        c = Chef(random_value)
        self.assertEqual(c.errors, [])
        self.assertEqual(c.cooked_data, {})
        self.assertEqual(c.method, random_value)

    def test_cook_data_urlencodes_params_and_appends_on_non_post(self):
        random_value = random.randint(1,100)
        c = Chef(random_value)
        random_stack = [str(random.randint(1,100)) for i in range(0, random.randint(1,10))]
        random_params = dict([('random-key-%d'%random.randint(1,100), i) for i in range(0, random.randint(1,10))])
        results = c.cook_data(random_stack, random_params)

        self.assertEqual(results['uri'].split('?')[0], ''.join(random_stack))
        self.assertEqual(results['uri'].split('?')[1], urllib.urlencode(random_params))
        self.assertEqual(results['body'], None)
        self.assertEqual(results['method'], random_value)

    def test_cook_data_puts_urlencoded_params_in_body_on_post(self):
        c = Chef('POST')
        random_stack = [str(random.randint(1,100)) for i in range(0, random.randint(1,10))]
        random_params = dict([('random-key-%d'%random.randint(1,100), i) for i in range(0, random.randint(1,10))])
        results = c.cook_data(random_stack, random_params)
        self.assertEqual(results['uri'], ''.join(random_stack))
        self.assertEqual(results['body'], urllib.urlencode(random_params))

    def test_cooks_clears_error_stack(self):
        c = Chef('POST')
        c.errors = [i for i in range(0, random.randint(0,100))]
        c.cooks([], {})
        self.assertEqual(c.errors, [])

    def test_cooks_sets_cooked_data(self):
        c = Chef('POST')
        c.cooks([], {})
        self.assertTrue('uri' in c.cooked_data.keys())
        self.assertTrue('method' in c.cooked_data.keys())
        self.assertTrue('body' in c.cooked_data.keys())

    def test_cooks_returns_false_if_errors(self):
        random_error = [random.randint(1,100)]
        class SousChef(Chef):
            def cook_data(self, *args, **kwargs):
                self.errors = random_error 
                return super(SousChef, self).cook_data(*args, **kwargs)

        c = SousChef('GET')
        self.assertFalse(c.cooks([], {}))
        self.assertEqual(c.errors, random_error)

class TestOfConsumer(unittest.TestCase):
    def test_handle_does_a_passthrough(self):
        c = Consumer()
        random_value = random.randint(1,100)
        self.assertEqual(c.handle(random.randint(1,100), random_value), random_value)

class TestOfJSONConsumer(unittest.TestCase):
    def test_handle_passes_through_simplejson(self):
        c = JSONConsumer()
        random_value = { 'rand-%d' % random.randint(1, 100): random.randint(1,100) }
        random_value_in_json = simplejson.dumps(random_value)
        self.assertEqual(c.handle(random.randint(1,100), random_value_in_json), random_value)

class TestOfMenu(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_instantiate_stores_value(self):
        random_value = random.randint(1,100)
        oh = Menu(random_value)
        self.assertEqual(random_value, oh.value) 

    def test_instantiate_updates_dict(self):
        random_value = random.randint(1,100)
        update_dict_key = [str, dict][random.randint(0,1)]
        update_dict = { update_dict_key: random_value }

        oh = Menu(random_value, update_dict)
        self.assertEqual(random_value, oh.value) 
        self.assertEqual(oh.dispatch[update_dict_key], random_value)

    def test_accept_waiter_delegates_to_dispatch(self):
        random_value = random.randint(1,100)
        update_dict_key = [str, dict][random.randint(0,1)]
        fake_function = lambda x: random_value
        update_dict = { update_dict_key: fake_function }
        oh = Menu(update_dict_key(), update_dict)
        result = oh.accept_waiter(Waiter())
        self.assertEqual(result, random_value)

    def test_accept_str_sets_stack_if_no_stack(self):
        waiter = Waiter()
        random_string = 'rand-%d'%random.randint(1,100)
        oh = Menu(random_string)
        results = oh.accept_str(waiter)
        self.assertTrue(results is waiter)
        self.assertEqual(waiter._stack, [random_string])

    def test_accept_str_prepends_divider_on_existing_stack(self):
        waiter = Waiter()
        random_string = 'rand-%d'%random.randint(1,100)
        waiter._stack = [random_string]
        oh = Menu(random_string)
        results = oh.accept_str(waiter)
        self.assertTrue(results is waiter)
        self.assertEqual(waiter._stack, [random_string, '/', random_string])

    def test_accept_dict_calls_waiter(self):
        waiter = self.mox.CreateMock(Waiter)
        random_value = { str('rand-%d'%random.randint(1,100)): random.randint(1,100) }
        random_return = random.randint(1,100)
        waiter(**random_value).AndReturn(random_return)
        self.mox.ReplayAll()
        oh = Menu(random_value)
        results = oh.accept_waiter(waiter)
        self.assertEqual(results, random_return)
        self.mox.VerifyAll()

    def test_accept_waiter_raises_typeerror_on_no_dispatch(self):
        random_type = type('Random_%d'%random.randint(1,100), (), {})
        oh = Menu(random_type())
        random_anything = random.randint(1,100) 
        self.assertRaises(TypeError, oh.accept_waiter, random_anything)

class TestOfWaiter(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_assigns_objects_if_any(self):
        random_http = random.randint(1,100)
        random_method = random.randint(1,100)
        random_chef = random.randint(1,100)
        random_consumer = random.randint(1,100)
        waiter = Waiter(random_http, random_method, random_chef, random_consumer)
        self.assertEqual(waiter._http, random_http)
        self.assertEqual(waiter._chef, random_chef)
        self.assertEqual(waiter._consumer, random_consumer)
        self.assertFalse(hasattr(waiter, '_method'))
        self.assertEqual(waiter._stack, [])
        self.assertEqual(waiter._payload, {})

    def test_div_delegates_to_objects_with_accept_waiter(self):
        random_value = random.randint(1,100)
        random_class = type('Rand%d'%random.randint(1,100), (), {'accept_waiter':lambda x, y:random_value})
        waiter = Waiter()
        results = waiter/random_class()
        self.assertEqual(results, random_value)

    def test_init_automatically_assigns_objects(self):
        random_method = ('GET', 'POST', 'PUT', 'DELETE')[random.randint(0, 3)]
        waiter = Waiter(method=random_method)
        self.assertTrue(isinstance(waiter._http, httplib2.Http))
        self.assertTrue(isinstance(waiter._chef, Chef))
        self.assertTrue(isinstance(waiter._consumer, JSONConsumer))
        self.assertEqual(waiter._stack, [])
        self.assertEqual(waiter._payload, {})
        self.assertEqual(waiter._chef.method, random_method)

    def test_div_slot_raises_on_unsupported_type(self):
        random_type_name = 'EvenMoreRandomType%d'%random.randint(1,100)
        random_type = type(random_type_name, (), {})
        self.assertRaises(TypeError, Waiter().__div__, random_type())

    def test_successful_call(self):
        mock_chef = self.mox.CreateMock(Chef)
        mock_consumer = self.mox.CreateMock(Consumer)
        mock_http = self.mox.CreateMock(httplib2.Http)

        random_result = random.randint(1,100)
        random_tuple = (random.randint(1,100), random.randint(1,100))
        random_payload= { 'rand-%d'%random.randint(1,100): random.randint(1,100) }
        waiter = Waiter(mock_http, 'GET', mock_chef, mock_consumer)
        waiter/("random-%d.com"%random.randint(1,100))
        waiter._payload = random_payload

        random_cooked_data = { 'rand-%d'%random.randint(1,100): random.randint(1,100) }
        mock_chef.cooked_data = random_cooked_data
        mock_chef.cooks(waiter._stack, waiter._payload).AndReturn(True)
        mock_http.request(**random_cooked_data).AndReturn(random_tuple)
        mock_consumer.handle(*random_tuple).AndReturn(random_result)
        self.mox.ReplayAll()
        result = waiter()
        self.assertEqual(result, random_result)
        self.assertEqual(waiter._stack, [])
        self.assertEqual(waiter._payload, {})
        self.mox.VerifyAll()

    def test_chef_fails_us_on_call(self):
        mock_chef = self.mox.CreateMock(Chef)
        mock_consumer = self.mox.CreateMock(Consumer)
        mock_http = self.mox.CreateMock(httplib2.Http)

        random_result = random.randint(1,100)
        random_tuple = (random.randint(1,100), random.randint(1,100))
        random_payload= { 'rand-%d'%random.randint(1,100): random.randint(1,100) }
        waiter = Waiter(mock_http, 'GET', mock_chef, mock_consumer)
        waiter/("random-%d.com"%random.randint(1,100))
        waiter._payload = random_payload

        random_cooked_data = { 'rand-%d'%random.randint(1,100): random.randint(1,100) }
        mock_chef.errors = []
        mock_chef.cooks(waiter._stack, waiter._payload).AndReturn(False)
        self.mox.ReplayAll()
        self.assertRaises(Waiter.Error, waiter.__call__)
        self.mox.VerifyAll()
