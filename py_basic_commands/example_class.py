# Only used as a reference for the base of a class


from dataclasses    import dataclass
from base   import Base


@dataclass
class Example(Base):
    _val1:bool = True

    def __post_init__(self):
        super().__init__()


    def __call__(self, val1:bool=None, do_print:bool=None):
        # Check input values
        val1 = self._check_input_val(val1, self._val1)
        do_print = self._check_input_val(do_print, self._do_print)


example = Example()