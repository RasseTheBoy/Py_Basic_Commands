from dataclasses    import dataclass
from py_basic_commands.fscripts import fprint, finput
from typing     import Any
from py_basic_commands.base   import Base


@dataclass
class ChooseFromList(Base):
    _header_text:str    = ''
    _header_nl:bool     = False
    _input_text:str     = 'Input index: '
    _choose_total:int   = 1
    _start_num:int      = 0
    _choose_until_correct:bool = True


    def __post_init__(self):
        super().__init__()


    def __call__(self, _array:Any, header_text:str=None, header_nl:bool=None, input_text:str=None, choose_total:int=None, start_num:int=None, choose_until_correct:bool=None) -> list:
        """Prompt the user to choose one or more values from a list.
        
        Parameters:
        - `_array` (Any): The list of values to choose from.
        - `header_text` (str): The text to display as a header. Default is `''`
        - `header_nl` (bool): Whether to append a newline character after the header. Default is `False`
        - `input_text` (str): The text to prompt the user with. Default is `'Input index: '`
        - `choose_total` (int): The number of values to choose. Default is `1`
        - `start_num` (int): The number to start the indexing from. Default is `0`
        - `choose_until_correct` (bool): Whether to keep prompting the user until a correct input is given. Default is `True`
        
        Returns:
        - `list`: A list of the chosen values.
        """

        # Check input values
        header_text = self._check_input_val(header_text, self._header_text)
        header_nl = self._check_input_val(header_nl, self._header_nl)
        input_text = self._check_input_val(input_text, self._input_text)
        choose_total = self._check_input_val(choose_total, self._choose_total)
        start_num = self._check_input_val(start_num, self._start_num)
        choose_until_correct = self._check_input_val(choose_until_correct, self._choose_until_correct)
        

        if not header_text:
            if choose_total == 1:
                header_text = '---Choose 1 value---'
            else:
                header_text = f'---Choose {choose_total} values---'

        fprint(header_text, nl=header_nl)

        for indx, val in enumerate(_array):
            print(f'({indx+start_num}) {val}')
        print()

        chosen_amnt = 0
        while chosen_amnt < choose_total:
            inpt_indx = finput(input_text, ret_type=str, nl=False)
            try:
                inpt_indx = tuple(int(x) for x in inpt_indx.split())

                if len(inpt_indx) != choose_total:
                    print(f'Input has to be {choose_total} values (space separated))')
                    raise ValueError

                elif any({x<start_num for x in inpt_indx}):
                    raise IndexError

                return [_array[x - start_num] for x in inpt_indx]

            except IndexError:
                print(f'Given index is out of range. Value has to be between: {start_num}-{start_num+len(_array)-1}')
            except ValueError:
                pass
            except Exception:
                print(f'Input not a valid index: {inpt_indx}')

            if not choose_until_correct:
                return []


choose_from_list = ChooseFromList()

if __name__ == '__main__':
    # Test the function
    _array = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print(choose_from_list(_array, choose_total=2, start_num=1))