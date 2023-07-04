from py_basic_commands.file_dir_scripts   import create_file
from dataclasses    import dataclass
from py_basic_commands.fscripts.fprint   import Fprint
from typing     import Any
from py_basic_commands.base   import Base

fprint = Fprint()


@dataclass
class ReadFile(Base):
<<<<<<< Updated upstream
    _create:bool = False
    _ret_did_create:bool = False
    _splitlines:bool = True
    _remove_empty:bool = True
    _do_strip:bool = True
    _do_lower:bool = False
    _encoding:str = 'utf-8'
=======
    """Read the contents of a file"""
    create:bool         = False
    ret_did_create:bool = False
    splitlines:bool     = True
    remove_empty:bool   = True
    do_strip:bool       = True
    do_lower:bool       = False
    encoding:str        = 'utf-8'
>>>>>>> Stashed changes


    def __post_init__(self):
        super().__init__()


    def config(self, **kwargs):
        """Configure variables"""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'create':
                self._create = value
            elif key == 'ret_did_create':
                self._ret_did_create = value
            elif key == 'splitlines':
                self._splitlines = value
            elif key == 'remove_empty':
                self._remove_empty = value
            elif key == 'do_strip':
                self._do_strip = value
            elif key == 'do_lower':
                self._do_lower = value
            elif key == 'encoding':
                self._encoding = value

    
    def __call__(self, file_path:str, **kwargs) -> Any:
        """Read the contents of a file.
        
        Parameters
        ----------
        file_path : str
            The path to the file to read
        create : bool, optional
            Whether to create the file if it does not exist. Default is False
        ret_did_create : bool, optional
            Whether to return whether the file was created. Default is False
        splitlines : bool, optional
            Whether to split the file contents by line. Default is True
        remove_empty : bool, optional
            Whether to remove empty lines from the file contents; only works if `splitlines` is True. Default is True
        do_strip : bool, optional
            Whether to strip the file contents of whitespace; only works if `splitlines` is True. Default is True
        do_lower : bool, optional
            Whether to convert the file contents to lowercase. Default is False
        encoding : str, optional
            The encoding to use when reading the file. Default is 'utf-8'
        do_print : bool, optional
            Whether to print information about the file creation process. Default is True
        
        Returns
        -------
        Any
            The file contents
        """
        
        def try_reading(did_create:bool=False) -> tuple:
            """Tries reading the file. If the file does not exist, creates it if `create` is True.
            
            Parameters
            ----------
            did_create : bool, optional
                Whether the file was created. Default is False
            
            Returns
            -------
            tuple
                The file contents and whether the file was created
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
<<<<<<< Updated upstream
        create      = self._check_input_val(create, self._create)
        ret_did_create = self._check_input_val(ret_did_create, self._ret_did_create)
        splitlines  = self._check_input_val(splitlines, self._splitlines)
        remove_empty = self._check_input_val(remove_empty, self._remove_empty)
        do_strip    = self._check_input_val(do_strip, self._do_strip)
        do_lower    = self._check_input_val(do_lower, self._do_lower)
        encoding    = self._check_input_val(encoding, self._encoding)
        do_print    = self._check_input_val(do_print, self._do_print)
=======
        create          = kwargs.get('create', self.create)
        ret_did_create  = kwargs.get('ret_did_create', self.ret_did_create)
        splitlines      = kwargs.get('splitlines', self.splitlines)
        remove_empty    = kwargs.get('remove_empty', self.remove_empty)
        do_strip        = kwargs.get('do_strip', self.do_strip)
        do_lower        = kwargs.get('do_lower', self.do_lower)
        encoding        = kwargs.get('encoding', self.encoding)
        do_print        = kwargs.get('do_print', self.do_print)
>>>>>>> Stashed changes

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

