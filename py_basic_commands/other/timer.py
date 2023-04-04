from dataclasses    import dataclass
from py_basic_commands.fscripts   import fprint
from time   import perf_counter
from py_basic_commands.base   import Base

@dataclass
class Timer(Base):
    def __post_init__(self) -> None:
        super().__init__()

        self.timer_lst:dict[str,float] = {}


    def start_timer(self, timer_name:str, do_print:bool=True) -> bool:
        """Start a timer with a specified name"""

        # Chek values
        do_print = self._check_input_val(do_print, self._do_print)

        if self.timer_lst.get(timer_name):
            print(f'Timer with name already started: {timer_name}')
            return False

        self.timer_lst[timer_name] = perf_counter()
        fprint(f'Timer started: {timer_name}', do_print=do_print)

        return True


    def end_timer(self, timer_name:str) -> float:
        """End timer with given name"""

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