

from py_basic_commands.json_scripts import read_json, write_json
from py_basic_commands.base import EditorBase

from send2trash import send2trash
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


    def __setitem__(self, keypath:str, data:Any):
        """Adds data to the json file. If the data already exists, it will be overwritten
        
        Parameters
        ----------
        keypath : str
            The key to add the data to
        data : Any
            The data to add"""
        self.b_json_data[keypath] = data


    def __getitem__(self, keypath:Any) -> Any:
        """Returns the data from the json file
        
        Parameters
        ----------
        keys : Any
            The key to get"""
        try:
            return self.b_json_data[keypath]
        except KeyError:
            return ''


    def __delitem__(self, keys:str):
        """Deletes the data from the json file
        
        Parameters
        ----------
        keys : str
            The key to delete"""
        del self.b_json_data[keys]


    def __contains__(self, keys:str) -> bool:
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
        
    
    def __len__(self) -> int:
        """Returns the number of keys in the json file
        
        Returns
        -------
        int
            The number of keys in the json file"""
        return len(self.b_json_data)
    

    def __iter__(self):
        """Returns an iterator for the json file with the key and value"""
        for key, value in self.b_json_data.items():
            yield key, value

    
    def new_dict(self, new_dict:dict):
        """Updates the json file with a new dict
        
        Parameters
        ----------
        new_dict : dict
            The new dict to update the json file with"""
        self.b_json_data = benedict(new_dict, keypath_separator="/")


    def new_file(self, file_path:str):
        """Updates the json file path and reads the json file
        
        Parameters
        ----------
        file_path : str
            The path to the json file"""
        self.file_path = file_path
        self.new_dict(read_json(self.file_path))


    def remove_file(self):
        """Removes the json file"""
        send2trash(self.file_path)


    def append(self, keypath:str, data) -> str:
        """Appends data to the json file.
        
        Parameters
        ----------
        keys : str
            The key to add the data to
        data : Any
            The data to add
        
        Returns
        -------
        str
            The path to the data
        """
        if not self.does_key_exists(keypath):
            self[keypath] = [data]
        else:
            self[keypath].append(data)

        return f'{keypath}[{len(self[keypath])-1}]'


    def does_key_exists(self, keypath:str) -> bool:
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
            self.b_json_data[keypath]
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
        

    def remove_path(self, path:str):
        """Removes a path from the json file

        WARNING: This will remove all data after the path as well
        
        Parameters
        ----------
        path : str
            The path to remove"""
        self.b_json_data.remove(path)


    def remove_empty_values(self, empty_values:list[Any]=['', None, {}, []]):
        """Removes all empty values from the json file.
         Also removes the keys that contain the empty values.

        Parameters
        ----------
        empty_values : list[Any], optional
            The values to remove, by default ['', None, {}, []]
        """
        def remove_falsy_recursive(obj):
            """Recursively remove all falsy values from a nested dict/list."""
            if isinstance(obj, dict):
                return {k: remove_falsy_recursive(v) for k, v in obj.items() if v not in empty_values}
            if isinstance(obj, list):
                return [remove_falsy_recursive(i) for i in obj if i]
            return obj
        
        self.new_dict(remove_falsy_recursive(self.b_json_data.dict()))


    def remove_duplicates(self, value:Any, master_keypath:str=''):
        """Remove all duplicates from the given value. Only keep the value on the master keypath.
        
        If no master keypath is given, the first item will be saved
        
        May leave empty lists and dicts behind
        To remove these, use remove_empty_values()
        
        Parameters
        ----------
        value : Any
            The value to remove duplicates from.
        master_keypath : str
            The keypath to the value that should be kept.
        """
        path_lst = self.find_value_path_all(value)

        if len(path_lst) <= 1:
            print('No duplicates')
            return
        else:
            print(f'{len(path_lst)} duplicates found')

        if not master_keypath:
            for path in path_lst[1:][::-1]:
                self.remove_path(path)
            return
        
        if master_keypath not in path_lst:
            raise Exception(f'Master keypath {master_keypath} not in path list')

        for path in path_lst[::-1]:
            if path != master_keypath:
                self.remove_path(path)