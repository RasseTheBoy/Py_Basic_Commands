from py_basic_commands.fscripts.fprint   import Fprint
from py_basic_commands.base   import Base
from dataclasses    import dataclass
from typing         import Optional, Any

fprint = Fprint()


@dataclass
class Finput(Base):
    text:str = 'Input: '
    nl:bool = True
    use_suffix:bool = True
    ret_type:type = str
    do_print:bool = True

    def __post_init__(self):
        super().__init__(self.do_print)


    def __call__(self, text:Optional[str]=None, **kwargs) -> Any:
        """Get input from the user and return it as a specified type.
        
        Parameters
        ----------
        text : str, optional
            The text to prompt the user with. Default is an `'Input: '`.
        ret_type : type, optional
            The type to return the input as. Default is `str`.
        nl : bool, optional
            Whether to append a newline character after the input. Default is `True`.
        use_suffix : bool, optional
            Whether to append a colon character to the end of the prompt text. Default is `True`.

        Returns
        -------
        Any
            The input value, converted to the specified type. If the conversion fails, the value is returned as a string.
        """
        # Get text
        text = text or self.text

        # Get kwargs
        nl = kwargs.get('nl', self.nl)
        use_suffix = kwargs.get('use_suffix', self.use_suffix)
        ret_type = kwargs.get('ret_type', self.ret_type)

        if use_suffix and text.rstrip()[-1] != ':':
            text = f'{text}: '

        inpt = input(text)

        if nl:
            print()

        try:
            return ret_type(inpt)
        except ValueError:
            print(f'Couldn\'t return input {inpt} as {ret_type}')
            print(f'Input type: {type(inpt)}')
            fprint('Returning value as string')
        return inpt


finput = Finput()


if __name__ == '__main__':
    # Test `finput`
    print(finput(text='Enter a number', ret_type=int))