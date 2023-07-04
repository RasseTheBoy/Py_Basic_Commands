from py_basic_commands.file_dir_scripts.get_src_path  import get_src_path
<<<<<<< Updated upstream
from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
=======
from py_basic_commands.fscripts   import Fprint
>>>>>>> Stashed changes
from py_basic_commands.base   import Base
from os     import makedirs


fprint = Fprint()


class CreateDirs(Base):
    """Create all required directories for the given path"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()


<<<<<<< Updated upstream
    def config(self, **kwargs):
        """Conmfigure `create_dirs` variables"""
        self._config(**kwargs)


    def __call__(self, dst_path:str, do_print:bool=None) -> bool:
            """Create all required directories for the given path.
            
            Parameters:
            - `dst_path` (str): Destination path; can include the file name at the end.
            - `do_print` (bool): Whether to print or not. Default is `True`
            
            Returns:
            - `bool`: If all directories were created or not"""

            # Check input values
            do_print = self._check_input_val(do_print, self._do_print)

=======
    def __call__(self, dst_path:str, **kwargs) -> bool:
            """Create all required directories for the given path.
            
            Parameters
            ----------
            dst_path : str
                The path to create the directories for.
            do_print : bool, optional
                Whether to print information about the directory creation process. Default is `True`

            Returns
            -------
            bool
                Whether the directories were created
            """

            # Check input values
            do_print = kwargs.get('do_print', self.do_print)

            # Set print config
>>>>>>> Stashed changes
            fprint.config(do_print=do_print)

            if dst_path == '':
                return False

            dir_path = get_src_path(dst_path, ret_val='d', do_print=do_print)

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
