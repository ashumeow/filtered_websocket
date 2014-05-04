import collections


class BaseStorageObject(object):
    storage = None

    def add(self, key, value):
        raise NotImplementedError

    def remove(self, key, value):
        raise NotImplementedError

class DefaultStorageObject(BaseStorageObject):

    def __init__(self, *args, **kwargs):
        self.storage = collections.defaultdict(set)

    def add(self, key, value):
        self.storage[key].add(value)

    def remove(self, key, value):
        self.storage[key].remove(value)
