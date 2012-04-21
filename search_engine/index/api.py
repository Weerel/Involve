from multiprocessing.managers import BaseManager
from index import Index

class IndexManager(BaseManager):

    @classmethod
    def default(cls):
         return cls(address=('localhost', 6000), authkey='password')

    @classmethod
    def get_proxy(cls):
        manager = cls.default()
        manager.connect()
        return manager.Index()

IndexManager.register('Index', Index)
