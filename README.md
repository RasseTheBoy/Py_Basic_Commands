
# Py Basic Tools

A package including some basic tools for Python (3)

## Author

- [@RasseTheBoy](https://github.com/RasseTheBoy)


## Installation

Install my-project with pip

```bash
  pip install py_basic_commands

  pip3 install py_baisc_commands
```
    
## Examples

### fprint
```
from py_basic_tools import fprint

print('Hello world')
>> Hello world!

fprint('Hello world!') # new line after string
>> Hello world!\n

fprint('Hello world!', nl=False) # No new line after string (works like normal print)
>> Hello world
```

### enter_to_continue
```
from py_basic_tools import enter_to_continue

enter_to_continue()
>> Press enter to continue...
>>
>>

enter_to_continue('Waiting')
>> Waiting (enter to continue)
>>
>>

enter_to_continue('Waiting', nl=False) # Removes new line after input
>> Waiting
>>

returned_value = enter_to_continue('Should this continue?', ret=True) # If the input isn't empty, the returned value is False
print(f'Returned value: {returned_value}')
>> Should this continue? (enter to continue)
>>
>> Returned value: True
```
