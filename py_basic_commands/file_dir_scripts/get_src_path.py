from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
from os.path    import dirname, basename, splitext
from typing     import Any
from py_basic_commands.base   import Base

@dataclass
class GetSourcePath(Base):
    ret_val:bool = 'a'

    def __post_init__(self):
        super().__init__()


    def __call__(self, src_path:str, ret_val=None, do_print:bool=None) -> Any:
        """Get the path for the given source.
        
        Parameters
        ----------
        src_path : str
            Source path to get path for
        ret_val : str, optional
            Return value; 'a': (directory path, filename), 'd': directory path, 'fnam': filename, by default 'a'
        do_print : bool, optional
            Print output, by default True
        
        Returns
        -------
        Any"""

        if not src_path:
            fprint('No source path given')
            return None

        # Check input values
        ret_val = self._check_input_val(ret_val, self.ret_val)
        do_print = self._check_input_val(do_print, self.do_print)

        fprint.config(do_print=do_print)

        root, ext = splitext(src_path)
        if not ext:
            dir_path = root
            fnam = ''
        else:
            dir_path, fnam = dirname(root), basename(root) + ext

        match ret_val:
            case 'd':
                return dir_path
            case 'fnam':
                return fnam
            case 'a':
                return dir_path, fnam
            case _:
                fprint(f'Invalid value for `ret_val`: {ret_val}')
                return None
    

get_src_path = GetSourcePath()


if __name__ == '__main__':
    # Testing code
    src_path = 'folder/subfolder/file.txt'
    dir_path, fnam = get_src_path(src_path, ret_val='a', do_print=True)

    print(f'Direcotry path: {dir_path!r}')
    print(f'Filename: {fnam!r}')