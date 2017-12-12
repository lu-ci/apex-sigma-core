import threading


class Cacher(object):
    def __init__(self):
        self.data = {}
        self.sem = threading.Event()

    def lock(self):
        self.sem.set()

    def unlock(self):
        self.sem.clear()

    def get_cache(self, key):
        self.lock()
        value = self.data.get(key)
        self.unlock()
        return value

    def set_cache(self, key, value):
        self.lock()
        self.data.update({key: value})
        self.unlock()

    def del_cache(self, key):
        if key in self.data:
            self.lock()
            self.data.pop(key)
            self.unlock()
