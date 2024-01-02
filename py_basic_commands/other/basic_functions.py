from py_basic_commands.file_dir_scripts.get_src_path    import get_src_path
from py_basic_commands.file_dir_scripts.create_dirs     import create_dirs
from py_basic_commands.file_dir_scripts.join_path       import join_path
from py_basic_commands.fscripts                         import Fprint
from traceback      import format_exc
from functools      import wraps
from shutil     import move
from typing     import Any, Optional
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


def try_listdir(path:Optional[str]=None, return_with_path:bool=False) -> list[str]:
    """Try to list the contents of the given directory.
    
    Parameters
    ----------
    path : str
        The path to list the contents of
    return_with_path : bool, optional
        Whether to return the contents with the path, by default False

    Returns
    -------
    list[str]
        The contents of the directory, or an empty list if the directory does not exist or the file cannot be read
    """
    try:
        if path == '':
            path = None
        content_lst = listdir(path)

        if return_with_path:
            return [join_path(path if path else '', content) for content in content_lst]
        return content_lst

    except FileNotFoundError:
        return []
    
    except NotADirectoryError:
        return []
    

def try_moving(src_file_path:str, dst_dir_path:str, do_print=False) -> bool:
    """Try to move a file
    
    Parameters
    ----------
    src : str
        Source file path
    dst : str
        Destination direcotory path
    
    Returns
    -------
    bool
        True if the file was moved, False if not
    """
    fprint.config(do_print=do_print)

    src_dir_path, src_file_name = get_src_path(src_file_path)

    if src_dir_path == dst_dir_path:
        fprint(f'File ({src_file_name!r}) already in {dst_dir_path!r}')
        return False
    
    dst_file_path = join_path(dst_dir_path, src_file_name)

    create_dirs(dst_dir_path, do_print=do_print) # Just in case

    try:
        move(src_file_path, dst_file_path)
        fprint(f'Moved {src_file_name!r} to {dst_dir_path!r}')
        return True
    
    except FileNotFoundError:
        fprint(f'File not found: {src_file_path!r}')
    except PermissionError:
        fprint(f'Permission error: {src_file_path!r}')
    except Exception as e:
        fprint(format_exc())

    return False


# TODO: Make a function that moves a directory to a dst directory. Add an option to delete the src directory after moving it.