class Cacher(object):
    def __init__(self):
        self.data = {}

    def get_cache(self, key):
        value = self.data.get(key)
        return value

    def set_cache(self, key, value):
        self.data.update({key: value})

    def del_cache(self, key):
        if key in self.data:
            self.data.pop(key)
