# Only used as a reference for the base of a class


from dataclasses    import dataclass
from base   import Base


@dataclass
class Example(Base):
    val1:bool = True
    do_print = True

    def __post_init__(self):
        super().__init__()


<<<<<<< Updated upstream
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
=======
    def __call__(self, **kwargs):
        # Check input values
        val1 = kwargs.get('val1', self.val1)
        do_print = kwargs.get('do_print', self.do_print)
>>>>>>> Stashed changes


example = Example()