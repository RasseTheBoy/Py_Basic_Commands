# Only used as a reference for the base of a class

import sys
sys.path.append('..')


from dataclasses    import dataclass
from base   import Base


@dataclass
class Example(Base):
    _val1:bool = True

    def __post_init__(self):
        super().__init__()


    def config(self, **kwargs):
        """Configure variables"""
        self._config(**kwargs)

        if 'val1' in kwargs:
            self._val1 = kwargs['val1']
        elif 'val2' in kwargs:
            self._val2 = kwargs['val2']


    def __call__(self, val1:bool=None):

        # Check input values
        val1 = self._check_input_val(val1, self._val1)


example = Example()