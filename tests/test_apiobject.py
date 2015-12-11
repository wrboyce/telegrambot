import unittest

from mock import Mock

from telegrambot import api


class TestAPIObjectAttributes(unittest.TestCase):
    def test_not_implemented(self):
        class Foo(api.APIObject):
            pass
        self.assertRaises(NotImplementedError, Foo.from_api, None)

    def test_required_value(self):
        class Foo(api.APIObject):
            _api_attrs = (('id', int, TypeError),)
        self.assertRaises(TypeError, Foo.from_api, None)

    def test_default_value(self):
        class Foo(api.APIObject):
            _api_attrs = (('id', int, None),)
        foo = Foo.from_api(api=None)
        self.assertIsNone(foo.id)

    def test_self_type_is_resolved(self):
        class Foo(api.APIObject):
            _api_attrs = (('foo', 'self', None),)
        payload = {'foo': {}}
        foo = Foo.from_api(api=None, **payload)
        self.assertIsInstance(foo.foo, Foo)

    def test_str_type_is_unicode(self):
        class Foo(api.APIObject):
            _api_attrs = (('id', str, None),)
        payload = {'id': 'Hello, World'}
        foo = Foo.from_api(api=None, **payload)
        self.assertIsInstance(foo.id, unicode)

    def test_reserved_attr_name(self):
        class Foo(api.APIObject):
            _api_attrs = (('from', str, None),)
        payload = {'from': 'Hello, World'}
        foo = Foo.from_api(api=None, **payload)
        self.assertEqual(foo.froom, payload['from'])

    def test_single_value(self):
        class Foo(api.APIObject):
            _api_attrs = (('id', str, None),)
        payload = {'id': 'Hello, World'}
        foo = Foo.from_api(api=None, **payload)
        self.assertEqual(foo.id, payload['id'])

    def test_dict_value(self):
        class Bar(api.APIObject):
            _api_attrs = (('id', int, None),)
        class Foo(api.APIObject):
            _api_attrs = (('bar', Bar, None),)
        payload = {'bar': {'id': 1}}
        foo = Foo.from_api(api=None, **payload)
        self.assertIsInstance(foo.bar, Bar)
        self.assertEqual(foo.bar.id, payload['bar']['id'])

    def test_value_arrays(self):
        class Foo(api.APIObject):
            _api_attrs = (('ids', [str], None),)
        payload = {'ids': [1, 2, 3, 4, 5]}
        foo = Foo.from_api(api=None, **payload)
        expected = [unicode(i) for i in payload['ids']]
        self.assertItemsEqual(foo.ids, expected)

    def test_value_array_objects(self):
        class Bar(api.APIObject):
            _api_attrs = (('id', int, None),)
        class Foo(api.APIObject):
            _api_attrs = (('bars', [Bar], None),)
        payload = {'bars': [{'id': 1}, {'id': 2}, {'id': 3}]}
        foo = Foo.from_api(api=None, **payload)
        self.assertIsInstance(foo.bars, list)
        self.assertIsInstance(foo.bars[0], Bar)

    def test_value_nested_array_objects(self):
        class Bar(api.APIObject):
            _api_attrs = (('id', int, None),)
        class Foo(api.APIObject):
            _api_attrs = (('bars', [[Bar]], None),)
        payload = {'bars': [[{'id': 1}, {'id': 2}], [{'id': 3}]]}
        foo = Foo.from_api(api=None, **payload)
        self.assertIsInstance(foo.bars, list)
        self.assertEqual(len(foo.bars), 2)
        self.assertIsInstance(foo.bars[0], list)
        self.assertEqual(len(foo.bars[0]), 2)
        self.assertEqual(len(foo.bars[1]), 1)
        self.assertIsInstance(foo.bars[0][0], Bar)


class TestAPIObjectAPIMethod(unittest.TestCase):
    def test_not_implemented(self):
        class Foo(api.APIObject):
            pass
        foo = Foo(api=None)
        self.assertRaises(NotImplementedError, foo.api_method)

    def test_get_method(self):
        class Foo(api.APIObject):
            _api_method = 'test'
        class API(object):
            def test(self): return
        foo = Foo(api=API)
        self.assertEqual(foo.api_method(), API.test)


class TestAPIObjectAPIPayload(unittest.TestCase):
    def test_not_implemented(self):
        class Foo(api.APIObject):
            pass
        foo = Foo(api=None)
        self.assertRaises(NotImplementedError, foo.api_payload)

    def test_payload(self):
        class Foo(api.APIObject):
            _api_payload = ('a', 'c')
            def __init__(self, api, a, b, c):
                self.api = api
                self.a = a
                self.b = b
                self.c = c
        foo = Foo(api=None, a='A', b='B', c='C')
        self.assertDictEqual(foo.api_payload(), {'a': 'A', 'c': 'C'})


class TestAPIObjectAPISend(unittest.TestCase):
    def test_send(self):
        class Foo(api.APIObject):
            _api_method = 'test'
            _api_payload = ('a', 'c')
            def __init__(self, api, a, b, c):
                self.api = api
                self.a = a
                self.b = b
                self.c = c
        bot = Mock()
        Foo(api=bot, a='A', b='B', c='C').send()
        bot.test.assert_called_with(a='A', c='C')