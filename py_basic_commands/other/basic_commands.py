from traceback  import format_exc
from functools  import wraps
from py_basic_commands.fscripts     import Fprint
from typing     import Any
from os     import listdir 

fprint = Fprint()

def try_traceback(print_traceback=False):
    """Decorator to catch and handle exceptions raised by a function.
    
    Parameters
    ----------
    print_traceback : bool, optional
        Whether to print the traceback if an exception is raised, by default False
    
    Returns
    -------
    function
        The decorated function
    """
    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                fprint(format_exc(), do_print=print_traceback)
        return wrapper
    return try_except


def enter_to_continue(text:str='', nl:bool=True, use_suffix:bool=True) -> bool:
    """Prompt the user to press the enter key to continue.
    
    Parameters
    ----------
    text : str, optional
        The text to display, by default ''
    nl : bool, optional
        Whether to print a newline after the text, by default True
    use_suffix : bool, optional
        Whether to use the default suffix, by default True

    Returns
    -------
    bool
        Whether the user pressed the enter key
    """
    if text and use_suffix:
        text = f'{text} (press enter to continue or type anything to break) '

    elif not text and use_suffix:
        text = 'Press enter to continue or type anything to break... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def chunker(seq, size:int) -> list[Any]:
    """Split a sequence into chunks of the specified size.
    
    Parameters
    ----------
    seq : Any
        The sequence to split
    size : int
        The size of each chunk
    
    Returns
    -------
    Any
        The sequence split into chunks of the specified size
    """
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def flatten_list(lst:list[Any]) -> Any:
    """Flatten a list of lists.
    
    Parameters
    ----------
    lst : list[Any]
        The list to flatten
        
    Returns
    -------
    Any
        The flattened list"""
    return [item for sublist in lst for item in sublist]


def try_listdir(path:str) -> list[str]:
    """Try to list the contents of the given directory.
    
    Parameters
    ----------
    path : str
        The path to list the contents of

    Returns
    -------
    list[str]
        The contents of the directory, or an empty list if the directory does not exist or the file cannot be read
    """
    try:
        return listdir(path)
    except FileNotFoundError:
        return []