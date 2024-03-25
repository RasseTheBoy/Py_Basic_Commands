from py_basic_commands.fscripts   import Fprint
from py_basic_commands.base   import Base
from dataclasses    import dataclass
from functools  import wraps
from time   import perf_counter

fprint = Fprint()


@dataclass
class FunctionTimer(Base):
    """A class for timing functions
    
    Attributes
    ----------
    ret_time : bool, optional
        Whether to return the time taken to run the function. Default is False
    skip_intro : bool, optional
        Whether to skip the intro message. Default is True
    skip_inputs : bool, optional
        Whether to skip printing the inputs. Default is True
    do_print : bool, optional
        Whether to print information about the timer starting process. Default is True
    """
    ret_time:bool = False
    skip_intro:bool = True
    skip_inputs:bool = True
    do_print:bool = True
    
    def __post_init__(self) -> None:
        super().__init__(self.do_print)


    def _func_timer(self, **kwargs):
        """A decorator for timing functions
        
        Parameters
        ----------
        ret_time : bool, optional
            Whether to return the time taken to run the function. Default is False
        skip_intro : bool, optional
            Whether to skip the intro message. Default is True
        skip_inputs : bool, optional
            Whether to skip printing the inputs. Default is True
        do_print : bool, optional
            Whether to print information about the timer starting process. Default is True"""
        def timer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                fprint(f'Function timer started: {self._get_func_name(func)}', do_print=not skip_intro and do_print)
                
                time_start = perf_counter() # Timer start
                ret_val = func(*args, **kwargs) # Function call
                time_delta = perf_counter() - time_start # Timer end

                self._print_time(func, time_delta, skip_inputs, do_print, *args, **kwargs)

                if ret_time:
                    return ret_val, time_delta
                return ret_val
            return wrapper
        
        # Check input values
        ret_time = kwargs.get('ret_time', self.ret_time)
        skip_intro = kwargs.get('skip_intro', self.skip_intro)
        skip_inputs = kwargs.get('skip_inputs', self.skip_inputs)
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)

        return timer
    

    def __call__(self, func, *args, **kwargs):
        """Time a function
        
        Parameters
        ----------
        func : function
            The function to be timed
        ret_time : bool, optional
            Whether to return the time taken to run the function. Default is False
        skip_intro : bool, optional
            Whether to skip the intro message. Default is True
        skip_inputs : bool, optional
            Whether to skip printing the inputs. Default is True
        do_print : bool, optional
        
        Returns
        -------
        Any
            The return value of the function or a tuple of the return value and the time taken to run the function"""
        
        ret_time = kwargs.get('ret_time', self.ret_time)
        skip_intro = kwargs.get('skip_intro', self.skip_intro)
        skip_inputs = kwargs.get('skip_inputs', self.skip_inputs)
        do_print = kwargs.get('do_print', self.do_print)

        fprint.config(do_print=do_print)    

        fprint(f'Function timer started: {self._get_func_name(func)}', do_print=not skip_intro and do_print)
        
        time_start = perf_counter()
        ret_val = func(*args, **kwargs)
        time_delta = perf_counter() - time_start
        
        self._print_time(func, time_delta, skip_inputs, do_print, *args, **kwargs)

        if ret_time:
            return ret_val, time_delta
        return ret_val


    def _get_func_name(self, func) -> str:
        """Get the name of the function

        Parameters
        ----------
        func : function
            The function whose name is to be returned
        
        Returns
        -------
        str
            The name of the function"""
        try:
            return func.__name__
        except Exception:
            try:
                return func.__class__.__name__
            except Exception:
                return ''
        

    def _print_time(self, func, time_delta:float, skip_inputs:bool, do_print:bool, *args, **kwargs):
        """Print the time taken to run the function
        
        Parameters
        ----------
        func : function
            The function that was timed
        time_delta : float
            The time taken to run the function
        skip_inputs : bool
            Whether to skip printing the inputs
        do_print : bool
            Whether to print information about the timer starting process    
        """
        if not do_print:
            return

        func_name = self._get_func_name(func)
        if round(time_delta, 4) == 0.0:
            time_delta = '0.0000...' # type: ignore
        else:
            time_delta = round(time_delta, 4)

        if skip_inputs:
            fprint(f'Function {func_name} Took {time_delta} seconds to run')
        else:
            fprint(f'Function {func_name} {args}{kwargs} Took {time_delta} seconds to run')


_func_timer = FunctionTimer()._func_timer
func_timer = FunctionTimer()