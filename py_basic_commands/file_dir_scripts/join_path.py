from dataclasses    import dataclass
from py_basic_commands.fscripts   import Fprint
from os.path    import dirname, basename, splitext
from py_basic_commands.base   import Base
from typing import Any

fprint = Fprint()

@dataclass
class JoinPath(Base):
    join_with:str = '/'
    remove_empty:bool = True
    dir_end:bool = False
    do_print:bool = False

    def __post_init__(self):
        super().__init__(self.do_print)


    def __call__(self, *args:Any, **kwargs) -> str:
        r"""Join path segments together, removing certain characters (`<>:"/\|?*`) and adjust for correct slash direction.

        Parameters
        ----------
        *args : Any
            The path segments to join together. If a list is given, the values will be joined by the `join_with` character
        join_with : str, optional
            The character to use to join the path segments together. Default is '/'
        remove_empty : bool, optional
            Whether to remove empty strings from the path segments. Default is True
        dir_end : bool, optional
            Whether to add the `join_with` character at the end of the path. Default is False
        do_print : bool, optional
            Whether to print information about the file creation process. Default is True
        
        Returns
        -------
        str
            The joined path
        """

        def split_join(var:str, split_with:str=' '):
            """Split a string and then join it back together"""
            return join_with.join(var.split(split_with))
        
        # Check input values
        join_with = kwargs.get('join_with', self.join_with)
        remove_empty = kwargs.get('remove_empty', self.remove_empty)
        dir_end = kwargs.get('dir_end', self.dir_end)
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)

        # Iterate through args and join them together
        new_args = []
        for arg_indx, arg in enumerate(args):
            # Remove invalid characters
            arg = split_join(split_join(arg, '\\'), '/')

            # Check if the start of the path is a drive letter
            if arg_indx == 0 and arg[1] == ':':
                _driver = True
            else:
                _driver = False

            # Remove invalid characters
            arg = arg.translate({ord(c): None for c in '<>:"|?*'})

            # Add drive letter back
            if _driver:
                arg = arg[0] + ':' + arg[1:]

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