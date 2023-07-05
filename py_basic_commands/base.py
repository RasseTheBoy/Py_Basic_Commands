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

    def __enter__(self):
        """Enter the context manager"""
        return self
