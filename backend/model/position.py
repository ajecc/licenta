class Position:
    D = ['D', 0]
    SB = ['SB', 1]
    BB = ['BB', 2]
    UTG = ['UTG', 3]
    UTG_1 = ['UTG+1', 4]
    UTG_2 = ['UTG+2', 5]

    def __init__(self, position, index):
        self._position = position
        self._index = index

    def get_next(self):
        if self._index == len(__POSITIONS_CACHE) - 1:
            return __POSITIONS_CACHE[0]
        return __POSITIONS_CACHE[self._index + 1]
    
    def __eq__(self, other):
        if type(other) is list:
            if len(other) != 2:
                return False
            return self._position == other[0]
        if type(other) is str:
            return self._position == other
        return self._position == other.position

    @property
    def position(self):
        return self._position

    @property
    def index(self):
        return self._index
         

__POSITIONS_CACHE = [Position(*Position.D), Position(*Position.SB), Position(*Position.BB),
        Position(*Position.UTG), Position(*Position.UTG_1), Position(*Position.UTG_2)]
