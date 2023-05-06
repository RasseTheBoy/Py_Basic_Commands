import json

from py_basic_commands.json_scripts.read_json  import read_json
from py_basic_commands.file_dir_scripts.create_dirs import create_dirs
from dataclasses    import dataclass
from traceback  import format_exc
from py_basic_commands.fscripts   import fprint
from typing     import Any
from py_basic_commands.base   import Base


@dataclass
class WriteJson(Base):
    _indent:bool = True
    _force:bool = False

    def __post_init__(self):
        super().__init__()
                

    def __call__(self, data:Any, file_path:str, force:bool=None, indent:int=None, do_print:bool=None) -> bool:
        """Write data to a JSON file.
        
        Parameters:
        - `data` (Any): The data to write to the JSON file. This can be a dictionary, list, or a string representation of JSON.
        - `file_path` (str): The path of the JSON file to write to.
        - `indent` (int): The number of spaces to use for indentation in the JSON file. Default is `4`.
        - `force` (bool): Whether to overwrite any existing data in the JSON file. Default is `False`.
        - `do_print` (bool): Whether to print information about the data writing process. Default is `True`.

        Return:
        - `bool`: Whether the file was created.
        """

        # Check input values
        indent = self._check_input_val(indent, self._indent)
        force = self._check_input_val(force, self._force)
        do_print = self._check_input_val(do_print, self.do_print)

        fprint.config(do_print=do_print)

        try:
            if data.__class__.__name__ == ('str'):
                data = json.loads(data)

            d = read_json(file_path, do_print=do_print)
            
            if d and not force:
                fprint(f'Data found in JSON file, not writing new data: {file_path}')
                return False

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=indent)

            fprint(f'Wrote data to JSON file: {file_path}')
            return True
        except TypeError:
            fprint(f'Data type is wrong, can\'t write to JSON: {data.__class__.__name__}')
        except FileNotFoundError:
            if force:
                fprint('Force is True, creating file path')
                create_dirs(file_path)
                self(data, file_path, indent=indent, force=force, do_print=do_print)
        except Exception:
            fprint(format_exc())
        return False


write_json = WriteJson()

if __name__ == '__main__':
    # Test code
    data = {"name": "John", "age": 30, "city": "New York"}
    write_json(data, 'test.json', do_print=True, force=True)