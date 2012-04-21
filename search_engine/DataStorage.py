from multiprocessing import freeze_support
from search_engine.index.api import IndexManager
import logging

if __name__ == '__main__':    
    freeze_support()
    logging.info('starting DataStorage')
    manager = IndexManager.default()
    s = manager.get_server()
    s.serve_forever()
