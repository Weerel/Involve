class Space:
    def __init__(self, dimension):
        self._dimension = dimension
        self._list = self.get_array(0, dimension)

    def get_val(self, coord):
        val = self._list
        for i in coord:
            val = val[i]
        return val
            
    def set_val(self ,coord, val):
        tmp = self._list
        for i in coord[:-1]:
            tmp = tmp[i]
        tmp[coord[-1]] = val        

    def get_array(self, level, dimension):
        if( level != len(dimension) ):
            return [self.get_array(level+1, dimension) for i in range(dimension[level])]
        else:
            return 0
