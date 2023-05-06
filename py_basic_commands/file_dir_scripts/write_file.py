from py_basic_commands.file_dir_scripts   import read_file
from dataclasses    import dataclass
from traceback  import format_exc
from py_basic_commands.fscripts   import fprint
from typing     import Any
from py_basic_commands.base   import Base


@dataclass
class WriteFile(Base):
    _append:bool    = False
    _force_create:bool  = True
    _remove_duplicates:bool = False
    _encoding:str   = 'utf-8'

    def __post_init__(self):
        super().__init__()


    def __call__(self, text:Any, file_path:str, append:bool=None, force_create:bool=None, remove_duplicates:bool=None, encoding:str=None, do_print:bool=None) -> bool:
        """Write text to a file.
        
        Parameters:
        - `text` (Any): The text to write. Can be a string, list, tuple, set or a numpy.array.
        - `file_path` (str): The path to the file to write to.
        - `append` (bool): Whether to append the text to the end of the file. Default is `False`.
        - `force_create` (bool): Whether to create the file if it does not exist. Default is `True`.
        - `remove_duplicates` (bool): Whether to remove duplicates from a list, tuple or set before writing to file. Default is `False`.
        - `encoding` (str): The encoding to use when writing the file. Default is `utf-8`.
        - `do_print` (bool): Whether to print information about the file writing process. Default is `True`.
        
        Returns:
        - `bool`: Whether the file was created.
        """

        # Check input values
        append = self._check_input_val(append, self._append)
        force_create = self._check_input_val(force_create, self._force_create)
        remove_duplicates = self._check_input_val(remove_duplicates, self._remove_duplicates)
        encoding = self._check_input_val(encoding, self._encoding)
        do_print = self._check_input_val(do_print, self.do_print)

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
            if not did_create and lines[-1] != '\n':
                text = '\n' + text 
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