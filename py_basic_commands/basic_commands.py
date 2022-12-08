import traceback
from functools  import wraps

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


def fprint(text=None, nl=True, flush=False):
    if not text:
        text = ''

    if nl:
        text = f'{text}\n'

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


def choose_from_list(lst, header_text='---Choose 1 value---', header_nl=False, input_text='Input index: ', choose_total=1, start_num=0):
    # TODO: Option to choose more than one
    # TOOD: If choose_amnt > 2, show input(f'{chosen_amnt}/{choose_total} {text}')

    fprint(header_text, nl=header_nl)
    for indx, val in enumerate(lst):
        print(f'({indx+start_num}) {val}')
    print()

    inpt_indx = finput(input_text, ret_type=int)

    try:
        return lst[inpt_indx - start_num] # type: ignore
    except IndexError:
        print('Given index is out of range')
        print(f'List length: {len(lst)}    Input index: {inpt_indx}')
    except:
        print('Input not valid: {inpt_indx}')

    fprint('Returning nothing!')
    return