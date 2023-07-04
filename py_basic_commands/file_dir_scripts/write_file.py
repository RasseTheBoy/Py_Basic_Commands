from py_basic_commands.file_dir_scripts   import read_file
from dataclasses    import dataclass
from traceback  import format_exc
from py_basic_commands.fscripts   import Fprint
from typing     import Any
from py_basic_commands.base   import Base

fprint = Fprint()


@dataclass
class WriteFile(Base):
<<<<<<< Updated upstream
    _append:bool    = False
    _force_create:bool  = True
    _remove_duplicates:bool = False
    _encoding:str   = 'utf-8'
=======
    """Write text to a file"""
    append:bool    = False
    force_create:bool  = True
    remove_duplicates:bool = False
    encoding:str   = 'utf-8'
>>>>>>> Stashed changes

    def __post_init__(self):
        super().__init__()


<<<<<<< Updated upstream
    def config(self, **kwargs):
        """Configure variables."""
        self._config(**kwargs)

        for key, value in kwargs.items():
            if key == 'append':
                self._append = value
            elif key == 'force_create':
                self._force_create = value
            elif key == 'remove_duplicates':
                self._remove_duplicates = value
            elif key == 'encoding':
                self._encoding = value


    def __call__(self, text:Any, file_path:str, append:bool=None, force_create:bool=None, remove_duplicates:bool=None, encoding:str=None, do_print:bool=None) -> bool:
        """Write text to a file.
        
        Parameters:
        - `text` (Any): The text to write. Can be a string, list, tuple, set or a numpy.array.
        - `file_path` (str): The path to the file to write to.
        - `append` (bool): Whether to append the text to the end of the file.
        - `force_create` (bool): Whether to create the file if it does not exist.
        - `remove_duplicates` (bool): Whether to remove duplicates from a list, tuple or set
        - `encoding` (str): The encoding to use when writing the file.
        - `do_print` (bool): Whether to print information about the file writing process.
=======
    def __call__(self, text:Any, file_path:str, **kwargs) -> bool:
        """Write text to a file.
        
        Parameters
        ----------
        text : Any
            The text to write to the file. If a list, tuple or set is given, the values will be joined by a newline character
        file_path : str
            The path to write the text to
        append : bool, optional
            Whether to append the text to the file. Default is False
        force_create : bool, optional
            Whether to force the creation of the file. Default is True
        remove_duplicates : bool, optional
            Whether to remove duplicate lines from the text. Default is False
        encoding : str, optional
            The encoding to use when writing to the file. Default is 'utf-8'
        do_print : bool, optional
            Whether to print information about the file creation process. Default is True
>>>>>>> Stashed changes
        
        Returns
        -------
        bool
            Whether the text was written to the file
        """

        # Check input values
<<<<<<< Updated upstream
        append = self._check_input_val(append, self._append)
        force_create = self._check_input_val(force_create, self._force_create)
        remove_duplicates = self._check_input_val(remove_duplicates, self._remove_duplicates)
        encoding = self._check_input_val(encoding, self._encoding)
        do_print = self._check_input_val(do_print, self._do_print)
=======
        append = kwargs.get('append', self.append)
        force_create = kwargs.get('force_create', self.force_create)
        remove_duplicates = kwargs.get('remove_duplicates', self.remove_duplicates)
        encoding = kwargs.get('encoding', self.encoding)
        do_print = kwargs.get('do_print', self.do_print)
>>>>>>> Stashed changes

        fprint.config(do_print=do_print)

        if text.__class__.__name__ == 'ndarray':
            text = text.tolist()
        
        if text.__class__.__name__ in ('list', 'tuple', 'set'):
            if remove_duplicates:
                text = list(dict.fromkeys(text))
            text = '\n'.join(text)

        lines, did_create = read_file(file_path, create=force_create, ret_did_create=True, remove_empty=False, splitlines=False, do_print=do_print)

        if len(lines.strip()) > 0 and not force_create and not append:
            fprint('Not writing to file. File has content; and foce_create is set to False')
            return did_create

        try:
            # Don't add newline if the last line already has one
            if lines[-1] == '\n':
                text = text.strip()

            # if not did_create and lines[-1] != '\n':
            #     text = '\n' + text 
        except IndexError:
            pass
        except Exception:
            fprint(format_exc())

        if append:
            mode = 'a'
        else:
            mode = 'w'

        with open(file_path, mode=mode, encoding=encoding) as f:
            f.write(text + '\n')
            fprint(f'Content written to file: {file_path}')

        return did_create


write_file = WriteFile()

if __name__ == '__main__':
    # Test
    write_file('test text\nAnd another row', 'Test folder/here.txt')