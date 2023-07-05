from py_basic_commands.base   import Base
from dataclasses    import dataclass
from typing     import Any
from typing    import Optional


class DoNotPrint(Exception):
    """Class that is raised when a message should not be printed"""
    pass


@dataclass
class Fprint(Base):
    nl:bool = True
    end:Optional[str] = None
    sep:str = ' '
    do_print:bool = True

    def __post_init__(self):
        super().__init__(self.do_print)


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

        # Check if printing is required
        if not do_print:
            raise DoNotPrint
        
        # Make args a list
        if not args:
            msg_args = ['']
        else:
            msg_args = list(args)

        # Combine args into a single string
        msg = sep.join([str(arg) for arg in msg_args])

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
    fprint.config(sep=' - ', end='!!!')
    fprint('Hello', 'World')
