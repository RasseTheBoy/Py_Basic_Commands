

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


    def __getitem__(self, keys:Any) -> Any:
        """Returns the data from the json file
        
        Parameters
        ----------
        keys : Any
            The key to get"""
        try:
            return self.b_json_data[keys]
        except KeyError:
            return None


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


    def find_value_path(self, value:Any, key:Optional[Any]=None) -> Optional[str]:
        """Finds the first path to a value in the json file
        
        Parameters
        ----------
        find_value : Any
            The value to search for
        key : Optional[Any], optional
            The key to search for the value in, by default None
        
        Returns
        -------
        str or None
            The path to the value if found, None if not found
        """
        if not self.does_value_exists(value):
            return None
        
        for keypath in self.b_json_data.keypaths(value):
            if value == self.b_json_data[keypath]:
                if key:
                    if key == keypath.split('/')[-1]:
                        return keypath
                else:
                    return keypath
            

    def find_value_path_all(self, value:Any, key:Optional[Any]=None) -> list[str]:
        """Finds all the paths to a value in the json file
        
        Parameters
        ----------
        find_value : Any
            The value to search for
        key : Optional[Any], optional
            The key to search for the value in, by default None
            
        Returns
        -------
        list[str]
            The paths to the value if found, an empty list if not found
        """
        paths = []
        if not self.does_value_exists(value):
            return paths
        
        for keypath in self.b_json_data.keypaths(value):
            if value == self.b_json_data[keypath]:
                if key:
                    if key == keypath.split('/')[-1]:
                        paths.append(keypath)
                else:
                    paths.append(keypath)

        return paths
            

    def count_occurance(self, value:Any, key:Optional[Any]=None) -> int:
        """Count the number of times a value occurs in the json file

        Parameters
        ----------
        value : Any
            The value to count
        key : Optional[Any], optional
            The key to search for the value in, by default None
        
        Returns
        -------
        int
            The number of times the value occurs"""
        if not key:
            return len(self.b_json_data.search(value))
    
        else:
            return len([values[1] for values in self.b_json_data.search(value) if values[1] == key])