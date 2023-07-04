from dataclasses    import dataclass
from py_basic_commands.fscripts import Finput
from py_basic_commands.base   import Base
from typing     import Any

# ------- Global Variables -------

finput = Finput()

# ------- Custtom Exceptions -------

class InavlidInputError(Exception):
    def __init__(self, msg:str):
        super().__init__(msg)

# ------- Choose From List -------

@dataclass
class ChooseFromList(Base):
<<<<<<< Updated upstream
    _header_text:str    = ''
    _header_nl:bool     = False
    _input_text:str     = 'Input index: '
    _choose_total:int   = 1
    _start_num:int      = 0
    _choose_until_correct:bool = True

=======
    """Prompt the user to choose one or more values from a list"""
    header_text:str    = ''
    header_nl:bool     = False
    input_text:str     = 'Input index: '
    choose_total:int   = 0
    ret_single_as_str:bool  = False
    start_num:int      = 1
    choose_until_correct:bool = True
    do_print:bool      = True
>>>>>>> Stashed changes

    def __post_init__(self):
        super().__init__(self.do_print)


<<<<<<< Updated upstream
    def config(self, **kwargs):
        """Configure variables"""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'header_text':
                self._header_text = value
            elif key == 'header_nl':
                self._header_nl = value
            elif key == 'input_text':
                self._input_text = value
            elif key == 'choose_total':
                self._choose_total = value
            elif key == 'start_num':
                self._start_num = value
            elif key == 'choose_until_correct':
                self._choose_until_correct = value


    def __call__(self, _array:Any, header_text:str=None, header_nl:bool=None, input_text:str=None, choose_total:int=None, start_num:int=None, choose_until_correct:bool=None) -> list:
=======
    def _check_input(self, user_input:str, array:list, choose_total:int, start_num:int) -> list:
        """Check if the user input is valid
        
        Args:
            user_input (str): User input
            array (list): List of values to choose from
            
        Returns:
            list: List of indexes for the chosen values
        
        Raises:
            InavlidInputError: If the user input is invalid
        """

        # Check if user input is not an empty string
        if user_input == '':
            raise InavlidInputError('Input cannot be empty')
        
        # Split user input into a list
        input_lst = user_input.split(' ')

        # check if user input is valid
        if choose_total <= 0:
            # Any amount of values
            if len(input_lst) > len(array):
                raise InavlidInputError(f'Input cannot be more than {len(array)} values')
            
        elif choose_total == 1:
            # Single value
            if len(input_lst) > 1:
                raise InavlidInputError('Input cannot be more than 1 value')
            
        else:
            # Multiple values
            if len(input_lst) != choose_total:
                raise InavlidInputError(f'Input must be {choose_total} values')
        
        chosen_indx_lst = []
        # Check if user input is valid index
        for input_val in input_lst:
            try:
                input_val = int(input_val)

                if input_val < start_num or input_val >= len(array)+start_num:
                    raise InavlidInputError(f'Input must be a valid index between {start_num} and {len(array)+start_num-1}')

                if input_val in chosen_indx_lst:
                    raise InavlidInputError('Input cannot contain duplicate values')
                
                chosen_indx_lst.append(input_val-start_num)

            except ValueError:
                raise InavlidInputError('Input must be an integer')
            except IndexError:
                raise InavlidInputError(f'Input must be a valid index between {start_num} and {len(array)+start_num-1}')
            
        return chosen_indx_lst


    def __call__(self, array:Any, **kwargs) -> Any:
>>>>>>> Stashed changes
        """Prompt the user to choose one or more values from a list.
        
        Args:
            array (Any): List of values to choose from
            header_text (str, optional): Header text to display. Defaults to ''
            header_nl (bool, optional): Whether to print a newline after the header text. Defaults to False
            input_text (str, optional): Text to display before the input. Defaults to 'Input index: '
            choose_total (int, optional): The amount of values to choose. Defaults to 0 (0 = any amount, 1 = single value, >1 = multiple values)
            ret_single_as_str (bool, optional): Whether to return a single value as a string. Defaults to False
            start_num (int, optional): The starting index number. Defaults to 1
            choose_until_correct (bool, optional): Whether to keep prompting the user until the correct amount of values are chosen. Defaults to True

        Returns:
            Any: List of chosen values or a single value potentially as a string
        """

        # Check input values
<<<<<<< Updated upstream
        header_text = self._check_input_val(header_text, self._header_text)
        header_nl = self._check_input_val(header_nl, self._header_nl)
        input_text = self._check_input_val(input_text, self._input_text)
        choose_total = self._check_input_val(choose_total, self._choose_total)
        start_num = self._check_input_val(start_num, self._start_num)
        choose_until_correct = self._check_input_val(choose_until_correct, self._choose_until_correct)
        
=======
        header_text = kwargs.get('header_text', self.header_text)
        header_nl   = kwargs.get('header_nl', self.header_nl)
        input_text  = kwargs.get('input_text', self.input_text)
        choose_total= kwargs.get('choose_total', self.choose_total)
        start_num   = kwargs.get('start_num', self.start_num)
        choose_until_correct = kwargs.get('choose_until_correct', self.choose_until_correct)
>>>>>>> Stashed changes

        if not header_text:
            if choose_total == 1:
                header_text = '---Choose 1 value---'
            elif choose_total <= 0:
                header_text = '---Choose any amount of values---'
            else:
                header_text = f'---Choose {choose_total} values---'

        print(header_text)
        if header_nl:
            print()

        for indx, val in enumerate(array):
            print(f'({indx+start_num}) {val}')
        print()

        # Get user input
        while True:
            user_input = finput(text=input_text)

            try:
                value_indx_lst = self._check_input(user_input, array, choose_total, start_num)
            except InavlidInputError as e:
                print(e)
                continue

            print('No errors')
            break
        
        chosen_value_lst = [array[indx] for indx in value_indx_lst]

        if choose_total == 1 and self.ret_single_as_str:
            return chosen_value_lst[0]
        
        return chosen_value_lst


choose_from_list = ChooseFromList()


# ------- Testing -------

if __name__ == '__main__':
    alphabet_lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print(choose_from_list(alphabet_lst, start_num=3))