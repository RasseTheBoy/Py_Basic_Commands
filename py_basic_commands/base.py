# Only used for inheritance

class Base:
    """Base class for all classes"""
    def __init__(self, do_print=True) -> None:
        self.do_print=do_print

    
    def config(self, **kwargs):
        """Configure variables"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                print(f'Changed {key} to {value}')
            else:
                raise AttributeError(f'{self.__class__.__name__} has no attribute {key}')
        

    def _check_input_val(self, inpt_val, saved_val):
        """Check if input value is None, if so return saved value"""
        return saved_val if inpt_val == None else inpt_val
