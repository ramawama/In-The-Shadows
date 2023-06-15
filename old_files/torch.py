class Torch():
    def __init__(self):
        self._lit = True
    @property
    def state(self):
        return self._lit
    @state.setter
    def state(self, state):
        self._lit = state