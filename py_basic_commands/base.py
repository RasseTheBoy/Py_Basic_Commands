# Only used for inheritance


class Base:
    """Base class for all classes"""
    def __init__(self, do_print=True) -> None:
        self._do_print=do_print

<<<<<<< Updated upstream
    def _config(self, **kwargs):
        """Configure variables"""
        if 'do_print' in kwargs:
            self._do_print = kwargs['do_print']
=======
    
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
       
>>>>>>> Stashed changes

    def _check_input_val(self, inpt_val, saved_val):
        """Check if input value is None, if so return saved value
        
        Parameters
        ----------
        inpt_val : Any
            The input value to check
        saved_val : Any
            The saved value to return if the input value is None
        """
        return saved_val if inpt_val == None else inpt_val


class EditorBase(Base):
    def __init__(self, file_path:str, do_print=True) -> None:
        super().__init__(do_print)

        self.file_path = file_path

    def __enter__(self):
        return self
