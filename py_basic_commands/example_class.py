# Only used as a reference for the base of a class


from dataclasses    import dataclass
from base   import Base


@dataclass
class Example(Base):
    val1:bool = True
    do_print = True

    def __post_init__(self):
        super().__init__(self.do_print)


    def __call__(self, **kwargs):
        # Check input values
        val1 = kwargs.get('val1', self.val1)
        do_print = kwargs.get('do_print', self.do_print)


example = Example()