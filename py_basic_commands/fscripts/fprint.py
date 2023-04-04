from dataclasses    import dataclass
from typing     import Any
from py_basic_commands.base   import Base

@dataclass
class Fprint(Base):
    _nl:bool = True
    _flush:bool = False
    _end = None

    def __post_init__(self):
        super().__init__()


    def config(self, **kwargs):
        """Configure variables"""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'nl':
                self._nl = value
            elif key == 'flush':
                self._flush = value
            elif key == 'end':
                self._end = value


    def __call__(self, *args:Any, nl:bool=None, flush:bool=None, do_print:bool=None, end:str=None) -> None:
        """Print one or more objects to the console, with optional newline, flushing, and ending characters.
        
        Parameters:
        - `args` (*Any): One or more objects to print.
        - `nl` (bool): Whether to append a newline character to the output.
        - `flush` (bool): Whether to flush the output buffer.
        - `do_print` (bool): Whether to actually print the output.
        - `end` (str): The string to print at the end of the output.
        """
        # TODO: Add `sep` input parameter (separator between objects to print)

        # Check input values
        nl = self._check_input_val(nl, self._nl) 
        flush = self._check_input_val(flush, self._flush)
        do_print = self._check_input_val(do_print, self._do_print)
        end = self._check_input_val(end, self._end)
        if not args:
            args = ('\n')

        if not do_print:
            return

        for arg_indx, arg in enumerate(args):
            if arg_indx == len(args)-1:
                print(arg, end=end, flush=flush)
            else:
                print(arg, end=' ', flush=flush)

        if nl and not end:
            print()


fprint = Fprint()


if __name__ == '__main__':
    fprint('hello', do_print=False)