class Sector:
    def __init__(self, in_power, length, damping, out_power):
        self._in_power = in_power
        self._length = length
        self._out_power = out_power
        self._damping = damping

    @property
    def in_power(self):
        return self._in_power

    @property
    def out_power(self):
        return self._out_power

    @property
    def length(self):
        return self._length

    @property
    def damping(self):
        return self._damping

