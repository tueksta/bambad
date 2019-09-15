import datetime
import logging
import time


def elapsedTime(start_time):
    timespan = time.perf_counter() - start_time
    elapsed_time = str(datetime.timedelta(seconds=round(timespan, 0)))
    logging.debug('Total time to complete: ' + elapsed_time)


def with_timer(func, *args):
    def func_wrapper(*args):
        start_time = time.perf_counter()
        result = func(*args)
        elapsedTime(start_time)
        return result
    return func_wrapper
