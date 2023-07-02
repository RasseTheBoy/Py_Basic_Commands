from py_basic_commands.file_dir_scripts.get_src_path  import get_src_path
from py_basic_commands.fscripts   import fprint
from py_basic_commands.base   import Base
from dataclasses    import dataclass
from os     import makedirs

@dataclass
class CreateDirs(Base):
    def __post_init__(self):
        super().__init__()


    def __call__(self, dst_path:str, do_print:bool=None) -> bool:
            """Create all required directories for the given path.
            
            Parameters
            ----------
            dst_path : str
                Path to create directories for
            do_print : bool, optional
                Print output, by default None
                
            Returns
            -------
            bool
                True if directories were created, False otherwise
                
            Raises
            ------
            ValueError
                If empty path is given"""

            # Check input values
            do_print = self._check_input_val(do_print, self.do_print)
            fprint.config(do_print=do_print)

            if dst_path == '': # Check if empty path is given
                raise ValueError('Empty path given')

            dir_path = get_src_path(dst_path, ret_val='d', do_print=do_print)

            if dir_path == '':
                # No directory path found
                return False

            try:
                makedirs(dir_path)
                # print(f'Destination created for path: {dir_path}')
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
