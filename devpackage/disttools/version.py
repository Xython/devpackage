from Redy.Tools.Version import Version as _Version

class Version(_Version):
    def carry_over(self, version_number_idx: int, max: int):
        _numbers = list(self._numbers)
        current = _numbers[version_number_idx]
        if version_number_idx is 0 or current < max:
            return
        
        over = current // max
        current = current % max
        _numbers[version_number_idx-1] += over
        _numbers[version_number_idx] = current
