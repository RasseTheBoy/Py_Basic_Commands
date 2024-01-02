
from py_basic_commands.file_dir_scripts import read_file, write_file
from py_basic_commands.fscripts import Fprint
from py_basic_commands.base  import EditorBase

from send2trash import send2trash
from typing import Any

fprint = Fprint()


class FileEditor(EditorBase):
    """An easy and safe way to edit and view files.
    Combines the functionality of `read_file` and `write_file` into one class."""
    def __init__(self, file_path:str, exit_write:bool=True, do_print:bool=True, **kwargs):
        """Initialize the class

        Parameters
        ----------
        file_path : str
            The path to the file to edit
        exit_write : bool, optional
            Whether to write the file when exiting the context manager. Default is True
        do_print : bool, optional
            Whether to print information about the file editing process. Default is True
        
        read_file Parameters
        --------------------
        create : bool, optional
            Whether to create the file if it does not exist. Default is False
        ret_did_create : bool, optional
            Whether to return whether the file was created. Default is False
        splitlines : bool, optional
            Whether to split the file contents by line. Default is True
        remove_empty : bool, optional
            Whether to remove empty lines from the file contents; only works if `splitlines` is True. Default is True
        do_strip : bool, optional
            Whether to strip the file contents of whitespace; only works if `splitlines` is True. Default is True
        do_lower : bool, optional
            Whether to convert the file contents to lowercase. Default is False
        encoding : str, optional
            The encoding to use when reading the file. Default is 'utf-8'
        
            
        write_file Parameters
        ---------------------
        append : bool, optional
            Whether to append the text to the file. Default is False
        force_create : bool, optional
            Whether to force the creation of the file. Default is True
        remove_duplicates : bool, optional
            Whether to remove duplicate lines from the text. Default is False
        encoding : str, optional
            The encoding to use when writing to the file. Default is 'utf-8'           
        """
        super().__init__(file_path, do_print)

        self.exit_write = exit_write
        
        fprint.config(do_print=do_print)
        read_file.config(do_print=do_print, **kwargs)
        write_file.config(do_print=do_print, **kwargs)

        self._read_file()
    

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Write the file"""
        if self.exit_write:
            write_file(self.text, self.file_path)


    def __str__(self):
        """Return the file path"""
        return self.text


    def __repr__(self):
        """Return the file path"""
        return self.text


    def __setitem__(self, key, value):
        """Set the file contents"""
        self.text_lst[key] = value
        self.text = '\n'.join(self.text_lst)


    def __getitem__(self, key):
        """Get the file contents"""
        return self.text_lst[key]
    

    def __delitem__(self, key):
        """Delete the given item from the file"""
        del self.text_lst[key]
        self.text = '\n'.join(self.text_lst)


    def __list__(self):
        """Get the file contents as a list"""
        return self.text_lst


    def __len__(self):
        """Get the length of the file"""
        return len(self.text_lst)
    

    def __iter__(self):
        """Iterate over the file"""
        return iter(self.text_lst)
    

    def __contains__(self, item):
        """Check if the file contains the given item"""
        return item in self.text_lst


    def new_file(self, file_path:str):
        """Update the file path and read the file contents
        
        Parameters
        ----------
        file_path : str
            The path to the file
        """
        self.file_path = file_path
        self._read_file()


    def _read_file(self):
        """Read the file contents"""
        self.text_lst = read_file(self.file_path)
        self.text = '\n'.join(self.text_lst)

    
    def get_text(self, splitlines:bool=True):
        """Read the file
        
        Parameters
        ----------
        splitlines : bool, optional
            Whether to split the file contents by line. Default is True
        """
        if splitlines:
            return self.text_lst
        else:
            return self.text
        

    def update_write(self):
        """Writes self.text to the file"""
        write_file(self.text, self.file_path)


    def overwrite(self, text:str|list):
        """Overwrite the file contents
        
        Parameters
        ----------
        text : str or list
            The text to overwrite the file with

        Raises
        ------
        TypeError
            If the given type is not str or list
        """
        if isinstance(text, str):
            self.text = text
            self.text_lst = text.split('\n')
        elif isinstance(text, list):
            self.text_lst = text
            self.text = '\n'.join(text)
        else:
            raise TypeError(f'Invalid type given: {type(text)}')
        
        fprint('Text overwritten')


    def append(self, text:str|list):
        """Append text to the file
        
        Parameters
        ----------
        text : str
            The text to append to the file
        """
        if isinstance(text, str):
            self.text += f'\n{text}'
            self.text_lst.append(text)
        
        elif isinstance(text, list):
            self.text += '\n' + '\n'.join(text)
            self.text_lst += text


    def remove_file(self):
        """Removes the file"""
        send2trash(self.file_path)
        fprint(f'File removed: {self.file_path}')


    def find_index_all(self, val:Any, exact:bool=False):
        """Find all occurances of the given value
        
        Parameters
        ----------
        val : Any
            The value to find
        exact : bool, optional
            Whether to only find exact matches. Default is False
        
        Returns
        -------
        list
            A list of the indices of the occurances of the given value  
        """
        return [i for i, line in enumerate(self) if (exact and (val == line)) or (not exact and (val in line))]


    def find_index(self, val:Any, exact:bool=False):
        """Find the first occurance of the given value
        
        Parameters
        ----------
        val : Any
            The value to find
        exact : bool, optional
            Whether to only find exact matches. Default is False
            
        Returns
        -------
        int
            The index of the first occurance of the given value
        """
        for i, line in enumerate(self):
            if (exact and (val == line)) or (not exact and (val in line)):
                return i
            

    def remove_all_occurance(self, val:Any, exact:bool=False):
        """Remove all occurances of the given value
        
        Parameters
        ----------
        val : Any
            The value to remove
        exact : bool, optional
            Whether to only remove exact matches. Default is False
        
        Returns
        -------
        bool
            Whether the value was removed
        """
        removed = False
        for i, line in enumerate(self):
            if (exact and (val == line)) or (not exact and (val in line)):
                del self[i]
                removed = True

        return removed



if __name__ == '__main__':
    with FileEditor('test.txt', create=True) as f:
        text = ['hello', 'world', 'how', 'are', 'you', 'doing', 'today']
        f.append(text)
        print(f.get_text())