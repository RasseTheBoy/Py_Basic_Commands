from dataclasses    import dataclass
from typing     import Any
from py_basic_commands.base   import Base


class DoNotPrint(Exception):
    """Class that is raised when a message should not be printed"""
    pass


@dataclass
class Fprint(Base):
<<<<<<< Updated upstream
    _nl:bool = True
    _flush:bool = False
    _end = None
=======
    nl:bool = True
    end = None
    sep = ' '
>>>>>>> Stashed changes

    def __post_init__(self):
        super().__init__()


<<<<<<< Updated upstream
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
=======
    def _get_msg(self, *args, **kwargs) -> str:
        """Get the message to print.
        
        Parameters
        ----------
        *args : Any
            The values to print
        do_print : bool, optional
            Whether to print or not. Default is True
        sep : str, optional
            The string to use to separate the given values. Default is ' '
        
        Returns
        -------
        str
            The message to print"""
        # Get kwargs values
        do_print = kwargs.get('do_print', self.do_print)
        sep = kwargs.get('sep', self.sep)
>>>>>>> Stashed changes

        # Check if printing is required
        if not do_print:
<<<<<<< Updated upstream
            return

        for arg_indx, arg in enumerate(args):
            if arg_indx == len(args)-1:
                print(arg, end=end, flush=flush)
            else:
                print(arg, end=' ', flush=flush)
=======
            raise DoNotPrint
        
        # Make args a list
        if not args:
            msg_args = ['']
        else:
            msg_args = list(args)

        # Combine args into a single string
        msg = sep.join([str(arg) for arg in msg_args])
>>>>>>> Stashed changes

        return msg


    def _print_msg(self, msg:str, error:bool=False, **kwargs):
        # Get kwargs values
        nl = kwargs.get('nl', self.nl)
        end = kwargs.get('end', self.end)

        # Print the message
        if end and not error:
            print(msg, end=end)
        else:
            print(msg)

        # Print a newline if required
        if nl:
            print()


    def error(self, *args, **kwargs):
        """Using the `fprint` function, print and error message to the console.
        
        Parameters
        ----------
        *args : Any
            The values to print
        do_print : bool, optional
            Whether to print or not. Default is True
        nl : bool, optional
            Whether to print a newline after the message. Default is True
        sep : str, optional
            The string to use to separate the given values. Default is ' '
        """
        try:
            msg = self._get_msg(*args, **kwargs)
        except DoNotPrint:
            return
        
        error_msg = f'--[!]-- {msg} --[!]--'
        self._print_msg(error_msg, error=True, **kwargs)


    def __call__(self, *args, **kwargs):
        """Print the given values to the console.
        
        Parameters
        ----------
        *args : Any
            The values to print
        do_print : bool, optional
            Whether to print or not. Default is True
        nl : bool, optional
            Whether to print a newline after the message. Default is True
        end : str, optional
            The string to print at the end of the message. Default is None
        sep : str, optional
            The string to use to separate the given values. Default is ' '
        """
        try:
            msg = self._get_msg(*args, **kwargs)
        except DoNotPrint:
            return
        
        self._print_msg(msg, **kwargs)


fprint = Fprint()


if __name__ == '__main__':
<<<<<<< Updated upstream
    fprint('hello', do_print=False)
=======
    fprint.config(sep=' - ', end='!!!')
    fprint('Hello', 'World')
>>>>>>> Stashed changes
