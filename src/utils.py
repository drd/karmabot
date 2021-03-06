import time

class Cache:
    def __init__(self, func, expire_seconds=None):
        self.func = func
        self.expire_seconds = expire_seconds
        self.last_result = None
        self.last_time = None
        self.last_args = None
        self.last_kwargs = None
        
    def __call__(self, *args, **kwargs):
        call_time = time.time()
        if args != self.last_args or kwargs != self.last_kwargs or \
           self.last_time is None or call_time > self.last_time + self.expire_seconds:
            self.last_result = self.func(*args, **kwargs)
            self.last_time = call_time
            self.last_args = args
            self.last_kwargs = kwargs
            
        return self.last_result
        
    def reset(self):
        self.last_time = None
