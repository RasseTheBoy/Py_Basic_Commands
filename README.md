
# Py Basic Tools

A package with some basic tools for Python (3)

## Author

- [@RasseTheBoy](https://github.com/RasseTheBoy)


## Installation

Install my-project with pip

```bash
  pip install py_basic_tools

  pip3 install py_baisc_tools
```
    
## Examples

### fprint
```
from py_basic_tools import fprint

print('Hello world')
>> Hello world!

fprint('Hello world!') # Linebreak after string
>> Hello world!\n

fprint('Hello world!', nl=False) # No linebreak after string (works like normal print)
>> Hello world
```

### enter_to_continue
```
from py_basic_tools import enter_to_continue

enter_to_continue() # Adds an extra print after the input command
>> Press enter to continue...
>>
>>

enter_to_continue('Waiting') # Write your own string in the 
>> Waiting (enter to continue)
>>
>>

enter_to_continue('Waiting', nl=False) # Removes newline after input
>> Waiting
>>

returned_value = enter_to_continue('Should this continue?') # If the input isn't empty, the returned value is False
print(f'Returned value: {returned_value}')
>> Should this continue? (enter to continue)
>>
>> Returned value: True

enter_to_continue('To be, or not to be?', use_help_text=False) # Removes the "help text" from the input string
>>To be, or not to be?
>>
>>
```
