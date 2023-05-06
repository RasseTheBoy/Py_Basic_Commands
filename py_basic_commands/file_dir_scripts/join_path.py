from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
from os.path    import dirname, basename, splitext
from py_basic_commands.base   import Base


@dataclass
class JoinPath(Base):
    _join_with:str = '/'
    _remove_empty:bool=True
    _dir_end:bool=False

    def __post_init__(self):
        super().__init__(False)


    def __call__(self, *args:str, join_with:str=None, remove_empty:bool=None, dir_end:bool=None, do_print:bool=None) -> str:
        r"""Join path segments together, removing certain characters (`<>:"/\|?*`) and adjust for correct slash direction.

        Parameters:
        - `*args` (str): One or more path segments to join.
        - `join_with` (str): The separator to use when joining the path segments. Default is `'/'`.
        - `remove_empty` (bool): Remove empty strings. Default is `True`.
        - `dir_end` (bool): Specify whether to add join_with character at the end of the returned path. Default is `False`.
        - `do_print` (bool): Whether to print or not. Default is `False`.

        Return:
        A `string` representing the joined path.
        """

        def split_join(var:str, split_with:str=' '):
            """Split a string and then join it back together"""
            return join_with.join(var.split(split_with))
        
        # Check input values
        join_with = self._check_input_val(join_with, self._join_with)
        remove_empty = self._check_input_val(remove_empty, self._remove_empty)
        dir_end = self._check_input_val(dir_end, self._dir_end)
        do_print = self._check_input_val(do_print, self.do_print)

        fprint.config(do_print=do_print)

        # Iterate through args and join them together
        new_args = []
        for arg_indx, arg in enumerate(args):
            # Remove invalid characters
            arg = split_join(split_join(arg, '\\'), '/')
            arg = arg.translate({ord(c): None for c in '<>"|?*'}) # ":" is an invalid character on Windows, but drivers can use it. E.g. "C:\"

            # Remove empty strings
            split_arg = arg.split('/')
            if '' in split_arg and remove_empty:
                fprint(f'Empty string found in input arg (indx: {arg_indx}): {arg!r}')
                split_arg = [x for x in split_arg if x != '']
                arg = join_with.join(split_arg)
                if arg == '':
                    continue

            new_args.append(arg)

        # Join the path segments together
        out_path = join_with.join(new_args)

        # Add join_with character at the end of the path if dir_end is True
        if dir_end:
            out_path += join_with

        return out_path


join_path = JoinPath()


if __name__ == '__main__':
    # Code testing
    from FastDebugger import fd

    p = join_path('Folder/subotex/.txt', 'Users', 'Documents', 'file.txt', do_print=True)

    fd(p)