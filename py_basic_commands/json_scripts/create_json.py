import json

from py_basic_commands.file_dir_scripts   import create_file, read_file
from py_basic_commands.json_scripts.read_json  import read_json
from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base

fprint = Fprint()


class CreateJson(Base):
<<<<<<< Updated upstream
    _force:bool = True
=======
    """Create a new empty JSON file."""
    def __init__(self, force:bool=True, do_print:bool=True):
        """Initialize the class
        
        Parameters
        ----------
        force : bool, optional
            Whether to overwrite any existing file with the same name. Default is True
        do_print : bool, optional
            Whether to print information about the file creation process. Default is True"""
        super().__init__(do_print)
>>>>>>> Stashed changes

        self.force = force


<<<<<<< Updated upstream
    def config(self, **kwargs):
        """Configure `create_json` variables"""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'force':
                self._force = value


    def __call__(self, file_path:str, force:bool=None, do_print:bool=None) -> bool:
=======
    def __call__(self, file_path:str, **kwargs) -> bool:
>>>>>>> Stashed changes
        """Create a new empty JSON file.
        
        Parameters
        ----------
        file_path : str
            The path for the new JSON file
        force : bool, optional
            Whether to overwrite any existing file with the same name. Default is True
        
        Returns
        -------
        bool
            Whether the file was created
        """

        # Check input values
<<<<<<< Updated upstream
        force = self._check_input_val(force, self._force)
        do_print = self._check_input_val(do_print, self._do_print)
=======
        force = kwargs.get('force', self.force)
        do_print = kwargs.get('do_print', self.do_print)
>>>>>>> Stashed changes

        fprint.config(do_print=do_print)

        write_empty_json = lambda: open(file_path, 'w').write(json.dumps({}, indent=4))

        did_create = create_file(file_path, force=force, do_print=do_print)
        if did_create:
            write_empty_json()
            fprint(f'New JSON created: {file_path}')
        elif read_json(file_path) == None:
            text = read_file(file_path, splitlines=False, do_print=do_print)
            if text and not force:
                fprint(f'Cannot create new JSON file. Text found in file; and force set as False: {file_path}')
                return did_create
            write_empty_json()
            fprint(f'Basic brackets added to JSON: {file_path}')
        
        return did_create


create_json = CreateJson()


if __name__ == '__main__':
    from FastDebugger import fd
    # Test code
    fd(create_json('test.json', force=True))