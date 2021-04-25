class Position:
    D = ['D', 0]
    SB = ['SB', 1]
    BB = ['BB', 2]
    UTG = ['UTG', 3]
    UTG_1 = ['UTG_1', 4]
    UTG_2 = ['UTG_2', 5]

    def __init__(self, position=None, index=None):
        if position is None and index is None:
            raise ValueError('position and index can\'t both be None')
        if position is None:
            self._index = index
            if self._index == 0:
                self._position = 'D'
            elif self._index == 1:
                self._position = 'SB'
            elif self._index == 2:
                self._position = 'BB'
            elif self._index == 3:
                self._position = 'UTG'
            elif self._index == 4:
                self._position = 'UTG_1'
            else:
                self._position = 'UTG_2'
            return
        self._position = position
        if index is not None:
            self._index = index
        else:
            if self._position == Position.D:
                self._index = 0
            elif self._position == Position.SB:
                self._index = 1
            elif self._position == Position.BB:
                self._index = 2
            elif self._position == Position.UTG:
                self._index = 3
            elif self._position == Position.UTG_1:
                self._index = 4
            else:
                self._index = 5

    def get_next(self):
        if self._index == Position.UTG_2[1]:
            return Position(index=0)
        return Position(index=self._index + 1)
    
    def __eq__(self, other):
        if type(other) is list:
            if len(other) != 2:
                return False
            return self._position == other[0]
        if type(other) is str:
            return self._position == other
        return self._position == other.position
    
    def __str__(self):
        return self._position

    @property
    def position(self):
        return self._position

    @property
    def index(self):
        return self._index
