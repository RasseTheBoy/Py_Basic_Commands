import executing, sys

from py_basic_commands.base   import Base
from dataclasses    import dataclass
from textwrap   import dedent


@dataclass
class FprintArray(Base):
    header:str=''
    indx_brackets:str='[]'
    print_num=False
    start_num:int=0
    nl:bool=True
    do_print:bool=True

    def __post_init__(self):
        super().__init__(self.do_print)


    def __call__(self, arr, **kwargs) -> None:
        """This function prints the elements of an array along with their index numbers.

        Parameters
        ----------
        arr : list|set|tuple|dict
            The input array whose elements are to be printed.
        header : str, optional
            The header message to be printed before the array elements. Defaults is ''.
        indx_brackets : str, optional
            The type of brackets to be used for index numbers. Defaults is '`[]`'.
        print_num : bool, optional
            Whether to print the index numbers of the array elements. Default is `False`.
        start_num : int, optional
            First shown value starts with this number. Default is `0`.
        nl : bool, optional
            Whether to append a newline character after the input. Default is `True`
        """

        def _get_array_name() -> str:
            """Get the name of the input array.
            
            Returns
            -------
            str
                The name of the input array"""
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
            inpt_array_name = source.get_text_with_indentation(callNode.args[0]) # type: ignore

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
        header      = kwargs.get('header', self.header)
        indx_brackets = kwargs.get('indx_brackets', self.indx_brackets)
        print_num   = kwargs.get('print_num', self.print_num)
        start_num   = kwargs.get('start_num', self.start_num)
        nl          = kwargs.get('nl', self.nl)

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