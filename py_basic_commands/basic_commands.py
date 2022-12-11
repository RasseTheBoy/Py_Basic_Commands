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
        return wrapper
    return try_except


def func_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        fprint('Function timer started')
        time_start = time()
        ret_val = func(*args, **kwargs)
        time_delta = time() - time_start
        fprint(f'Function {func.__name__}{args} {kwargs} Took {time_delta:.4f} seconds to run')
        return ret_val
    return wrapper


def fprint(text=None, nl=True, flush=False, do_print=True):
    if not text:
        text = ''

    if nl:
        text = f'{text}\n'

    if do_print:
        print(text, flush=flush)


def enter_to_continue(text='', nl=True, use_help_text=True):
    if text and use_help_text:
        text = f'{text} (press enter to continue) '

    elif not text and use_help_text:
        text = 'Press enter to continue... '
    
    inpt = input(text)
    
    if nl:
        print()

    return not any(inpt)


def finput(text='', nl=True, use_end_addon=True, ret_type: type = str):
    if use_end_addon and text.rstrip()[-1] != ':':
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


def choose_from_list(lst, header_text='---Choose 1 value---', header_nl=False, input_text='Input index: ', choose_total=1, start_num=0, choose_until_correct=False):
    # TODO: Option to choose more than one
    # TOOD: If choose_amnt > 2, show input(f'{chosen_amnt}/{choose_total} {text}')

    fprint(header_text, nl=header_nl)
    for indx, val in enumerate(lst):
        print(f'({indx+start_num}) {val}')
    print()

    while True:
        inpt_indx = finput(input_text, ret_type=int)
        try:
            return lst[inpt_indx - start_num] # type: ignore
        except IndexError:
            print('Given index is out of range')
            fprint(f'List length: {len(lst)}    Input index: {inpt_indx}')
        except:
            fprint(f'Input not a valid index: {inpt_indx}')

        if not choose_until_correct:
            return


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
        file_dir, filename = get_path_for_file(do_path) #type:ignore
        files_in_path = listdir(file_dir)

        if force or filename not in files_in_path:
            try:
                open(do_path, 'w', encoding='utf-8').close()
                fprint(f'File created: {do_path}', do_print=do_print)
            except FileExistsError:
                fprint(f'File already exists: {do_path}', do_print=do_print)
        elif filename in files_in_path:
            fprint(f'File already exists: {do_path}', do_print=do_print)


@try_traceback()
def remove_file_dir(do, do_path, force=False, do_print=True):
    if do == 'dir':
        dir_content = listdir(do_path)
        if force:
            rmtree(do_path)
            fprint(f'Directory removed: {do_path}', do_print=do_print)
        elif dir_content:
            fprint(f'Directory is not empty, not removing: {do_path}', do_print=do_print)

    elif do == 'file':
        lines = read_file(do_path)
        if lines:
            fprint(f'File is not empty, not removing: {do_path}', do_print=do_print)
            return
        remove(do_path)
        fprint(f'File removed: {do_path}', do_print=do_print)


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


def get_path_for_file(file_path, return_val='all'):
    file_dir = file_path.replace('\\', '/').split('/')
    if len(file_dir) == 1:
        file_dir = None
        filename = file_path
    else:
        filename = file_dir.pop()
        file_dir = '/'.join(file_dir)

    if return_val == 'dir':
        return file_dir
    elif return_val == 'filename':
        return filename

    return file_dir, filename


def join_dir(*args, join_with='\\'):
    return join_with.join(args)