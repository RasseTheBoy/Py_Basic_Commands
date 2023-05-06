from py_basic_commands.file_dir_scripts.create_dirs   import create_dirs
from dataclasses    import dataclass
from traceback  import format_exc
from py_basic_commands.fscripts   import fprint
from os.path   import exists
from py_basic_commands.base   import Base


@dataclass
class CreateFile(Base):
    _force:bool = False

    def __post_init__(self):
        super().__init__()


    def _create_empty_file(self, dst_path:str) -> bool:
        """Create an empty file at the specified path.
        
        Parameters:
        - `dst_path` (str): The path to create the file at.
        
        Returns:
        - `bool`: Whether the file was created.
        """
        try:
            with open(dst_path, 'w') as f:
                f.write('')
            fprint(f'File created: {dst_path}')
            return True
        except Exception:
            fprint(format_exc())
            return False


    def __call__(self, dst_path:str, force:bool=None, do_print:bool=None) -> bool:
        """Create a file or directory at the specified path.
        
        Parameters:
        - `dst_path` (str): The path to create the file or directory at.
        - `force` (bool): Whether to force the creation of the file or directory by deleting any existing file or directory with the same name. Default is `False`
        - `do_print` (bool): Whether to print information about the file or directory creation process. Default is `True`
        
        Returns:
        - `bool`: Whether the file or directory was created.
        """

        if dst_path == '':
            fprint('No path specified')
            return False

        # Check input values
        force = self._check_input_val(force, self._force)
        do_print = self._check_input_val(do_print, self.do_print)

        fprint.config(do_print=do_print)

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