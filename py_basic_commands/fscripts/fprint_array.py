import executing, sys

from dataclasses    import dataclass
from textwrap   import dedent
from py_basic_commands.base   import Base


@dataclass
class FprintArray(Base):
    _header:str=''
    _indx_brackets:str='[]'
    _print_num=False
    _start_num:int=0
    _nl:bool=True

    def __post_init__(self):
        super().__init__()


    def __call__(self, arr, header:str=None, indx_brackets:str=None, print_num=None, start_num:int=None, nl:bool=None) -> None:
        """This function prints the elements of an array along with their index numbers.

        Parameters:
        - `arr` (`list`|`set`|`tuple`|`dict`): The input array whose elements are to be printed.
        - `header` (str):  The header message to be printed before the array elements. Defaults is ''.
        - `indx_brackets` (str): The type of brackets to be used for index numbers. Defaults is '`[]`'.
        - `start_num` (int): First shown value starts with this number. Default is `0`.
        - `nl` (bool): Whether to append a newline character after the input. Default is `True`
        
        Returns:
        - `None`
        """

        def _get_array_name() -> str:
            """Get the name of the input array."""
            class Source(executing.Source):
                def get_text_with_indentation(self, node):
                    result = self.asttokens().get_text(node)
                    if '\n' in result:
                        result = ' ' * node.first_token.start[1] + result
                        result = dedent(result)
                    result = result.strip()
                    return result
            
            callFrame = sys._getframe(2)
            callNode = Source.executing(callFrame).node
            source = Source.for_frame(callFrame)
            inpt_array_name = source.get_text_with_indentation(callNode.args[0])

            return inpt_array_name


        def _print_output(text) -> None:
            """Print the output of the array elements and their index numbers if `print_num` is `True`. Otherwise, just print the array elements.
            If the input is a dictionary, then print the key-value pairs."""
            if text.__class__.__name__ == 'dict':
                return self.__call__(text, header=header, indx_brackets=indx_brackets, print_num=print_num, start_num=start_num, nl=nl)

            if print_num:
                print(f'{config_indx_num(indx)} {text}')
            else:
                print(text)


        # Check input values
        header      = self._check_input_val(header, self._header)
        indx_brackets = self._check_input_val(indx_brackets, self._indx_brackets)
        print_num   = self._check_input_val(print_num, self._print_num)
        start_num   = self._check_input_val(start_num, self._start_num)
        nl          = self._check_input_val(nl, self._nl)

        config_indx_num = lambda indx : f'{indx_brackets[0]}{indx}{indx_brackets[1]}'

        arr_type = arr.__class__.__name__

        # Check if the input is a valid array
        if arr_type in ['list', 'set', 'tuple', 'dict']:
            if not arr:
                print(f'Array is empty: {_get_array_name()}')
                return

            if header:
                print(header)

            for indx, value in enumerate(arr, start=start_num):
                _print_output(value)

            if nl:
                print()

        elif arr_type == 'dict':
            for indx, (key, value) in enumerate(arr.items(), start=start_num):
                _print_output(f'{key}: {value}')
        
        else:
            arr_name = _get_array_name()
            print(f'Given array ({arr_name}) is not a valid format: {arr_type}')
            return


fprint_array = FprintArray()