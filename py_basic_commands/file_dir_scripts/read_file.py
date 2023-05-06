from py_basic_commands.file_dir_scripts   import create_file
from dataclasses    import dataclass
from py_basic_commands.fscripts.fprint   import fprint
from typing     import Any
from py_basic_commands.base   import Base


@dataclass
class ReadFile(Base):
    _create:bool = False
    _ret_did_create:bool = False
    _splitlines:bool = True
    _remove_empty:bool = True
    _do_strip:bool = True
    _do_lower:bool = False
    _encoding:str = 'utf-8'


    def __post_init__(self):
        super().__init__()

    
    def __call__(self, file_path:str, create:bool=None, ret_did_create:bool=None, splitlines:bool=None, remove_empty:bool=None, do_strip:bool=None, do_lower:bool=None, encoding:str=None, do_print:bool=None) -> Any:
        """Read the contents of a file.
        
        Parameters:
        - `file_path` (str): The path to the file to read.
        - `create` (bool): Whether to create the file if it does not exist. Default is `False`
        - `ret_did_create` (bool): Whether to return a tuple of the file contents and a bool indicating whether the file was created. Default is `False`
        - `splitlines` (bool): Whether to split the file contents into a list of lines. Default is `True`
        - `remove_empty` (bool): Whether to remove empty lines when `splitlines` is True. Default is `True`
        - `strip` (bool): Whether to strip leading and trailing whitespace from each line when `splitlines` is True.
        - `encoding` (str): The encoding to use when reading the file. Default is `utf-8`
        - `do_print` (bool): Whether to print information about the file reading process. Default is `True`
        
        Returns:
        - `Any`: If `ret_did_create` is True, a tuple containing the file contents and a bool indicating whether the file was created. Otherwise, the file contents.
        """
        
        def try_reading(did_create:bool=False) -> list and bool:
            """Tries reading the file. If the file does not exist, creates it if `create` is True.
            
            Parameters:
            - `did_create` (bool): Whether the file was created.
            
            Returns:
            - `Any`: If `ret_did_create` is True, a tuple containing the file contents and a bool indicating whether the file was created. Otherwise, the file contents.
            """
            lines: list[str] | str = []
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    lines = f.read()
                if splitlines:
                    lines = lines.splitlines()
                    if remove_empty:
                        lines = [x for x in lines if x != '']
                    if do_strip:
                        lines = [x.strip() for x in lines]
                    if do_lower:
                        lines = [x.lower() for x in lines]
                return lines, did_create
            except FileNotFoundError:
                fprint(f'File not found: {file_path}', do_print=do_print)
                if create:
                    create_file(file_path, force=True, do_print=do_print)
                    return try_reading(True)
            return lines, did_create

        # Check input values
        create      = self._check_input_val(create, self._create)
        ret_did_create = self._check_input_val(ret_did_create, self._ret_did_create)
        splitlines  = self._check_input_val(splitlines, self._splitlines)
        remove_empty = self._check_input_val(remove_empty, self._remove_empty)
        do_strip    = self._check_input_val(do_strip, self._do_strip)
        do_lower    = self._check_input_val(do_lower, self._do_lower)
        encoding    = self._check_input_val(encoding, self._encoding)
        do_print    = self._check_input_val(do_print, self._do_print)

        fprint.config(do_print=do_print)

        lines, did_create = try_reading()

        # Return the file contents
        if ret_did_create:
            return lines, did_create
        return lines


read_file = ReadFile()

if __name__ == '__main__':
    from FastDebugger import fd

    # Test code
    file_path = 'Test folder/here.txt'
    f = read_file(file_path, create=True)
    fd(f)

