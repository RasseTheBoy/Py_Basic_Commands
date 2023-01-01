import traceback, json

from functools  import wraps
from colored    import fg, attr
from shutil     import rmtree
from typing     import Any
from time   import perf_counter
from os     import mkdir, listdir, remove

def try_traceback(skip_traceback=False):
    def try_except(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if not skip_traceback:
                    print(traceback.format_exc())
                return traceback.format_exc()
        return wrapper
    return try_except


def func_timer(ret_time=False, do_print=True):
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


def fprint(text=None, nl=True, flush=False, do_print=True, end='') -> None:
    if not text:
        text = ''

    if nl:
        text = f'{text}\n'

    if do_print:
        if not end:
            print(text, flush=flush)
        else:
            print(text, end=end, flush=flush)


def finput(text='', nl=True, use_end_addon=True, ret_type: type = str):
    if not text:
        text = 'Input: '
    elif use_end_addon and text.rstrip()[-1] != ':':
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


def enter_to_continue(text='', nl=True, use_help_text=True) -> bool:
    if text and use_help_text:
        text = f'{text} (press enter to continue) '

    elif not text and use_help_text:
        text = 'Press enter to continue... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def choose_from_list(lst, header_text='', header_nl=False, input_text='Input index: ', choose_total=1, start_num=0, choose_until_correct=True) -> list:
    if not header_text:
        if choose_total == 1:
            header_text = '---Choose 1 value---'
        else:
            header_text = f'---Choose {choose_total} values---'

    fprint(header_text, nl=header_nl)

    for indx, val in enumerate(lst):
        print(f'({indx+start_num}) {val}')
    print()

    while True:
        inpt_indx = finput(input_text, ret_type=str)
        try:
            inpt_indx = tuple(int(x) for x in inpt_indx.split())

            if any({x<start_num for x in inpt_indx}):
                raise IndexError

            return [lst[x - start_num] for x in inpt_indx]

        except IndexError:
            print('Given index is out of range')
            fprint(f'Value has to be between: {start_num}-{start_num+len(lst)-1}')
        except:
            fprint(f'Input not a valid index: {inpt_indx}')

        if not choose_until_correct:
            return []


def read_file(file_path, create:bool=False, ret_did_create:bool=False, remove_empty:bool=True, splitlines:bool=True, do_print:bool=True, encoding:str='utf-8', strip:bool=True) -> Any:
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
    def create_dir():
        try:
            mkdir(do_path)
            fprint(f'Directory created: {do_path}', do_print=do_print)
            return True
        except FileExistsError:
            fprint(f'Directory aleady exists: {do_path}', nl=False, do_print=do_print)
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
def remove_file_dir(do, do_path, force=False, do_print=True):
    if do == 'd': # Directory
        try:
            dir_content = listdir(do_path)
        except FileNotFoundError:
            fprint(f'Directory path not found: {do_path}', do_print=do_print)
            return traceback.format_exc()

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


def get_dir_path_for_file(file_path, ret_val='a') -> Any:
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


def fd(variable, nl=False) -> None:
    reset = attr('reset')
    filename, lineno, function_name, code = traceback.extract_stack()[-2]
    original_var = code.replace('fd(', '').replace(')', '', 1)
    if code.replace(original_var, '') != 'fd()':
        original_var = code

    variable_type = type(variable).__name__

    if variable == True:
        variable = fg("green") + str(variable) + reset
    elif variable == False:
        variable = fg("red") + str(variable) + reset
    elif isinstance(variable, int):
        variable = fg("blue") + str(variable) + reset
    else:
        variable = f'{variable!r}'

    fprint(f'fd | {variable_type} | {original_var}: {variable}', nl=nl)


def join_path(*args, join_with='\\'):
    return join_with.join(args)


def chunker(seq, size:int):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


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