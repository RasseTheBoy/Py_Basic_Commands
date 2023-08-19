from py_basic_commands.fscripts import Fprint
from py_basic_commands.base     import Base
from time   import perf_counter

fprint = Fprint()
    

class Timer(Base):
    """A timer class that can be used as a context manager or as a normal class."""
    def __init__(self, timer_name:str='Timer', do_print:bool=True):
        """Initializes the timer class.
        
        Parameters
        ----------
        timer_name : str, optional
            The name of the timer, by default 'Timer'
        do_print : bool, optional
            Whether to print the timer messages, by default True"""
        super().__init__(do_print)

        fprint.config(do_print=do_print)

        self.timer_name = timer_name
        self.start_time = 0.0

    
    def start(self) -> None:
        """Starts the timer."""
        self.start_time = perf_counter()
        fprint(f'Timer started: {self.timer_name!r}', do_print=self.do_print)


    def stop(self) -> float:
        """Stops the timer and returns the time elapsed since the timer was started.
        
        Returns
        -------
        float
            The time elapsed since the timer was started."""
        delta_time = perf_counter() - self.start_time

        if delta_time < 0.0001:
            delta_time_prnt = '0.0000...'
        else:
            delta_time_prnt = round(delta_time, 4)

        fprint(f'Timer stopped {self.timer_name!r} --> {delta_time_prnt} seconds')

        return delta_time
    

    def reset(self):
        """Resets the timer."""
        self.start_time = perf_counter()
        fprint(f'Timer reset: {self.timer_name!r}')

    
    def __enter__(self):
        """Starts the timer and stops it when the context manager is exited."""
        self.start()
        return self
    

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Stops the timer when the context manager is exited."""
        self.stop()


timer = Timer()