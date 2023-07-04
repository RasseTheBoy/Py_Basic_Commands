

from py_basic_commands.json_scripts import read_json, write_json
from py_basic_commands.base import EditorBase
from benedict import benedict
from typing import Any, Optional


class JsonEditor(EditorBase):
    """A class to read, edit and write json files"""
    def __init__(self, file_path:str, exit_write:bool=True, do_print:bool=False) -> None:
        """Initialize the class
        
        Parameters
        ----------
        file_path : str
            The path to the json file
        exit_write : bool, optional
            If True, the json file will be written to when the class is exited, by default True
        do_print : bool, optional
            If True, print statements will be printed, by default False"""
        super().__init__(file_path, do_print)
        self.exit_write = exit_write
        self.new_file(file_path)

        read_json.config(do_print=do_print)
        write_json.config(do_print=do_print)


    def __exit__(self, exc_type, exc_value, traceback):
        """Write the json file"""
        if self.exit_write:
            write_json(self.b_json_data, self.file_path, force=True)


    def __call__(self) -> benedict:
        """Returns the json data"""
        return self.b_json_data


    def __setitem__(self, keys:str, data):
        """Adds data to the json file. If the data already exists, it will be overwritten
        
        Parameters
        ----------
        keys : str
            The key to add the data to
        data : Any
            The data to add"""
        self.b_json_data[keys] = data


    def __getitem__(self, keys:Any):
        """Returns the data from the json file
        
        Parameters
        ----------
        keys : Any
            The key to get"""
        return self.b_json_data[keys]


    def __delitem__(self, keys:str):
        """Deletes the data from the json file
        
        Parameters
        ----------
        keys : str
            The key to delete"""
        del self.b_json_data[keys]


    def new_file(self, file_path:str):
        """Updates the json file path and reads the json file
        
        Parameters
        ----------
        file_path : str
            The path to the json file"""
        self.file_path = file_path
        self.b_json_data = benedict(read_json(self.file_path), keypath_separator="/")


    def add_data(self, keys:str, data):
        """Adds data to the json file. If the data already exists, it will be overwritten"""
        self.b_json_data[keys] = data


    def does_key_exists(self, keys:str) -> bool:
        """Checks if a key is in the json file

        Parameters
        ----------
        keys : str
            The key to check for
        
        Returns
        -------
        bool
            True if the key is in the json file, False if not"""
        
        try:
            self.b_json_data[keys]
            return True
        
        except KeyError:
            return False


    def does_value_exists(self, value:Any) -> bool:
        """Checks if a value is in the json file

        Parameters
        ----------
        value : Any
            The value to check for
        
        Returns
        -------
        bool
            True if the value is in the json file, False if not"""
        
        ret = self.b_json_data.search(value)

        if len(ret) == 0:
            return False
        else:
            return True


    def find_value_path(self, find_value:str, separator:str='/', path:Optional[str] = None) -> Optional[str]:
        """Iterate through the json file and find the path to a value.
        When a list is encountered, the index of the list is added to the path as: {key}[{list index}].

        Return the path as a string.
        If value is not found, return None
        
        Parameters
        ----------
        find_value : str
            The value to search for
        separator : str, optional
            The separator to use when returning the path, by default '/'
        path : [type], optional
            The path to the value, by default None
        
        Returns
        -------
        str or None
            The path to the value if found, None if not found"""

        def _search_json(json_data:dict, find_value:str, separator:str='.', path = None) -> Optional[str]:
            """Iterate through the json file and find the path to a value."""
            for key, val in json_data.items():
                if isinstance(val, dict):
                    path = _search_json(val, find_value, separator, path)
                    if path:
                        path = key + separator + path
                        return path
                elif isinstance(val, list):
                    for index, item in enumerate(val):
                        path = _search_json(item, find_value, separator, path)
                        if path:
                            path = f'{key}[{index}]' + separator + path
                            return path
                else:
                    if val == find_value:
                        path = key
                        return path

        return _search_json(self.b_json_data, find_value, separator, path)


