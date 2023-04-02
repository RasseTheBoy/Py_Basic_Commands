import json

from basic_commands     import create_file_dir, read_file
from traceback  import format_exc
from fscripts     import fprint
from typing     import Any


def create_json(file_path:str, force:bool=False, do_print:bool=True) -> bool:
    """Create a new empty JSON file.
    
    Parameters:
    - `file_path` (str): The path for the new JSON file.
    - `force` (bool): Whether to overwrite any existing file with the same name.
    - `do_print` (bool): Whether to print information about the file creation process.
    
    Returns:
    - `bool`: Whether the file was created.
    """
    write_empty_json = lambda: open(file_path, 'w').write(json.dumps({}, indent=4))

    did_create = create_file_dir('f', file_path, force=force, do_print=do_print)
    if did_create:
        write_empty_json()
        fprint(f'New JSON created: {file_path}', do_print=do_print)
    elif read_json(file_path, do_print=do_print) == None:
        text = read_file(file_path, splitlines=False)
        if text and not force:
            fprint(f'Cannot create new JSON file. Text found in file; and force set as False: {file_path}', do_print=do_print)
            return did_create
        write_empty_json()
        fprint(f'Basic brackets added to JSON: {file_path}', do_print=do_print)
    
    return did_create


def read_json(file_path:str, do_print:bool=True) -> Any:
    """Read data from a JSON file.
    
    Parameters:
    - `file_path` (str): The path of the JSON file to read from.
    - `do_print` (bool): Whether to get feedback printed to terminal or not
    
    Returns:
    - `Any`: The data from the JSON file, as a dictionary or list.
    """

    try:
        with open(file_path, 'r') as f:
            file_data = json.load(f)
        return file_data
    except FileNotFoundError:
        fprint(f'File not found: {file_path}', do_print=do_print)
    except json.decoder.JSONDecodeError:
        fprint(f'File cannot be read as a JSON: {file_path}', do_print=do_print)
    except Exception:
        fprint(format_exc(), do_print=do_print)


def write_json(data:Any, file_path:str, indent:int=4, force:bool=False, do_print:bool=True):
    """Write data to a JSON file.
    
    Parameters:
    - `data` (Any): The data to write to the JSON file. This can be a dictionary, list, or a string representation of JSON.
    - `file_path` (str): The path of the JSON file to write to.
    - `indent` (int): The number of spaces to use for indentation in the JSON file.
    - `force` (bool): Whether to overwrite any existing data in the JSON file.
    - `do_print` (bool): Whether to print information about the data writing process.

    Return:
    - `bool`: Whether the file was created.
    """

    try:
        if data.__class__.__name__ == ('str'):
            data = json.loads(data)

        d = read_json(file_path)
        
        if d and not force:
            fprint(f'Data found in JSON file, not writing new data: {file_path}', do_print=do_print)
            return False

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)

        fprint(f'Wrote data to JSON file: {file_path}', do_print=do_print)
        return True
    except TypeError:
        fprint(f'Data type is wrong, can\'t write to JSON: {data.__class__.__name__}', do_print=do_print)
    except Exception:
        fprint(format_exc())
    return False