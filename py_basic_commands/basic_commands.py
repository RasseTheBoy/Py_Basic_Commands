def fprint(text='', nl=True, flush=False):
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

def better_input(text='', nl=True, use_end_addon=True, ret_type: type = str):
    if use_end_addon:
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