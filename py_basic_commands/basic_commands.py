import traceback, json

from functools  import wraps
from shutil     import rmtree
from typing     import Any, Optional
from time   import perf_counter
from os     import mkdir, listdir, remove

def try_traceback(skip_traceback=False):
    """Wraps a `try except` for the whole function
    
    Parameters:
        `skip_traceback`: Doesn't print the traceback
        
    Return:
        `func(*args, **kwargs)`: Returns whatever the given function should return
        
        `None`: If `except` is raised"""

    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if not skip_traceback:
                    fprint(traceback.format_exc())
                return None
        return wrapper
    return try_except


def func_timer(ret_time=False, do_print=True):
    """Times the excecution time of a function.
    
    Parameters:
        `ret_time`: If time delta should be returned
        
        `do_print`: Print time delta
        
    Return:
        `ret_val`: Default return values from the given fucntion
        
        `time_delta`: Time delta of function excecution time"""

    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fprint('Function timer started', do_print=do_print)
            time_start = perf_counter()
            ret_val = func(*args, **kwargs)
            time_delta = perf_counter() - time_start
            fprint(f'Function {func.__name__}{args} {kwargs} Took {time_delta:.4f} seconds to run', do_print=do_print)
            if ret_time:
                return ret_val, time_delta
            return ret_val
        return wrapper
    return timer


def fprint(*args:Any, nl:bool=True, flush:bool=False, do_print:bool=True, end:Optional[str]=None) -> None:
    """Custom print function.
    
    Parameters:
        `*args`: Values to be printed
        
        `nl`: If a new line should be included at the end a the print
        
        `flush`: Add flush to print
        
        `do_print`: Should values be printed
        
        `end`: Same as the `end` in the default print funciton"""

    if do_print:
        if not args:
            print('')

        for arg in args:
            if nl:
                arg = f'{arg}\n'

            print(arg, end=end, flush=flush)


def finput(text:str='', nl:bool=True, use_suffix:bool=True, ret_type:type=str):
    """Custom input function.
    
    Parameters:
        `text`: Text to be shown
        
        `nl`: If a newline should be printed after the input
        
        `use_suffix`: if `': '` should be added at the end of the input text
        
        `ret_type`: Type the input variable should be returned as
        
    Return:
        `ret_type(inpt)`: Input value changed to the desired type
        
        `inpt`: Input value returned as a string if it can't be changed to the desired type"""

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
    """Wait for user input to continue.
    
    Parameters:
        `text`: Text to show
        
        `nl`: If a new line should be printed afetr the input
        
        `use_suffix`: If a suffix should be used
        
    Return:
        `not any(inpt)`: `True` if input was left empty, `False` if not"""

    if text and use_suffix:
        text = f'{text} (press enter to continue) '

    elif not text and use_suffix:
        text = 'Press enter to continue... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def choose_from_list(_array:Any, header_text:str='', header_nl:bool=False, input_text:str='Input index: ', choose_total:int=1, start_num:int=0, choose_until_correct:bool=True) -> list:
    """Choose one or more values from a list.

    - Parameters:
        - `_array`: An array to choose item(s) from        
        - `header_text`: String to use before the array is printed
        - `header_nl`: If a new line is printed after the header
        - `input_text`: Text displayed in the input function
        - `choose_total`: Total amount of values to choose
        - `start_num`: What number the list index should start at
        - `choose_until_correct`: Only continue after a valid value is chosen from the given array
    - Return:
        - A list of variables that've been chosen. A list is returned even when only one value is requested."""

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


def read_file(file_path, create:bool=False, ret_did_create:bool=False, splitlines:bool=True, remove_empty:bool=True, strip:bool=True, encoding:str='utf-8', do_print:bool=True) -> Any:
    """Read a file and return the read content.
    
    - Parameters:
        - `file_path`: Path to the file that is going to be read
        - `create`: Creates the file if not found
        - `ret_did_create`: Return value if file was created or not
        - `splitlines`: Converts the read file string to a list of lines
            - `remove_empty`: Remove empty lines from the read file list
            - `strip`: If the individual lines in the list should be stripped
        - `encoding`: What encoding should be used when reading the file
        - `do_print`: Print status messages
    - Return:
        - The read file is returned as a list or a string, depending on the given parameters."""

    def try_reading(did_create:bool=False):
        lines: list[str] | str = []
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.read()
            if splitlines:
                lines = lines.splitlines()
                if remove_empty:
                    lines = [x for x in lines if x != '']
                if strip:
                    lines = [x.strip() for x in lines]
            return lines, did_create
        except FileNotFoundError:
            fprint(f'File not found: {file_path}')
            if create:
                create_file_dir('f', file_path, force=True, do_print=do_print)
                return try_reading(True)
        return lines, did_create

    lines,did_create = try_reading()

    if ret_did_create:
        return lines,did_create
    return lines


