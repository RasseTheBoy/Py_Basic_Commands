import sys
sys.path.append('..')

from py_basic_commands.other.basic_commands     import try_traceback
from py_basic_commands.file_dir_scripts   import read_file
from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
from shutil     import rmtree
from py_basic_commands.base   import Base
from os     import listdir, remove


@dataclass
class RemoveFileDir(Base):
    _force:bool = True

    def __post_init__(self):
        super().__init__()

    
    def config(self, **kwargs):
        """Configure `remove_file_dir` variables"""
        self._config(**kwargs)

        if 'force' in kwargs:
            self._force = kwargs['force']

    @try_traceback(print_traceback=True)
    def __call__(self, do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
        """Remove a file or directory at the specified path.
        
        Parameters:
        - `do` (str): Whether to remove a `'d'`irectory or a `'f'`ile.
        - `do_path` (str): The path to the file or directory to remove.
        - `force` (bool): Whether to force the removal of the file or directory.
        - `do_print` (bool): Whether to print information about the file or directory removal process.
        
        Returns:
        - `bool`: Whether the file or directory was removed.
        """

        # Check input values
        force    = self._check_input_val(force, self._force)
        do_print = self._check_input_val(do_print, self._do_print)

        fprint.config(do_print=do_print)

        if do == 'd': # Directory
            try:
                dir_content = listdir(do_path)
            except FileNotFoundError:
                fprint(f'Directory path not found: {do_path}')
                return False
            except NotADirectoryError:
                fprint(f'Path is not a directory: {do_path}')
                return False

            if not dir_content or force:
                rmtree(do_path)
                fprint(f'Directory removed: {do_path}')
                return True
                
            elif dir_content:
                fprint(f'Directory is not empty, not removing: {do_path}')
                return False
            
            else:
                return False

        elif do == 'f': # File
            lines = read_file(do_path)
            if lines and not force:
                fprint(f'File is not empty, not removing: {do_path}')
                return False
            remove(do_path)
            fprint(f'File removed: {do_path}')
            return True


remove_file_dir = RemoveFileDir()

if __name__ == '__main__':
    # Test code
    remove_file_dir('d', 'Test folder', force=True)