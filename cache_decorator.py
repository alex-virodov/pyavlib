import numpy as np


def cache(filename_or_fun=None, is_debug=False):
    def dbg_print(*args):
        if is_debug: print(*args)
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def decorator(fun):
        if filename_or_fun is None or callable(filename_or_fun):
            inferred_filename = fun.__name__
        else:
            inferred_filename = filename_or_fun
        def wrapper(**kwargs):
            dbg_print(f'called with kwargs={kwargs}')
            try:
                with np.load(inferred_filename + '.npz', allow_pickle=True) as data:
                    if np.all([np.all(data[k] == kwargs[k]) for k in kwargs]):
                        dbg_print(f'cache hit!')
                        return data['result']
                dbg_print(inferred_filename + ' cache mismatch, computing...')
            except:
                dbg_print(inferred_filename + ' failed to load cache, computing...')

            result = fun(**kwargs)
            np.savez(inferred_filename, result=result, **kwargs)
            return result
        return wrapper
    # https://stackoverflow.com/questions/35572663/using-python-decorator-with-or-without-parentheses
    if callable(filename_or_fun):
        return decorator(filename_or_fun)
    else:
        return decorator


def time_each_call(func):
    import time
    # https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        print(f'@time_each_call {func.__name__} {t2-t1}')
        return res
    return wrapper


@cache('test_cache_decorator', is_debug=True)
def test_fun(a, b, c):
    return a + b + c


@cache('test_cache_decorator_2', is_debug=True)
def test_fun_2(a, b, c):
    return (a + b, c)


@cache()
def test_cache_decorator_3(a, b, c):
    return a + b + c

# TODO: time_each_call doesn't work well with cache with autodetect name - one of them
#  ends up seeing 'wrapper' as function name.
# @time_each_call
@cache
def test_cache_decorator_4(a, b, c):
    return a + b + c

@time_each_call
def long_running_function(sleep_secs):
    import time
    time.sleep(sleep_secs)



if __name__ == "__main__":
    print("start")
    print(test_fun(a=1, b=2, c=np.array([1, 3])))
    print(test_fun_2(a=1, b=2, c=np.array([1, 3])))
    print(test_cache_decorator_3(a=1, b=2, c=np.array([1, 3])))
    print(test_cache_decorator_4(a=1, b=2, c=np.array([1, 3])))
    print(test_cache_decorator_4(a=1, b=2, c=np.array([1, 3])))
    long_running_function(sleep_secs=0.1)
    long_running_function(sleep_secs=0.6)