def write_file(text:Any, file_path:str, append:bool=False, create:bool=True, encoding:str='utf-8', do_print:bool=True) -> bool:
    """Write content to a file.
    
    - Parameters:
        - `text`: Text to write or append in the file        
        - `file_path`: Path to the file        
        - `append`: If the text should be appended, instead of writing on top of the file        
        - `create`: Create file, if not found:        
        - `encoding`: Encoding used for writing:
        - `do_print`: Print status messages
    - Return:
        - `did_create`: If a file was created or not"""

    if text.__class__.__name__ == 'ndarray':
        text = text.tolist()
    
    if text.__class__.__name__ in ('list', 'tuple', 'set'):
        text = '\n'.join(text)

    lines, did_create = read_file(file_path, create:=create, ret_did_create=True, remove_empty=False, splitlines=False, do_print=do_print)

    try:
        if not did_create and lines[-1] != '\n':
            text = '\n' + text 
    except IndexError:
        pass
    except Exception:
        print(traceback.format_exc())

    if append:
        mode = 'a'
    else:
        mode = 'w'

    with open(file_path, mode=mode, encoding=encoding) as f:
        f.write(text + '\n')

    return did_create


def create_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Create a file or a directory to given path.
    
    - Parameters:
        - `do`: `'d'` - Create a directory, `'f'` - Create a file
        - `do_path`: Path to the new file/directory
        - `force`: Even if an excisting file/directory is found, create a new one
        - `do_print`: Print status messages
        
    - Return:
        - `did_create`: If the file/directory was created"""

    def create_dir():
        try:
            mkdir(do_path)
            fprint(f'Directory created: {do_path}', do_print=do_print)
            return True
        except FileExistsError:
            fprint(f'Directory aleady exists: {do_path}', nl=not force, do_print=do_print)
            if force:
                rmtree(do_path)
                fprint(f'Directory removed: {do_path}', nl=False, do_print=do_print)
                return create_dir()

    if do == 'd': # Directory
        return create_dir()
    
    elif do == 'f': # File
        file_dir, filename = get_dir_path_for_file(do_path)
        files_in_path = listdir(file_dir)

        if force or filename not in files_in_path:
            try:
                open(do_path, 'w', encoding='utf-8').close()
                fprint(f'File created: {do_path}', do_print=do_print)
                return True
            except FileExistsError:
                fprint(f'File already exists: {do_path}', do_print=do_print)
                return False
        elif filename in files_in_path:
            fprint(f'File already exists: {do_path}', do_print=do_print)
            return False


@try_traceback(skip_traceback=True)
def remove_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> None:
    """Removes file or directory for given path.
    
    - Parameters:
        - `do`: `'f'` - Removes a file, `'d'` - Removes a directory    
        - `do_path`: Path to the file/directory    
        - `force`: Removes file/directory even when content is found inside    
        - `do_print`: Should info get printed"""

    if do == 'd': # Directory
        try:
            dir_content = listdir(do_path)
        except FileNotFoundError:
            fprint(f'Directory path not found: {do_path}', do_print=do_print)

        if not dir_content or force:
            rmtree(do_path)
            fprint(f'Directory removed: {do_path}', do_print=do_print)
            
        elif dir_content:
            fprint(f'Directory is not empty, not removing: {do_path}', do_print=do_print)

    elif do == 'f': # File
        lines = read_file(do_path)
        if lines and not force:
            fprint(f'File is not empty, not removing: {do_path}', do_print=do_print)
            return
        remove(do_path)
        fprint(f'File removed: {do_path}', do_print=do_print)


def get_dir_path_for_file(file_path:str, ret_val='a') -> Any:
    """Get the directory path for given file path.
    
    - Parameters:
        - `ret_val`:
            - `'a'` - Return both `'d'` and `'fnam'`
            - `'d' `- Returns only the directory path
            - `'fnam'` - Returns only the filename"""
    dir_path = file_path.replace('\\', '/').split('/')
    if len(dir_path) == 1:
        dir_path = None
        filename = file_path
    else:
        filename = dir_path.pop()
        dir_path = '/'.join(dir_path)

    if ret_val == 'd': # Directory
        return dir_path
    elif ret_val == 'fnam': # Filename
        return filename

    return dir_path, filename


def join_path(*args, join_with='/'):
    """Join a list of paths with a specified separator.
    
    - Parameters:
        - args (str): A list of paths to join.
        - join_with (str): The separator to use when joining the paths. Default is '/'.
    
    - Returns:
        - str: The joined path."""

    return join_with.join(args)


def chunker(seq, size:int) -> Any:
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def create_json(filepath:str, force:bool=False, do_print:bool=True) -> bool:
    did_create = create_file_dir('f', filepath, force=force, do_print=do_print)
    if did_create:
        open(filepath, 'w').write(json.dumps({}, indent=4))
    return did_create


def read_json(filepath:str) -> Any:
    try:
        with open(filepath, 'r') as f:
            file_data = json.load(f)
        return file_data
    except FileNotFoundError:
        fprint(f'File not found: {filepath}')
    except json.decoder.JSONDecodeError:
        fprint(f'File cannot be read as a JSON: {filepath}')
    except Exception:
        fprint(traceback.format_exc())


def write_json(data:Any, filepath:str, indent:int=4, force:bool=False, do_print:bool=True):
    try:
        if data.__class__.__name__ == ('str'):
            data = json.loads(data)

        d = read_json(filepath)
        
        if d and not force:
            fprint(f'Data found in JSON file, not writing new data: {filepath}', do_print=do_print)
            return

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)

        fprint(f'Wrote data to JSON file: {filepath}', do_print=do_print)
    except TypeError:
        fprint(f'Data type is wrong, can\'t write to JSON: {data.__class__.__name__}', do_print=do_print)
    except Exception:
        fprint(traceback.format_exc())
