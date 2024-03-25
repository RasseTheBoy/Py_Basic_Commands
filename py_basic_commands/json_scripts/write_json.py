import json

from py_basic_commands.json_scripts.read_json       import read_json
from py_basic_commands.fscripts                     import Fprint
from py_basic_commands.base                         import Base

from traceback      import format_exc
from typing         import Any
from os             import makedirs

fprint = Fprint()


class WriteJson(Base):
    def __init__(self, force:bool=False, indent:int=4, do_print:bool=True, encoding:str='utf-8'):
        super().__init__(do_print)

        self.force = force
        self.indent = indent
        self.encoding = encoding
                

    def __call__(self, data:Any, file_path:str, **kwargs) -> bool:
        """Write data to a JSON file.
        
        Parameters
        ----------
        data : Any
            The data to write to the JSON file. This can be a dictionary, list, or a string representation of JSON.
        file_path : str
            The path of the JSON file to write to.
        indent : int, optional
            The number of spaces to use for indentation in the JSON file. Default is 4.
        force : bool, optional
            Whether to overwrite any existing data in the JSON file. Default is False.
        do_print : bool, optional
            Whether to print information about the data writing process. Default is True.
        
        Returns
        -------
        bool
            Whether the file was created.
        """

        # Check input values
        indent = kwargs.get('indent', self.indent)
        force = kwargs.get('force', self.force)
        do_print = kwargs.get('do_print', self.do_print)
        encoding = kwargs.get('encoding', self.encoding)

        fprint.config(do_print=do_print)
        
        data_type = data.__class__.__name__

        try:
            if data_type == ('str'):
                data = json.loads(data)

            d = read_json(file_path, do_print=do_print, encoding=encoding)
            
            if d and not force:
                fprint(f'Data found in JSON file, not writing new data: {file_path}')
                return False

            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(data, f, indent=indent)

            fprint(f'Wrote data to JSON file: {file_path}')
            return True
        
        except TypeError:
            fprint(f'Data type is wrong, can\'t write to JSON: {data_type}')

        except FileNotFoundError:
            if force:
                fprint('Force is True, creating file path')
                makedirs(file_path)
                self(data, file_path, indent=indent, force=force, do_print=do_print)

        except Exception:
            fprint(format_exc())

        return False


write_json = WriteJson()

if __name__ == '__main__':
    # Test code
    data = {"name": "John", "age": 30, "city": "New York"}
    write_json(data, 'test.json', do_print=True, force=True)