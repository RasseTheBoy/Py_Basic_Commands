from py_basic_commands.file_dir_scripts import get_src_path

# Only used for inheritance
class Base:
    """Base class for all classes"""
    def __init__(self, do_print=True) -> None:
        """Initialize the class
        
        Parameters
        ----------
        do_print : bool, optional
            Whether to print information about the file editing process. Default is True"""
        self.do_print=do_print

    
    def config(self, **kwargs):
        """Configure variables
        
        Parameters
        ----------
        **kwargs : Any
            The variables to configure
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# Only used for inheritance
class EditorBase(Base):
    """Base class for all file editors"""
    def __init__(self, file_path:str, do_print=True) -> None:
        """Initialize the class
        
        Parameters
        ----------
        file_path : str
            The path to the file to edit
        do_print : bool, optional
            Whether to print information about the file editing process. Default is True"""
        super().__init__(do_print)

        self.file_path = file_path


    def get_file_path(self) -> str:
        """Get the file path
        
        Returns
        -------
        str
            The file path"""
        return self.file_path


    def get_file_name(self) -> str:
        """Get the file name
        
        Returns
        -------
        str
            The file name"""
        return get_src_path(self.file_path, ret_val='f')
    

    def get_dir_path(self) -> str:
        """Get the directory path
        
        Returns
        -------
        str
            The directory path"""
        return get_src_path(self.file_path, ret_val='d')


    def __enter__(self):
        """Enter the context manager"""
        return self
