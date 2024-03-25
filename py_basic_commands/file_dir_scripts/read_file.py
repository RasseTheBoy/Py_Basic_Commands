from py_basic_commands.file_dir_scripts   import create_file
from py_basic_commands.fscripts.fprint   import Fprint
from py_basic_commands.base   import Base
from dataclasses    import dataclass
from typing     import Any

fprint = Fprint()


@dataclass
class ReadFile(Base):
    """Read the contents of a file"""
    create:bool         = False
    ret_did_create:bool = False
    splitlines:bool     = True
    remove_empty:bool   = True
    do_strip:bool       = True
    do_lower:bool       = False
    encoding:str        = 'utf-8'
    do_print:bool       = True

    def __post_init__(self):
        super().__init__(self.do_print)

    
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
                    if do_strip:
                        lines = [x.strip() for x in lines]
                    if remove_empty:
                        lines = [x for x in lines if x != '']
                    if do_lower:
                        lines = [x.lower() for x in lines]
            
            except FileNotFoundError:
                fprint(f'File not found: {file_path}')
                if create:
                    create_file(file_path, force=True)
                    return try_reading(True)
                
            except UnicodeDecodeError:
                fprint(f'Could not read file: {file_path}')
                lines = []
                
            if not lines and not splitlines:
                lines = ''
                
            return lines, did_create

        # Check input values
        create          = kwargs.get('create', self.create)
        ret_did_create  = kwargs.get('ret_did_create', self.ret_did_create)
        splitlines      = kwargs.get('splitlines', self.splitlines)
        remove_empty    = kwargs.get('remove_empty', self.remove_empty)
        do_strip        = kwargs.get('do_strip', self.do_strip)
        do_lower        = kwargs.get('do_lower', self.do_lower)
        encoding        = kwargs.get('encoding', self.encoding)
        do_print        = kwargs.get('do_print', self.do_print)

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

