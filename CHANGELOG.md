# Changelog

## [0.0.3] - 2022-12-08

### Added

- `better_input()` to `__init__.py`

## [0.0.2] - 2022-12-08

### Added

- New function created -> `better_input()`
- A new variable (`flush`) was added to`fprint()`
- New`CHANGELOG.md` added to the project

#### New function created -> `better_input()`

Customize your input as you wish!

```
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
        print('Returning value as string')
        return inpt
```

Function variable table:

| Variable name     | What it does                      | Type |
| -------------     |:-------------:                    |:-------------:|
| text              | Text to use in `input`            | String
| nl                | Add newline after `input`         | Bool
| use_end_addon     | Add `: ` at the end of to `text` variable    | Bool
| ret_type          | Returns value as given type       | Type


#### A new variable (`flush`) was added to`fprint()`

<pre>
def fprint(text='', nl=True, <b>flush=False</b>):
    if nl:
        text = f'{text}\n'
    print(text, <b>flush=flush</b>)
</pre>

`flush` has a default value (`False`), so this can be left empty

#### New`CHANGELOG.md` added to the project


A `CHANGELOG.md` file is added to the project and it will get updated with every new version.

### TODO

- Edit `README.md`

### Edit `README.md`

The `README.md` should include a guide and examples of the new function (`better_input()`).


## [0.0.1] - 2022-12-03

### Added

Files created and added to [GitHub](https://github.com/RasseTheBoy/Py_Basic_Tools) and [PyPi](https://pypi.org/project/py-basic-commands/).