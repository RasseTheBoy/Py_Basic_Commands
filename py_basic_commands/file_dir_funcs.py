
from basic_commands  import try_traceback
from traceback      import format_exc
from fscripts     import fprint
from shutil     import rmtree
from typing     import Any
from os     import mkdir, listdir, makedirs, remove


def read_file(file_path, create:bool=False, ret_did_create:bool=False, splitlines:bool=True, remove_empty:bool=True, do_strip:bool=True, do_lower:bool=False, encoding:str='utf-8', do_print:bool=True) -> Any:
    """Read the contents of a file.
    
    Parameters:
    - `file_path` (str): The path to the file to read.
    - `create` (bool): Whether to create the file if it does not exist.
    - `ret_did_create` (bool): Whether to return a tuple of the file contents and a bool indicating whether the file was created.
    - `splitlines` (bool): Whether to split the file contents into a list of lines.
    - `remove_empty` (bool): Whether to remove empty lines when `splitlines` is True.
    - `strip` (bool): Whether to strip leading and trailing whitespace from each line when `splitlines` is True.
    - `encoding` (str): The encoding to use when reading the file.
    - `do_print` (bool): Whether to print information about the file reading process.
    
    Returns:
    - `Any`: If `ret_did_create` is True, a tuple containing the file contents and a bool indicating whether the file was created. Otherwise, the file contents.
    """
    
    def try_reading(did_create:bool=False):
        lines: list[str] | str = []
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.read()
            if splitlines:
                lines = lines.splitlines()
                if remove_empty:
                    lines = [x for x in lines if x != '']
                if do_strip:
                    lines = [x.strip() for x in lines]
                if do_lower:
                    lines = [x.lower() for x in lines]
            return lines, did_create
        except FileNotFoundError:
            fprint(f'File not found: {file_path}', do_print=do_print)
            if create:
                create_file_dir('f', file_path, force=True, do_print=do_print)
                return try_reading(True)
        return lines, did_create

    lines, did_create = try_reading()

    if ret_did_create:
        return lines, did_create
    return lines


def write_file(text:Any, file_path:str, append:bool=False, force_create:bool=True, remove_duplicates:bool=False, encoding:str='utf-8', do_print:bool=True) -> bool:
    """Write text to a file.
    
    Parameters:
    - `text` (Any): The text to write. Can be a string, list, tuple, set or a numpy.array.
    - `file_path` (str): The path to the file to write to.
    - `append` (bool): Whether to append the text to the end of the file.
    - `force_create` (bool): Whether to create the file if it does not exist.
    - `remove_duplicates` (bool): Whether to remove duplicates from a list, tuple or set
    - `encoding` (str): The encoding to use when writing the file.
    - `do_print` (bool): Whether to print information about the file writing process.
    
    Returns:
    - `bool`: Whether the file was created.
    """

    if text.__class__.__name__ == 'ndarray':
        text = text.tolist()
    
    if text.__class__.__name__ in ('list', 'tuple', 'set'):
        if remove_duplicates:
            text = list(dict.fromkeys(text))
        text = '\n'.join(text)

    lines, did_create = read_file(file_path, create=force_create, ret_did_create=True, remove_empty=False, splitlines=False, do_print=do_print)

    if len(lines.strip()) > 0 and not force_create and not append:
        fprint('Not writing to file. File has content; and foce_create is set to False', do_print=do_print)
        return did_create

    try:
        if not did_create and lines[-1] != '\n':
            text = '\n' + text 
    except IndexError:
        pass
    except Exception:
        fprint(format_exc(), do_print=do_print)

    if append:
        mode = 'a'
    else:
        mode = 'w'

    with open(file_path, mode=mode, encoding=encoding) as f:
        f.write(text + '\n')
        fprint(f'Content written to file: {file_path}', do_print=do_print)

    return did_create


