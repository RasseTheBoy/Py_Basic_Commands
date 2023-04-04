from traceback  import format_exc
from functools  import wraps
from py_basic_commands.fscripts     import fprint
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
            except Exception:
                if print_traceback:
                    fprint(format_exc())
                return None
        return wrapper
    return try_except


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