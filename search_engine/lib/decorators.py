import time, logging

def singleton(c):
    def wrapper(*a):
        instance = None
        if not hasattr(c, '_instance'):
            c._instance = None
        if c._instance is None:
            instance = c(*a)
            c._instance = instance
        else:
            instance = c._instance
        return instance
            
    return wrapper

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print "%s %f" % (method.__name__, te-ts)
        logging.info("%s %f", method.__name__, te-ts)
        return result
    return timed
