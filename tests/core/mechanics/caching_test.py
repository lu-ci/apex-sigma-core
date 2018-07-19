import secrets
from sigma.core.mechanics.caching import Cacher

test_count = 1000


class TestCaching(object):
    @staticmethod
    def get_random_string():
        return secrets.token_hex(secrets.randbelow(20) + 1)

    @staticmethod
    def get_random_integer():
        return secrets.randbelow(999999999999999999999999)

    def get_random_generator(self):
        return secrets.choice([self.get_random_string, self.get_random_integer])

    def test_getter(self):
        cache = Cacher()
        assert cache.get_cache(self.get_random_generator()()) is None

    def test_setter(self):
        cache = Cacher()
        pairs = {}
        for _ in range(test_count):
            random_key = self.get_random_generator()()
            random_val = self.get_random_generator()()
            cache.set_cache(random_key, random_val)
            pairs.update({random_key: random_val})
        for pair in pairs.keys():
            assert cache.get_cache(pair) == pairs.get(pair)

    def test_deleter(self):
        cache = Cacher()
        keys = []
        for _ in range(test_count):
            random_key = self.get_random_generator()()
            random_val = self.get_random_generator()()
            cache.set_cache(random_key, random_val)
            keys.append(random_key)
        for key in keys:
            cache.del_cache(key)
            assert cache.get_cache(key) is None
        assert cache.data == {}
