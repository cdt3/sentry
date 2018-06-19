"""
sentry.utils.canonical
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2018 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import, print_function

import copy
import collections
import six

__all__ = ('CanonicalKeyDict', 'get_canonical_name', 'make_canonical')

canonical_KEY_MAPPING = {
    'sentry.interfaces.Exception': 'exception',
    'sentry.interfaces.Message': 'logentry',
    'sentry.interfaces.Stacktrace': 'stacktrace',
    'sentry.interfaces.Template': 'template',
    'sentry.interfaces.Query': 'query',
    'sentry.interfaces.Http': 'request',
    'sentry.interfaces.User': 'user',
    'sentry.interfaces.Csp': 'csp',
    'sentry.interfaces.AppleCrashReport': 'applecrashreport',
    'sentry.interfaces.Breadcrumbs': 'breadcrumbs',
    'sentry.interfaces.Contexts': 'contexts',
    'sentry.interfaces.Threads': 'threads',
    'sentry.interfaces.DebugMeta': 'debug_meta',
}


def get_canonical_name(key):
    return canonical_KEY_MAPPING.get(key, key)


def get_canonical_data(data):
    if isinstance(data, CanonicalKeyDict):
        return copy.copy(data.data)

    result = type(data)()
    for key, value in six.iteritems(data):
        canonical_key = get_canonical_name(key)
        if key == canonical_key or canonical_key not in result:
            result[canonical_key] = value

    return result


def make_canonical(data):
    if isinstance(data, CanonicalKeyDict):
        return data.data

    for key, value in six.iteritems(data):
        canonical_key = get_canonical_name(key)
        if key != canonical_key:
            data.setdefault(canonical_key, value)
            del data[key]

    return data


class CanonicalKeyDict(collections.MutableMapping):
    def __init__(self, data, passthrough=False):
        self.data = make_canonical(data)

    def copy(self):
        rv = object.__new__(self.__class__)
        rv.data = copy.copy(self.data)
        return rv

    __copy__ = copy

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return get_canonical_name(key) in self.data

    def __getitem__(self, key):
        return self.data[get_canonical_name(key)]

    def __setitem__(self, key, value):
        self.data[get_canonical_name(key)] = value

    def __delitem__(self, key):
        del self.data[get_canonical_name(key)]
