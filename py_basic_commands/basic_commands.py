import traceback

from functools  import wraps
from shutil     import rmtree
from time   import time
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
            time_start = time()
            ret_val = func(*args, **kwargs)
            time_delta = time() - time_start
            fprint(f'Function {func.__name__}{args} {kwargs} Took {time_delta:.4f} seconds to run', do_print=do_print)
            if ret_time:
                return ret_val, time_delta
            return ret_val
        return wrapper
    return timer


def fprint(text=None, nl=True, flush=False, do_print=True):
    if not text:
        text = ''

    if nl:
        text = f'{text}\n'

    if do_print:
        print(text, flush=flush)


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


def enter_to_continue(text='', nl=True, use_help_text=True):
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


def read_file(file_path, create=False, force=False, remove_empty=True, do_print=True):
    def try_read():
        try:
            return open(file_path, 'r', encoding='utf-8').read().splitlines()
        except FileNotFoundError:
            if create:
                create_file_dir('file', file_path, force)
                return try_read()
            else:
                fprint(f'File not found: {file_path}', do_print=do_print)
    lines = try_read()
    if remove_empty and lines:
        return [x for x in lines if x != '']
    return lines


def create_file_dir(do, do_path, force=False, do_print=True):
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

    if do == 'dir':
        create_dir()
    
    elif do == 'file':
        file_dir, filename = get_dir_path_for_file(do_path) #type:ignore
        files_in_path = listdir(file_dir)

        if force or filename not in files_in_path:
            try:
                open(do_path, 'w', encoding='utf-8').close()
                fprint(f'File created: {do_path}', do_print=do_print)
            except FileExistsError:
                fprint(f'File already exists: {do_path}', do_print=do_print)
        elif filename in files_in_path:
            fprint(f'File already exists: {do_path}', do_print=do_print)


@try_traceback(skip_traceback=True)
def remove_file_dir(do, do_path, force=False, do_print=True):
    if do == 'dir':
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

    elif do == 'file':
        lines = read_file(do_path)
        if lines and not force:
            fprint(f'File is not empty, not removing: {do_path}', do_print=do_print)
            return
        remove(do_path)
        fprint(f'File removed: {do_path}', do_print=do_print)


def get_dir_path_for_file(file_path, ret_val='all'):
    dir_path = file_path.replace('\\', '/').split('/')
    if len(dir_path) == 1:
        dir_path = None
        filename = file_path
    else:
        filename = dir_path.pop()
        dir_path = '/'.join(dir_path)

    if ret_val == 'dir':
        return dir_path
    elif ret_val == 'filename':
        return filename

    return dir_path, filename


def join_path(*args, join_with='\\'):
    return join_with.join(args)