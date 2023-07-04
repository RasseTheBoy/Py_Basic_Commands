from py_basic_commands.fscripts   import Fprint
from os.path    import dirname, basename, splitext
from typing     import Any
from py_basic_commands.base   import Base

<<<<<<< Updated upstream
@dataclass
class GetSourcePath(Base):
    _ret_val:bool = 'a'
=======
fprint = Fprint()
>>>>>>> Stashed changes


class GetSourcePath(Base):
    """Get the path for the given source"""
    def __init__(self, ret_val:str='a'):
        """Initialize the class
        
        Parameters
        ----------
        ret_val : str, optional
            Return value; 'a': (directory path, filename), 'd': directory path, 'f': filename, by default 'a'"""
        super().__init__()

        self.ret_val = ret_val

<<<<<<< Updated upstream
    def config(self, **kwargs):
        """Configure variables"""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'ret_val':
                self._ret_val = value


    def __call__(self, src_path:str, ret_val=None, do_print:bool=None) -> Any:
        """Get the path for the given source.
        
        Parameters:
        - `src_path` (str): The path to the source.
        - `ret_val` (str): Whether to return the `'d'`irectory path, `'fnam'`e of the file, or `'a'`ll (default).
        
        Returns:
        - `Any`: If `ret_val` is `'d'`, the directory path. If `ret_val` is `'fnam'`, the filename. Otherwise, a tuple containing the directory path and the filename.
        """
=======

    def __call__(self, src_path:str, **kwargs) -> Any:
        """Get the path for the given source.
        
        Parameters
        ----------
        src_path : str
            Source path to get path for
        ret_val : str, optional
            Return value; 'a': (directory path, filename), 'd': directory path, 'f': filename, by default 'a'
        do_print : bool, optional
            Print output, by default True
        
        Returns
        -------
        Any
            The path for the given source
        """
        # Check input values
        ret_val = kwargs.get('ret_val', self.ret_val)
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)
>>>>>>> Stashed changes

        if not src_path:
            fprint('No source path given')
            return None

<<<<<<< Updated upstream
        # Check input values
        ret_val = self._check_input_val(ret_val, self._ret_val)
        do_print = self._check_input_val(do_print, self._do_print)

        fprint.config(do_print=do_print)

=======
>>>>>>> Stashed changes
        root, ext = splitext(src_path)
        if not ext:
            dir_path = root
            file_name = ''
        else:
            dir_path, file_name = dirname(root), basename(root) + ext

        match ret_val:
            case 'd':
                return dir_path
            case 'f':
                return file_name
            case 'a':
                return dir_path, file_name
            case _:
                fprint(f'Invalid value for `ret_val`: {ret_val}')
                return None
    

get_src_path = GetSourcePath()


if __name__ == '__main__':
    # Testing code
    src_path = 'folder/subfolder/file.txt'
    dir_path, fnam = get_src_path(src_path, ret_val='f', do_print=True)

    print(f'Direcotry path: {dir_path!r}')
    print(f'Filename: {fnam!r}')