""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import datetime


class APIObject(object):
    _api_attrs = ()

    _api_method = None
    _api_payload = ()

    def __init__(self, api):
        self.api = api
        for attr_name, attr_type, attr_default in self._api_attrs:
            if not hasattr(self, attr_name):
                default = '' if attr_type is str else None
                setattr(self, attr_name, default)

    @classmethod
    def from_api(cls, api, **kwargs):
        """ Parses a payload from the API, guided by `_api_attrs` """
        if not cls._api_attrs:
            raise NotImplementedError()

        def resolve_attribute_type(attr_type):
            # resolve arrays of types down to base type
            while isinstance(attr_type, list):
                attr_type = attr_type[0]
            # attribute type 'self' resolves to current class
            if attr_type == 'self':
                attr_type = cls
            # attribute type 'date' is a unix timestamp
            if attr_type == 'date':
                attr_type = datetime.datetime.fromtimestamp
            # string attributes should use unicode literals
            if attr_type is str:
                attr_type = unicode
            # if attribute type is an APIObject, use the from_api factory method and pass the `api` argument
            if hasattr(attr_type, 'from_api'):
                return lambda **kw: attr_type.from_api(api, **kw)
            return attr_type

        def instantiate_attr(attr_value, attr_type):
            if isinstance(attr_value, dict):
                return attr_type(**attr_value)
            return attr_type(attr_value)

        def instantiate_array(attr_values, attr_type):
            func = instantiate_attr
            if isinstance(attr_values[0], list):
                func = instantiate_array
            return [func(val, attr_type) for val in attr_values]

        def instantiate(attr_value, attr_type):
            if isinstance(attr_value, list):
                return instantiate_array(attr_value, attr_type)
            return instantiate_attr(attr_value, attr_type)

        instance = cls(api)
        for attr_name, attr_type, attr_default in cls._api_attrs:
            # grab the current attribute value
            attr_value = kwargs.get(attr_name, attr_default)
            # default of TypeError means a required attribute, raise Exception
            if attr_value is TypeError:
                raise TypeError('{} requires argument {}'.format(cls.__name__, attr_name))
            attr_type = resolve_attribute_type(attr_type)
            # if value has been provided from API, instantiate it using `attr_type`
            if attr_value != attr_default:
                attr_value = instantiate(attr_value, attr_type)
            # rename the 'from' variable, reserved word
            if attr_name == 'from':
                attr_name = 'froom'
            # and finally set the attribute value on the instance
            setattr(instance, attr_name, attr_value)
        return instance

    def api_method(self):
        """ Returns the api method to `send` the current API Object type """
        if not self._api_method:
            raise NotImplementedError()
        return getattr(self.api, self._api_method)

    def api_payload(self):
        """ Generates a payload ready for submission to the API, guided by `_api_payload` """
        if not self._api_payload:
            raise NotImplementedError()
        payload = {}
        for attr_name in self._api_payload:
            value = getattr(self, attr_name, None)
            if value is not None:
                payload[attr_name] = value
        return payload

    def send(self, **kwargs):
        """ Combines api_payload and api_method to submit the current object to the API """
        payload = self.api_payload()
        payload.update(**kwargs)
        return self.api_method()(**payload)