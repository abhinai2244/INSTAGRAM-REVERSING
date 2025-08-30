import math
import random
import functools

class Reverse:
    def random_uint32():
        return math.floor(random.random() * 4294967296)

    def to_string(n):
        chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        result = ''
        while n:
            n, r = divmod(n, 36)
            result = chars[r] + result
        return result or '0'

    def machine_id():
        return functools.reduce(
            lambda a, _: a + Reverse.to_string(Reverse.random_uint32()),
            [0] * 8,
            ''
        )

    def web_session_id(extra=False, c=None):
        def _p(j=6):
            a = math.floor(random.random() * 2176782336)
            a = Reverse.to_string(a)
            return '0' * (j - len(a)) + a

        if extra:
            a = _p()
            b = _p()
        else:
            a = '' # del webstorage
            b = '' # del webstorage
        if c is None:
            c = _p()
        return a + ':' + b + ':' + c

    def get_numeric_value(string):
        c = 0
        sprinkle_version = '2'

        for x in range(len(string)):
            c += ord(string[x])
        return sprinkle_version + str(c)
