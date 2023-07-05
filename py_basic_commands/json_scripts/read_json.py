import json

from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base
from traceback  import format_exc
from typing import Any

fprint = Fprint()


class ReadJson(Base):
    """Read data from a JSON file"""
    def __init__(self, do_print:bool=True) -> None:
        """Initialize the class

        Parameters
        ----------
        do_print : bool, optional
            Whether to get feedback printed to terminal or not. Default is True.
        """
        super().__init__(do_print)


    def __call__(self, file_path:str, **kwargs) -> Any:
        """Read data from a JSON file.
        
        Parameters
        ----------
        file_path : str
            The path of the JSON file to read from.
        do_print : bool, optional
            Whether to get feedback printed to terminal or not. Default is True.
        
        Returns
        -------
        Any
            The data from the JSON file, as a dictionary or list.
        """

        # Check input values
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)

        try:
            with open(file_path, 'r') as f:
                file_data = json.load(f)
            return file_data
        except FileNotFoundError:
            fprint(f'File not found: {file_path}')
        except json.decoder.JSONDecodeError:
            fprint(f'File cannot be read as a JSON: {file_path}')
        except Exception:
            fprint(format_exc())


read_json = ReadJson()


if __name__ == '__main__':
    from FastDebugger import fd
    # Test code
    file_path = 'test.json'
    data = read_json(file_path)
    fd(data)