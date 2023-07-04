from py_basic_commands.file_dir_scripts   import read_file
<<<<<<< Updated upstream
from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
from shutil     import rmtree
from py_basic_commands.base   import Base
from os     import listdir, remove
=======
from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base
from dataclasses    import dataclass
from send2trash import send2trash
from os.path import isfile, isdir
from os     import listdir
>>>>>>> Stashed changes

fprint = Fprint()


@dataclass
class RemoveFileDir(Base):
<<<<<<< Updated upstream
    _force:bool = True
=======
    """Remove a file or directory at the specified path."""
    def __init__(self, force:bool=True, do_print:bool=True):
        """Initialize the class
>>>>>>> Stashed changes

        Parameters
        ----------
        force : bool, optional
            Whether to force the removal of the file or directory. Default is True
        do_print : bool, optional
            Whether to print information about the file or directory removal process. Default is True
        """
        super().__init__(do_print)

        self.force = force

    
    def config(self, **kwargs):
        """Configure `remove_file_dir` variables"""
        self._config(**kwargs)

<<<<<<< Updated upstream
        for key, value in kwargs.items():
            if key == 'force':
                self._force = value

    @try_traceback(print_traceback=True)
    def __call__(self, do:str, do_path:str, force:bool=False, do_print:bool=True) -> bool:
=======
    def __call__(self, do:str, do_path:str, **kwargs) -> bool:
>>>>>>> Stashed changes
        """Remove a file or directory at the specified path.
        
        Parameters
        ----------
        do : str
            Whether to remove a file or directory. Must be either 'f' or 'd'
        do_path : str
            The path to remove the file or directory at
        force : bool, optional
            Whether to force the removal of the file or directory. Default is True
        do_print : bool, optional
            Whether to print information about the file or directory removal process. Default is True
    
        Returns
        -------
        bool
            Whether the file or directory was removed

        Raises
        ------
        ValueError
            If an invalid `do` value is given
        """

        # Check input values
<<<<<<< Updated upstream
        force    = self._check_input_val(force, self._force)
        do_print = self._check_input_val(do_print, self._do_print)
=======
        force    = kwargs.get('force', self.force)
        do_print = kwargs.get('do_print', self.do_print)
>>>>>>> Stashed changes

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
                send2trash(do_path)
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
        
        else:
            raise ValueError(f'Invalid do value given: {do}')


remove_file_dir = RemoveFileDir()

if __name__ == '__main__':
    # Test code
    remove_file_dir('d', 'Test folder', force=True)