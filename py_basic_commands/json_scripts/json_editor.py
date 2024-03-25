from py_basic_commands.json_scripts import ReadJson, WriteJson
from py_basic_commands.base import EditorBase
from py_basic_commands.fscripts import Fprint

from send2trash import send2trash
from benedict import benedict
from typing import Any, Optional, Sequence


read_json = ReadJson(do_print=False)
write_json = WriteJson(do_print=False)
fprint = Fprint(do_print=False)


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
        fprint.config(do_print=do_print)


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
            The key to get
            
        Returns
        -------
        Any
            The data from the json file
        """
        try:
            return self.b_json_data[keypath]
        except KeyError:
            return None


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


    def keys(self) -> Any:
        """Returns all the keys in the json file
        
        Returns
        -------
        list[str]
            All the keys in the json file"""
        return self.b_json_data.keys()
    

    def values(self) -> Any:
        """Returns all the values in the json file
        
        Returns
        -------
        list[Any]
            All the values in the json file"""
        return self.b_json_data.values()
    

    def items(self) -> Any:
        """Returns all the items in the json file
        
        Returns
        -------
        list[tuple[str, Any]]
            All the items in the json file"""
        return self.b_json_data.items()

    
    def new_dict(self, new_dict:dict[Any, Any]):
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


    def save_file(self):
        """Writes the json file"""
        write_json(self.b_json_data, self.file_path, force=True)


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


    def keypaths(self, with_indexes:bool=True) -> list[str]:
        """Returns all the keypaths in the json file

        Returns
        -------
        list[str]
            All the keypaths in the json file
        """
        return self.b_json_data.keypaths(with_indexes)


    def does_value_exists(self, value:Any, keypath:Optional[str]=None) -> bool:
        """Checks if a value is in the json file

        Parameters
        ----------
        value : Any
            The value to check for
        keypath : Optional[str], optional
            The keypath to check for the value in, by default None
        
        Returns
        -------
        bool
            True if the value is in the json file, False if not"""
        if len(self.find_value_path_all(value, keypath)) == 0:
            return False
        else:
            return True
        

    def does_key_exists(self, key:str) -> bool:
        """Checks if a key or keypath is in the json file

        Parameters
        ----------
        key : str
            The key to check for
        
        Returns
        -------
        bool
            True if the key is in the json file, False if not"""
        for keypath in self.keypaths(False):
            if keypath.split('/')[-1] == key:
                return True
        return False
        

    def _yield_keypaths(self, value, search_key:Optional[str]=None, remove_last_key:bool=False):
        """Yields all the keypaths that contain the value
        
        Parameters
        ----------
        value : Any
            The value to search for
        search_key : Optional[str], optional
            The key to search for the value in, by default None
        remove_last_key : bool, optional
            If True, removes the last key from the keypath, by default False
            
        Yields
        ------
        str
            The keypath that contains the value"""
        def check_keypath_value(keypath_value:Any) -> bool:
            """Checks if the keypath value is equal to the value

            Parameters
            ----------
            keypath_value : Any
                The value to check

            Returns
            -------
            bool
                True if the value is equal to the keypath value, False if not
            """
            if isinstance(value, str):
                return value == keypath_value
            
            elif isinstance(value, dict):
                return value in keypath_value.values()

            elif isinstance(value, Sequence):
                return keypath_value in value
            
            else:
                return value == keypath_value


        def _remove_last_key(keypath:str) -> str:
            """Removes the last key from the keypath

            Parameters
            ----------
            keypath : str
                The keypath to remove the last key from

            Returns
            -------
            str
                The keypath with the last key removed
            """
            for i in range(len(keypath) - 1, 0, -1):
                if keypath[i] == '/' or keypath[i] == '[':
                    return keypath[:i]
            return ''


        for keypath in self.keypaths():
            if not check_keypath_value(self[keypath]) or (search_key and search_key not in keypath):
                continue

            if remove_last_key:
                yield _remove_last_key(keypath)
            else:
                yield keypath


    def find_value_path(self, value:Any, key:Optional[Any]=None, remove_last_key:bool=False) -> str:
        """Finds the first path to a value in the json file
        
        Parameters
        ----------
        find_value : Any
            The value to search for
        key : Optional[Any], optional
            The key to search for the value in, by default None
        remove_last_key : bool, optional
            If True, removes the last key from the keypath, by default False
        
        Returns
        -------
        str
            The path to the value if found, an empty string if not found
        """
        try:
            return self.find_value_path_all(value, key, remove_last_key)[0]
        except IndexError:
            return ''
            

    def find_value_path_all(self, value:Any, key:Optional[Any]=None, remove_last_key:bool=False) -> list[str]:
        """Finds all the paths to a value in the json file
        
        Parameters
        ----------
        find_value : Any
            The value to search for
        key : Optional[Any], optional
            The key to search for the value in, by default None
        remove_last_key : bool, optional
            If True, removes the last key from the keypath, by default False
            
        Returns
        -------
        list[str]
            The paths to the value if found, an empty list if not found
        """
        return [keypath for keypath in self._yield_keypaths(value, key, remove_last_key)]
            

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

    
    def remove_all_occurance(self, value:Any, keypath:Optional[str]=None) -> int:
        """Removes all occurances of a value in the json file
        
        Parameters
        ----------
        value : Any
            The value to remove
        keypath : Optional[str], optional
            The keypath to remove the value from, by default None
        
        Returns
        -------
        int
            The number of times the value was removed
        """
        removed_amnt = 0
        for path in self.find_value_path_all(value, keypath):
            self.remove_path(path)
            removed_amnt += 1

        return removed_amnt


    def remove_empty_values(self, master_keypath:str='', empty_values:list[Any]=[None, {}, []]):
        """Removes all empty values from the json file.
         Also removes the keys that contain the empty values.

        Parameters
        ----------
        master_keypath : str, optional
            The keypath to the value that should be removed in, by default ''
        empty_values : list[Any], optional
            The values to remove, by default None, {}, []]
        """
        for keypath in self.keypaths():
            keypath_value = self[keypath]

            if master_keypath != '' and master_keypath not in keypath:
                continue

            if keypath_value in empty_values:
                self.remove_path(keypath)


    def remove_duplicates(self, value:Any, master_keypath:str='', only_in_key:str='') -> int:
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

        Returns
        -------
        int
            The amount of duplicates removed
        
        Raises
        ------
        Exception
            If the master keypath is not in the path list
        """
        path_lst = self.find_value_path_all(value)
        removed_amnt = 0

        if len(path_lst) <= 1:
            # print('No duplicates')
            return removed_amnt
        # else:
        #     print(f'{len(path_lst)} duplicates found')

        if only_in_key:
            path_lst = [path for path in path_lst if only_in_key in path]

        # If no master keypath is given, keep the first item
        if not master_keypath:
            for path in path_lst[1:][::-1]:
                self.remove_path(path)
                removed_amnt += 1
            return removed_amnt
        
        # If master keypath is given, but not in path list, raise error
        if master_keypath not in path_lst:
            raise Exception(f'Master keypath {master_keypath} not in path list')

        # Remove all duplicates
        for path in path_lst[::-1]:
            if path != master_keypath:
                self.remove_path(path)
                removed_amnt += 1

        return removed_amnt