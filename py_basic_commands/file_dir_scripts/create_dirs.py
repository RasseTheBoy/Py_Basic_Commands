from py_basic_commands.file_dir_scripts.get_src_path  import get_src_path
from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base
from os.path import exists
from os     import makedirs

fprint = Fprint()


class CreateDirs(Base):
    """Create all required directories for the given path"""
    def __init__(self, do_print:bool=True):
        """Initialize the class
        
        Parameters
        ----------
        do_print : bool, optional
            Whether to print information about the directory creation process. Default is True"""
        super().__init__(do_print)


    def __call__(self, dst_path:str, includes_file:bool=True, **kwargs) -> bool:
            """Create all required directories for the given path.
            
            Parameters
            ----------
            dst_path : str
                The path to create the directories for.
            includes_file : bool, optional
                Whether the path includes a file. Default is True
            do_print : bool, optional
                Whether to print information about the directory creation process. Default is True

            Returns
            -------
            bool
                Whether the directories were created
            """
            # Check input values
            do_print = kwargs.get('do_print', self.do_print)
            
            # Set print config
            fprint.config(do_print=do_print)

            if not isinstance(dst_path, str):
                raise TypeError(f'dst_path must be a string, not {type(dst_path)}')
            
            elif dst_path == '':
                raise ValueError('dst_path cannot be an empty string')
            
            elif exists(dst_path):
                fprint(f'dst_path already exists: {dst_path!r}')
                return False

            if dst_path == '':
                return False

            if includes_file:
                dir_path = get_src_path(dst_path, ret_val='d', do_print=do_print)
            else:
                dir_path = dst_path

            if dir_path == '':
                return False

            try:
                makedirs(dir_path)
                fprint(f'Destination created for path: {dir_path}')
                return True

            except FileExistsError:
                fprint(f'Path already exists: {dir_path}')

            except TypeError:
                fprint(f'Type error in {dir_path}')
            
            return False


create_dirs = CreateDirs()

if __name__ == '__main__':
    # Code testing
    create_dirs('test folder/subfolder/file.txt')
