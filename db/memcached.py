# -*- coding: utf-8 -*-
import re       # pip install python-memcached


class Memcached:
    def __init__(self, servers=None, default_timeout=300, **kwargs):
        self.host = kwargs.get('host', '49.232.57.79')
        self.port = kwargs.get('port', 11211)
        self.cache_timeout = default_timeout
        if servers is None or isinstance(servers, (list, tuple)):
            if servers is None:
                servers = ['49.232.57.79:11211']
            self.client = self.get_memcache_connection(servers)
            if self.client is None:
                raise RuntimeError('no memcache module found')
        else:
            self.client = servers

    def set(self, key, value, timeout=None):
        timeout = timeout if timeout else self.cache_timeout
        return self.client.set(key, value, timeout)

    def get(self, key, default=None):
        value = self.client.get(key)
        if not value:
            value = default
        return value

    def get_memcache_connection(self, servers):
        try:
            import pylibmc
        except ImportError:
            print("=== 引入pylibmc出错 ===")
        else:
            return pylibmc.Client(servers)

        try:
            from google.appengine.api import memcache
        except ImportError:
            print("=== 引入google出错 ===")
        else:
            return memcache.Client()

        try:
            import memcache
        except ImportError:
            print("=== 引入memcache出错 ===")
        else:
            return memcache.Client(servers)

        try:
            import libmc
        except ImportError:
            print("=== 引入libmc出错 ===")
        else:
            return libmc.Client(servers)


if __name__ == "__main__":
    m = Memcached()
    m.set("name", "liu")
    s = m.get("name")
    print(s)
# http://www.mamicode.com/info-detail-519543.html
# https://www.linuxzen.com/vlogshi-yong-tornadokuang-jia-jie-he-memcachedhuan-cun-ye-mian.html
# https://www.cnblogs.com/yangxiaolan/p/5964303.html
# https://my.oschina.net/1123581321/blog/214091
# https://blog.csdn.net/dutsoft/article/details/71101809


class BaseCache(object):
    """Baseclass for the cache systems.  All the cache systems implement this API or a superset of it."""
    def __init__(self, default_timeout=300):
        self.default_timeout = default_timeout

    def _normalize_timeout(self, timeout):
        if timeout is None:
            timeout = self.default_timeout
        return timeout

    def get(self, key):
        """Look up key in the cache and return the value for it.
        :param key: the key to be looked up.
        :returns: The value if it exists and is readable, else ``None``.
        """
        return None

    def delete(self, key):
        """Delete `key` from the cache.
        :param key: the key to delete.
        :returns: Whether the key existed and has been deleted.
        :rtype: boolean
        """
        return True

    def get_many(self, *keys):
        """Returns a list of values for the given keys.
        For each key an item in the list is created::

            foo, bar = cache.get_many("foo", "bar")

        Has the same error handling as :meth:`get`.

        :param keys: The function accepts multiple keys as positional
                     arguments.
        """
        return [self.get(k) for k in keys]

    def get_dict(self, *keys):
        """Like :meth:`get_many` but return a dict::
            d = cache.get_dict("foo", "bar")
            foo = d["foo"]
            bar = d["bar"]
        :param keys: The function accepts multiple keys as positional
                     arguments.
        """
        return dict(zip(keys, self.get_many(*keys)))

    def set(self, key, value, timeout=None):
        """Add a new key/value to the cache (overwrites value, if key already
        exists in the cache).

        :param key: the key to set
        :param value: the value for the key
        :param timeout: the cache timeout for the key in seconds (if not
                        specified, it uses the default timeout). A timeout of
                        0 indicates that the cache never expires.
        :returns: ``True`` if key has been updated, ``False`` for backend
                  errors. Pickling errors, however, will raise a subclass of
                  ``pickle.PickleError``.
        :rtype: boolean
        """
        return True

    def add(self, key, value, timeout=None):
        """Works like :meth:`set` but does not overwrite the values of already
        existing keys.

        :param key: the key to set
        :param value: the value for the key
        :param timeout: the cache timeout for the key in seconds (if not
                        specified, it uses the default timeout). A timeout of
                        0 indicates that the cache never expires.
        :returns: Same as :meth:`set`, but also ``False`` for already
                  existing keys.
        :rtype: boolean
        """
        return True

    def set_many(self, mapping, timeout=None):
        """Sets multiple keys and values from a mapping.

        :param mapping: a mapping with the keys/values to set.
        :param timeout: the cache timeout for the key in seconds (if not
                        specified, it uses the default timeout). A timeout of
                        0 indicates that the cache never expires.
        :returns: Whether all given keys have been set.
        :rtype: boolean
        """
        rv = True
        for key, value in _items(mapping):
            if not self.set(key, value, timeout):
                rv = False
        return rv

    def delete_many(self, *keys):
        """Deletes multiple keys at once.

        :param keys: The function accepts multiple keys as positional
                     arguments.
        :returns: Whether all given keys have been deleted.
        :rtype: boolean
        """
        return all(self.delete(key) for key in keys)

    def has(self, key):
        """Checks if a key exists in the cache without returning it. This is a
        cheap operation that bypasses loading the actual data on the backend.

        This method is optional and may not be implemented on all caches.

        :param key: the key to check
        """
        raise NotImplementedError(
            '%s doesn\'t have an efficient implementation of `has`. That '
            'means it is impossible to check whether a key exists without '
            'fully loading the key\'s data. Consider using `self.get` '
            'explicitly if you don\'t care about performance.'
        )

    def clear(self):
        """Clears the cache.  Keep in mind that not all caches support
        completely clearing the cache.

        :returns: Whether the cache has been cleared.
        :rtype: boolean
        """
        return True

    def inc(self, key, delta=1):
        """Increments the value of a key by `delta`.  If the key does
        not yet exist it is initialized with `delta`.

        For supporting caches this is an atomic operation.

        :param key: the key to increment.
        :param delta: the delta to add.
        :returns: The new value or ``None`` for backend errors.
        """
        value = (self.get(key) or 0) + delta
        return value if self.set(key, value) else None

    def dec(self, key, delta=1):
        """Decrements the value of a key by `delta`.  If the key does
        not yet exist it is initialized with `-delta`.

        For supporting caches this is an atomic operation.

        :param key: the key to increment.
        :param delta: the delta to subtract.
        :returns: The new value or `None` for backend errors.
        """
        value = (self.get(key) or 0) - delta
        return value if self.set(key, value) else None



