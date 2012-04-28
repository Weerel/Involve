from search_engine.modeling.space import Space
import array, collections, math

def get_pages(dimension, max_depth = 500):
    dimension = array.array('i', dimension)
    s = Space(dimension)
    v = [0 for d in dimension]
    frontier_current = collections.deque([v])
    s.set_val(v, 1)
    frontier_next = collections.deque()
    depth = 0
    yield depth, len(frontier_current)
    while len(frontier_current) > 0 and max_depth > depth:
        depth += 1
        while len(frontier_current) > 0:        
            v = frontier_current.pop()
            for i, x in enumerate(v):
                n = dimension[i]
                for k in -1, 1:
                    v_neighbor = v[:]
                    v_neighbor[i] = (x + k) % n
                    if s.get_val(v_neighbor) == 0:
                        frontier_next.append(v_neighbor)
                        s.set_val(v_neighbor, 1)
        frontier_current, frontier_next = frontier_next, frontier_current
        yield depth, len(frontier_current)

def split(m):
    l = []
    for row in m:
        for i, x in enumerate(row):
            if len(l) <= i:
                l.append([])
            l[i].append(x)
    return l

def dimensions(data):
    i = 0
    vx = []
    vy = []
    for x, y in data:
        vx.append(x)
        vy.append(y)
        if len(vx) == 3:
            x = vx[1]
            y = vy[1]
            dy = float(vy[2] - vy[0])/(vx[2] - vx[0])
            yield x, max(x*dy/y + 1, 0)
            del vx[0]
            del vy[0]
            
            