def create_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Create a file or directory at the specified path.
    
    Parameters:
    - `do` (str): Whether to create a `'d'`irectory or a `'f'`ile.
    - `do_path` (str): The path to create the file or directory at.
    - `force` (bool): Whether to force the creation of the file or directory by deleting any existing file or directory with the same name.
    - `do_print` (bool): Whether to print information about the file or directory creation process.
    
    Returns:
    - `bool`: Whether the file or directory was created.
    """

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

    match do:
        case 'd': # Directory
            return create_dir()

        case 'f': # File
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


def create_dirs(dst_path:str, do_print:bool=True) -> bool:
    """Create all required directories for the given path.
    
    Parameters:
    - `dst_path` (str): Destination path; can include the file name at the end
    
    Returns:
    - `bool`: If all directories were created or not"""

    if dst_path == '':
        return False

    _dst_path = get_dir_path_for_file(dst_path, ret_val='d', do_print=do_print)

    try:
        makedirs(_dst_path)
        fprint(f'Destination created for path: {_dst_path}', do_print=do_print)
        return True

    except FileExistsError:
        fprint(f'Path already exists: {_dst_path}', do_print=do_print)

    except Exception:
        fprint(format_exc(), do_print=do_print)
    
    return False


@try_traceback(print_traceback=True)
def remove_file_dir(do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Remove a file or directory at the specified path.
    
    Parameters:
    - `do` (str): Whether to remove a `'d'`irectory or a `'f'`ile.
    - `do_path` (str): The path to the file or directory to remove.
    - `force` (bool): Whether to force the removal of the file or directory.
    - `do_print` (bool): Whether to print information about the file or directory removal process.
    
    Returns:
    - `bool`: Whether the file or directory was removed.
    """

    if do == 'd': # Directory
        try:
            dir_content = listdir(do_path)
        except FileNotFoundError:
            fprint(f'Directory path not found: {do_path}', do_print=do_print)
            return False

        if not dir_content or force:
            rmtree(do_path)
            fprint(f'Directory removed: {do_path}', do_print=do_print)
            return True
            
        elif dir_content:
            fprint(f'Directory is not empty, not removing: {do_path}', do_print=do_print)
            return False
        
        else:
            return False

    elif do == 'f': # File
        lines = read_file(do_path, do_print=do_print)
        if lines and not force:
            fprint(f'File is not empty, not removing: {do_path}', do_print=do_print)
            return False
        remove(do_path)
        fprint(f'File removed: {do_path}', do_print=do_print)
        return True


def get_dir_path_for_file(file_path:str, ret_val='a') -> Any:
    """Get the directory path and filename for a file.
    
    Parameters:
    - `file_path` (str): The path to the file.
    - `ret_val` (str): Whether to return the `'d'`irectory path, `'fnam'`e of the file, or `'a'`ll (default).
    
    Returns:
    - `Any`: If `ret_val` is `'d'`, the directory path. If `ret_val` is `'fnam'`, the filename. Otherwise, a tuple containing the directory path and the filename.
    """

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


def join_path(*args:str, join_with='/', remove_empty:bool=True, dir_end:bool=False, do_print:bool=False) -> str:
    r"""Join path segments together, removing certain characters (`<>:"/\|?*`) and adjust for correct slash direction.

    Parameters:
    - `*args`: One or more path segments to join
    - `join_with`: The separator to use when joining the path segments
    - `dir_end`: Specify whether to add join_with character at the end of the returned path

    Return:
    A `string` representing the joined path
    """
    
    def split_join(var:str, split_with:str=' '):
        return join_with.join(var.split(split_with))

    new_args = []
    for arg_indx, arg in enumerate(args):
        arg = split_join(split_join(arg, '\\'), '/')
        arg = arg.translate({ord(c): None for c in '<>:"|?*'})

        split_arg = arg.split('/')
        if '' in split_arg and remove_empty:
            fprint(f'Empty string found in input arg (indx: {arg_indx}): {arg!r}', do_print=do_print)
            split_arg = [x for x in split_arg if x != '']
            arg = join_with.join(split_arg)
            if arg == '':
                continue

        new_args.append(arg)

    out_path = join_with.join(new_args)

    if dir_end:
        out_path += join_with

    return out_path

