class DummyException(Exception):
    def __init__(self):
        self.message = 'This is a dummy exception, it should never be raised.'
