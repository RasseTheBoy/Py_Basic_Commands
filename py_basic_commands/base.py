# Only used for inheritance

class Base:
    """Base class for all classes"""
    def __init__(self, do_print=True) -> None:
        self._do_print=do_print

    def _config(self, **kwargs):
        """Configure variables"""
        if 'do_print' in kwargs:
            self._do_print = kwargs['do_print']

    def _check_input_val(self, inpt_val, saved_val):
        """Check if input value is None, if so return saved value"""
        return saved_val if inpt_val == None else inpt_val
