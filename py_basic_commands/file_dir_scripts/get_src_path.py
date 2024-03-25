from py_basic_commands.fscripts   import Fprint
from os.path    import dirname, basename, splitext
from typing     import Any
from py_basic_commands.base   import Base

fprint = Fprint()


class GetSourcePath(Base):
    """Get the path for the given source"""
    def __init__(self, ret_val:str='a', do_print:bool=True):
        """Initialize the class
        
        Parameters
        ----------
        ret_val : str, optional
            Return value; 'a': (directory path, filename), 'd': directory path, 'f': filename, by default 'a'"""
        super().__init__(do_print=do_print)

        self.ret_val = ret_val


    def __call__(self, src_path:str, **kwargs) -> Any:
        """Get the path for the given source.
        
        Parameters
        ----------
        src_path : str
            Source path to get path for
        ret_val : str, optional
            Return value; 'a': (directory path, file name), 'd': directory path, 'f': file name, by default 'a'
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

        if not src_path:
            fprint('No source path given')
            return None

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
    from FastDebugger import fd

    # Testing code
    src_path = '/file.txt'
    out = get_src_path(src_path, ret_val='d', do_print=True)

    fd(out)
    # print(f'Direcotry path: {dir_path!r}')
    # print(f'Filename: {fnam!r}')