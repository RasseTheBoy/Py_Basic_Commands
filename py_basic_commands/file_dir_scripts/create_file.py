from py_basic_commands.file_dir_scripts.create_dirs   import create_dirs
from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base
from traceback  import format_exc
from os.path   import exists

fprint = Fprint()


class CreateFile(Base):
    """Create a file at the specified path."""
    def __init__(self, force:bool=False, do_print:bool=True) -> None:
        """Initialize the class
        
        Parameters
        ----------
        force : bool, optional
            Whether to force the creation of the file. Default is False
        """
        super().__init__(do_print=do_print)

        self.force = force


    def _create_empty_file(self, dst_path:str) -> bool:
        """Create an empty file at the specified path
        
        Parameters
        ----------
        dst_path : str
            The path to create the file at

        Returns
        -------
        bool
            Whether the file was created
        """
        try:
            with open(dst_path, 'w') as f:
                f.write('')
            fprint(f'File created: {dst_path!r}')
            return True
        except Exception:
            fprint(format_exc())
            return False


    def __call__(self, dst_path:str, **kwargs) -> bool:
        """Create a file or directory at the specified path.
        
        Parameters
        ----------
        dst_path : str
            The path to create the file at
        force : bool, optional
            Whether to force the creation of the file. Default is False
        do_print : bool, optional
            Whether to print information about the file creation process. Default is True
        
        Returns
        -------
        bool
            Whether the file was created
        """
        # Check input values
        force = kwargs.get('force', self.force)
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)

        if dst_path == '':
            fprint('No path specified')
            return False

        # Check if file already exists
        create_dirs(dst_path, do_print=do_print)

        if exists(dst_path):
            fprint(f'File already exists: {dst_path}')
            if force:
                fprint('Force is enabled, creating new file...')
                return self._create_empty_file(dst_path)
            return False
        
        return self._create_empty_file(dst_path)


create_file = CreateFile()

if __name__ == '__main__':
    # Code testing
    create_file('test folder/test.txt', force=True)