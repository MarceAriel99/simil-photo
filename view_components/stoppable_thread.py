import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.close_window = False

    def stop(self, close_window:bool = False):
        self._stop_event.set()
        self.close_window = close_window

    def stopped(self):
        return self._stop_event.is_set()
    
def current_thread() -> StoppableThread:
    return threading.current_thread()