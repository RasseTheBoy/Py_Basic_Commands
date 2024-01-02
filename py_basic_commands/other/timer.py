from py_basic_commands.fscripts import Fprint
from py_basic_commands.base     import Base
from time   import perf_counter

fprint = Fprint()


class Timer(Base):
    """A class for timing processes"""
    def __init__(self, do_print:bool=True) -> None:
        """Initialize the class
        
        Parameters
        ----------
        do_print : bool, optional
            Whether to print information about the timer starting process. Default is True"""
        super().__init__(do_print)

        self.timer_lst:dict[str,float] = {}


    def start_timer(self, timer_name:str, **kwargs) -> bool:
        """Start a timer with a specified name
        
        Parameters
        ----------
        timer_name : str
            The name of the timer
        do_print : bool, optional
            Whether to print information about the timer starting process. Default is True
            
        Returns
        -------
        bool
            Whether the timer was started"""

        # Chek values
        do_print = kwargs.get('do_print', self.do_print)

        if self.timer_lst.get(timer_name):
            print(f'Timer with name already started: {timer_name}')
            return False

        self.timer_lst[timer_name] = perf_counter()
        fprint(f'Timer started: {timer_name}', do_print=do_print)

        return True


    def end_timer(self, timer_name:str) -> float:
        """End timer with given name
        
        Parameters
        ----------
        timer_name : str
            The name of the timer
        
        Returns
        -------
        float
            The time in seconds that the timer ran for"""

        if not self.timer_lst.get(timer_name):
            print(f'No timer found with name: {timer_name}')
            return 0.0

        delta_time = perf_counter() - self.timer_lst[timer_name]
        if delta_time < 0.0001:
            delta_time_prnt = '0.0000...'
        else:
            delta_time_prnt = round(delta_time, 4)
        fprint(f'Time for timer {timer_name!r} --> {delta_time_prnt} seconds')

        return delta_time
    

timer = Timer()