import sys, executing

from traceback  import format_exc
from functools  import wraps
from textwrap   import dedent
from fscripts     import fprint
from typing     import Any


def try_traceback(print_traceback=False):
    """Decorator to catch and handle exceptions raised by a function.
    
    Parameters:
    - `print_traceback` (bool): Whether to skip printing the traceback information.
    
    Returns:
    - `function`: The decorated function.
    """

    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if print_traceback:
                    fprint(format_exc())
                return None
        return wrapper
    return try_except


def finput(text:str='', nl:bool=True, use_suffix:bool=True, ret_type:type=str):
    """Get input from the user and return it as a specified type.
    
    Parameters:
    - `text` (str): The text to prompt the user with. Default is an empty string.
    - `nl` (bool): Whether to append a newline character after the input. Default is True.
    - `use_suffix` (bool): Whether to append a colon character to the end of the prompt text. Default is True.
    - `ret_type` (type): The type to return the input as. Default is `str`.
    
    Returns:
    - The input value, converted to the specified type. If the conversion fails, the value is returned as a string.
    """

    if not text:
        text = 'Input: '
    elif use_suffix and text.rstrip()[-1] != ':':
        text = f'{text}: '

    inpt = input(text)

    if nl:
        print()

    try:
        return ret_type(inpt)
    except:
        print(f'Couldn\'t return input {inpt} as {ret_type}')
        print(f'Input type: {type(inpt)}')
        fprint('Returning value as string')
    return inpt


def enter_to_continue(text:str='', nl:bool=True, use_suffix:bool=True) -> bool:
    """Prompt the user to press the enter key to continue.
    
    Parameters:
    - `text` (str): The text to prompt the user with.
    - `nl` (bool): Whether to append a newline character after the input.
    - `use_suffix` (bool): Whether to append '(press enter to continue)' to the end of the prompt text.
    
    Returns:
    - `bool`: True if the user pressed the enter key, False otherwise.
    """

    if text and use_suffix:
        text = f'{text} (press enter to continue or type anything to break) '

    elif not text and use_suffix:
        text = 'Press enter to continue or type anything to break... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def fprint_array(arr, header:str='', indx_brackets:str='[]', print_num=False, start_num:int=0, nl:bool=True) -> None:
    """This function prints the elements of an array along with their index numbers.

    Parameters:
    - `arr` (`list`|`set`|`tuple`|`dict`): The input array whose elements are to be printed.
    - `header` (str):  The header message to be printed before the array elements. Defaults is ''.
    - `indx_brackets` (str): The type of brackets to be used for index numbers. Defaults is '`[]`'.
    - `nl` (bool): Whether to append a newline character after the input.
    
    Returns:
    - `None`
    """

    def _get_array_name() -> str:
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


    def _print_output(text):
        if text.__class__.__name__ == 'dict':
            return fprint_array(text, header=header, indx_brackets=indx_brackets, print_num=print_num, start_num=start_num, nl=nl)

        if print_num:
            print(f'{config_indx_num(indx)} {text}')
        else:
            print(text)

    config_indx_num = lambda indx : f'{indx_brackets[0]}{indx}{indx_brackets[1]}'

    arr_type = arr.__class__.__name__

    match arr_type:
        case 'list' | 'set' | 'tuple':
            if not arr:
                print(f'Array is empty: {_get_array_name()}')
                return

            if header:
                print(header)

            for indx, value in enumerate(arr, start=start_num):
                _print_output(value)

            if nl:
                print()

        case 'dict':
            for indx, (key, value) in enumerate(arr.items(), start=start_num):
                _print_output(f'{key}: {value}')

        case _:
            arr_name = _get_array_name()
            print(f'Given array ({arr_name}) is not a valid format: {arr_type}')
            return


def choose_from_list(_array:Any, header_text:str='', header_nl:bool=False, input_text:str='Input index: ', choose_total:int=1, start_num:int=0, choose_until_correct:bool=True) -> list:
    """Prompt the user to choose one or more values from a list.
    
    Parameters:
    - `_array` (Any): The list of values to choose from.
    - `header_text` (str): The text to display as a header.
    - `header_nl` (bool): Whether to append a newline character after the header.
    - `input_text` (str): The text to prompt the user with.
    - `choose_total` (int): The number of values to choose. 
    - `start_num` (int): The number to start the indexing from.
    - `choose_until_correct` (bool): Whether to keep prompting the user until a correct input is given.
    
    Returns:
    - `list`: A list of the chosen values.
    """

    if not header_text:
        if choose_total == 1:
            header_text = '---Choose 1 value---'
        else:
            header_text = f'---Choose {choose_total} values---'

    fprint(header_text, nl=header_nl)

    for indx, val in enumerate(_array):
        print(f'({indx+start_num}) {val}')
    print()

    while True:
        inpt_indx = finput(input_text, ret_type=str)
        try:
            inpt_indx = tuple(int(x) for x in inpt_indx.split())

            if any({x<start_num for x in inpt_indx}):
                raise IndexError

            return [_array[x - start_num] for x in inpt_indx]

        except IndexError:
            print('Given index is out of range')
            fprint(f'Value has to be between: {start_num}-{start_num+len(_array)-1}')
        except:
            fprint(f'Input not a valid index: {inpt_indx}')

        if not choose_until_correct:
            return []




def chunker(seq, size:int) -> Any:
    """Split a sequence into chunks of the specified size.
    
    Parameters:
    - `seq` (Any): The sequence to split. Can be a list, tuple, or any other iterable object.
    - `size` (int): The size of the chunks.
    
    Returns:
    - `Any`: A list of chunks of the specified size.
    """

    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def flatten_list(lst:list[Any]) -> Any:
    return [item for sublist in lst for item in sublist]