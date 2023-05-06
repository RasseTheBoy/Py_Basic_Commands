from dataclasses    import dataclass
from py_basic_commands.fscripts.fprint   import fprint
from py_basic_commands.base   import Base


@dataclass
class Finput(Base):
    _text:str = 'Input: '
    _nl:bool = True
    _use_suffix:bool = True
    _ret_type:type = str

    def __post_init__(self):
        super().__init__()


    def __call__(self, text:str=None, ret_type:type=None, nl:bool=None, use_suffix:bool=None):
        """Get input from the user and return it as a specified type.
        
        Parameters:
        - `text` (str): The text to prompt the user with. Default is an `'Input: '`.
        - `ret_type` (type): The type to return the input as. Default is `str`.
        - `nl` (bool): Whether to append a newline character after the input. Default is `True`.
        - `use_suffix` (bool): Whether to append a colon character to the end of the prompt text. Default is `True`.
        
        Returns:
        - The input value, converted to the specified type. If the conversion fails, the value is returned as a string.
        """

        text = self._check_input_val(text, self._text)
        nl = self._check_input_val(nl, self._nl)
        use_suffix = self._check_input_val(use_suffix, self._use_suffix)
        ret_type = self._check_input_val(ret_type, self._ret_type)

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
    print(finput('Enter a number', ret_type=int))