from dataclasses    import dataclass
from functools  import wraps
from py_basic_commands.fscripts   import fprint
from py_basic_commands.base   import Base
from time   import perf_counter


@dataclass
class FunctionTimer(Base):
    _ret_time:bool = False
    _skip_intro:bool = True
    _skip_inputs:bool = True    
    
    def __post_init__(self) -> None:
        super().__init__()


    # TODO: Add self.do_print to function
    def _func_timer(self, do_print:bool=True, ret_time:bool=False, skip_intro:bool=True, skip_inputs:bool=True):
        def timer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                fprint(f'Function timer started: {self._get_func_name(func)}', do_print=not skip_intro and do_print)
                
                time_start = perf_counter()
                ret_val = func(*args, **kwargs)
                time_delta = perf_counter() - time_start

                self._print_time(func, time_delta, skip_inputs, do_print, *args, **kwargs)

                if ret_time:
                    return ret_val, time_delta
                return ret_val
            return wrapper
        
        # Check input values
        do_print = self._check_input_val(do_print, self._do_print)
        ret_time = self._check_input_val(ret_time, self._ret_time)
        skip_intro = self._check_input_val(skip_intro, self._skip_intro)
        skip_inputs = self._check_input_val(skip_inputs, self._skip_inputs)

        return timer
    

    def __call__(self, func, *args, **kwargs):
        fprint(f'Function timer started: {self._get_func_name(func)}', do_print=not self._skip_intro and self.do_print)
        
        time_start = perf_counter()
        ret_val = func(*args, **kwargs)
        time_delta = perf_counter() - time_start
        
        self._print_time(func, time_delta, self.skip_inputs, self.do_print, *args, **kwargs)

        if self.ret_time:
            return ret_val, time_delta
        return ret_val


    def _get_func_name(self, func):
        try:
            return func.__name__
        except Exception:
            try:
                return func.__class__.__name__
            except Exception:
                return ''
        

    def _print_time(self, func, time_delta:float, skip_inputs:bool, do_print:bool, *args, **kwargs):
        if not do_print:
            return

        func_name = self._get_func_name(func)
        if round(time_delta, 4) == 0.0:
            time_delta = '0.0000...'
        else:
            time_delta = round(time_delta, 4)

        if skip_inputs:
            fprint(f'Function {func_name} Took {time_delta} seconds to run')
        else:
            fprint(f'Function {func_name} {args}{kwargs} Took {time_delta} seconds to run')


_func_timer = FunctionTimer()._func_timer
func_timer = FunctionTimer()