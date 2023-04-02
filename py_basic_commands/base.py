



class Base:
    def __init__(self) -> None:
        self.do_print=True

    def _config(self, **kwargs):
        if 'do_print' in kwargs:
            self.do_print = kwargs['do_print']

    def _check_input_val(self, inpt_val, saved_val):
        return saved_val if inpt_val == None else inpt_val