import json

from py_basic_commands.fscripts     import Fprint
from py_basic_commands.base         import Base
from traceback  import format_exc
from typing     import Any


fprint = Fprint()


class ReadJson(Base):
    """Read data from a JSON file"""
    def __init__(self, do_print:bool=True, create:bool=True, encoding:str='utf-8') -> None:
        """Initialize the class

        Parameters
        ----------
        do_print : bool, optional
            Whether to get feedback printed to terminal or not. Default is True.
        create : bool, optional
            Whether to create the file if it doesn't exist. Default is True.
        """
        super().__init__(do_print)
        self.create = create
        self.encoding = encoding


    def __call__(self, file_path:str, **kwargs) -> dict:
        """Read data from a JSON file.
        
        Parameters
        ----------
        file_path : str
            The path of the JSON file to read from.
        do_print : bool, optional
            Whether to get feedback printed to terminal or not. Default is True.
        create : bool, optional
            Whether to create the file if it doesn't exist. Default is True.
        
        
        Returns
        -------
        Any
            The data from the JSON file, as a dictionary or list.
        """

        # Check input values
        do_print = kwargs.get('do_print', self.do_print)
        create = kwargs.get('create', self.create)
        encoding = kwargs.get('encoding', self.encoding)

        fprint.config(do_print=do_print)

        file_data = {}

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                file_data = json.load(f)
        
        except FileNotFoundError:
            fprint.error(f'File not found: {file_path!r}')
            if create:
                # Create empty json file
                json.dump({}, open(file_path, 'w', encoding=encoding))
                fprint(f'Created file: {file_path!r}')

        except json.decoder.JSONDecodeError:
            fprint.error(f'File cannot be read as a JSON: {file_path}')

        except Exception:
            fprint.error(format_exc())

        finally:
            return file_data


read_json = ReadJson()


if __name__ == '__main__':
    from FastDebugger import fd
    # Test code
    file_path = 'test.json'
    data = read_json(file_path)
    fd(data)