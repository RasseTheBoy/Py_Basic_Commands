
Py Basic Commands
==================

<p align="center">
    <img src="https://raw.githubusercontent.com/RasseTheBoy/Py_Basic_Commands/main/Logo/py_basic_commands.png" width=300>
</p>

A package with some basic tools and commands for Python (3.6>)


# Author

- [@RasseTheBoy](https://github.com/RasseTheBoy)

# Installation

Install using pip

```bash
  pip install py_basic_tools

  pip3 install py_baisc_tools
```

# Table of input variables

| Variable | Usage | Type |
| :---: | :---: | :---: |
| text | The text to be printed | str |
| nl | Whether to print a newline or not | bool |
| flush | Whether to flush the output print or not | bool |
| do_print | Whether to print the text or not | bool |
| use_end_addon | Whether or not to add a colon to the end of the text | bool |
| file_path | The path of the file to be read | str |
| create | If True, the file/directory will be created if it does not exist | bool |
| force | If True, the file/directory will be created even if it exists | bool |
| remove_empty | If True, empty lines will be removed from list | bool |
| do | Action for directory or file | `'dir'`/`'file'` |
| ret_type | Variable type to return | type |
| ret_var | Variable to return | str |

# Examples

## Links to functions

- [fprint()](#fprint)
- [finput()](#finput)
- [enter_to_continue()](#enter_to_continue)
- [choose_from_list()](#choose_from_list)
- [read_file()](#read_file)
- [create_file_dir()](#create_file_dir)
- [remove_file_dir()](#remove_file_dir)
- [get_dir_path_for_file()](#get_dir_path_for_file)
- [join_path()](#join_path)
- [try_traceback()](#try_traceback)
- [func_timer()](#func_timer)


## fprint()

- Customizable input function

```python
>>> fprint('Hello World')
Hello World

>>> fprint('Hello World', nl=False)
Hello World
>>> fprint()

>>> fprint('Hello World', do_print=False)

```

The above fprint() examples are very basic. But you could implement and customise it to your liking.
## finput()

- Customizable input function

```python
>>> finput('Enter a number', ret_type=int)
Enter a number: 5

5
>>> finput('Enter a number', ret_type=int)
Enter a number: 5.5

Couldn't return input 5.5 as <class 'int'>
Input type: <class 'str'>
Returning value as string

'5.5'
>>> finput('Enter a number', ret_type=int)
Enter a number: five

Couldn't return input five as <class 'int'>
Input type: <class 'str'>
Returning value as string

'five'
```
## enter_to_continue()

- Wait until user presses enter to continue
- Returns:
    - `True`: No input was given, only enter was pressed
    - `False`: Something was written before pressing enter

```py
from py_basic_tools import enter_to_continue

>>> enter_to_continue()
Press enter to continue...

>>> enter_to_continue('Waiting')
Waiting (enter to continue)

>>> enter_to_continue('Waiting', nl=False)
Waiting (enter to continue)
>>> enter_to_continue('Waiting', use_help_text=False)
Waiting

>>> enter_to_continue(use_help_text=False)

```
## choose_from_list()

- Choose one or more variables from user given list
- When choosing more than one, add a space between chosen indexes
- Returns:
    - `list of variables`: If variables were chosen correctly
    - `empty list`: If an `exception` occured

```py
>>> lst = ['foo', 'bar']
>>> choose_from_list(lst)
---Choose 1 value---
(0) foo
(1) bar

Input index: 0
'foo'
>>> choose_from_list(lst, choose_total=2, start_num=1)
---Choose 2 values---
(1) foo
(2) bar

Input index: 1 2
['foo', 'bar']
>>> choose_from_list(lst, start_num=3, choose_until_correct=True)
---Choose 1 value---
(3) foo
(4) bar

Input index: 0

Given index is out of range
List length: 2    Input index: 0

Input index: 3

foo
>>> choose_from_list(lst, choose_total=2, start_num=1, choose_until_correct=False)
---Choose 2 values---
(1) foo
(2) bar

Input index: 0 1
Given index is out of range
Value has to be between: 1-2
[]
>>> choose_from_list(lst, header_text='Choose what you will', header_nl=True, input_text='Input what you will')
Choose what you will

(0) foo
(1) bar

Input what you will: 0

['foo']
```
## read_file()

- Function tries to read the file, and if it fails, it will create the file if the `create` argument is True.
- If the file is read successfully, the function will return a list of lines from the file

```py
>>> read_file('path/to/file.txt')
File not found: path/to/file.txt

None
>>> read_file('path/to/file.txt', do_print=False)
None
>>> read_file('path/to/file.txt', create=True)
File created: path/to/file.txt

>>> read_file('path/to/file.txt')
['hello', 'world', 'foo bar']

>>> read_file('path/to/file.txt', remove_empty_lines=False)
['hello', 'world', '', 'foo bar']
```
## create_file_dir()

- Creates a file or directory to the given path

```py
>>> create_file_dir('file', 'path/to/file.txt')
File created: path/to/file.txt

>>> create_file_dir('file', 'path/to/file.txt')
File already exists: path/to/file.txt

>>> create_file_dir('file', 'path/to/file.txt', do_print=False)

>>> create_file_dir('file', 'path/to/file.txt', force=True)
File created: path/to/file.txt

>>> create_file_dir('dir', 'path/to/new directory')
Directory created: path/to/new directory

```
## remove_file_dir()

- Removes a file or directory to the given path

```py
>>> remove_file_dir('file', 'path/to/file.txt')
File removed: path/to/file.txt

>>> remove_file_dir('file', 'path/to/another_file.txt')
File is not empty, not removing: file.txt

>>> remove_file_dir('file', 'path/to/another_file.txt', force=True)
File removed: path/to/another file.txt

>>> remove_file_dir('file', 'path/to/another_file.txt')
File not found: path/to/another file.txt

>>> remove_file_dir('dir', 'path/to/directory')
Directory path not found: path/to/directory
```
## get_dir_path_for_file()

- Gets the path to the direcotry where given file is
- Returns: 
    - `dir_path`: Paht to the directory
    - `filename`: Name of the file

```py
>>> get_dir_path_for_file('path/to/file.txt')
('path/to', 'file.txt')
>>> get_dir_path_for_file('path/to/file.txt', ret_var='filename')
'file.txt'
>>> get_dir_path_for_file('path/to/file.txt', ret_var='dir')
'path/to'
```
## join_path()

- Joins given paths together
    - Like `os.path.join()`

```py
>>> join_path('hello', 'world')
'hello\\world'
>>> join_path('hello', 'world', join_with='/')
'hello/world'
```
## try_traceback()

Code:
```python
@try_traceback()
def foo():
    raise Exception('foo')

@try_traceback(skip_traceback=True)
def bar():
    raise Exception('bar')

foo()
bar()
```

Output:
```python
Traceback (most recent call last):
    File "test.py", line 13, in wrapper
        return func(*args, **kwargs)
    File "test.py", line 8, in foo
        raise Exception('foo')

```

`bar()` doesn't raise an exception, because traceback was skipped.
## func_timer()

- The decorator can be used to time any function, and it will print the time it took to run the function
- Returns:
    - `ret_val`: Values to return from the function
    - `time_delta`: The time it took for the function to run

Code:
```py
from time import sleep

@func_timer()
def foo(sec_to_sleep):
    sleep(sec_to_sleep)
    return 'Foo is done'

@func_timer(ret_time=True, do_print=False)
def bar(sec_to_sleep):
    sleep(sec_to_sleep)
    return 'bar is done'

foo(3)
bar(3)
```

Output:
```py
Function timer started

Function foo(3,) {} Took 3.0094 seconds to run

Foo is done
('bar is done', 3.0135743618011475)
```
