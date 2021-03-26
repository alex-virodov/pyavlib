import numpy as np

def cache(filename, is_debug=False):
    def dbg_print(*args):
        if is_debug: print(*args)
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def wrapper(fun):
        def wrapper(**kwargs):
            dbg_print(f'called with kwargs={kwargs}')
            try:
                with np.load(filename + '.npz', allow_pickle=True) as data:
                    if np.all([np.all(data[k] == kwargs[k]) for k in kwargs]):
                        dbg_print(f'cache hit!')
                        return data['result']
                dbg_print(filename + ' cache mismatch, computing...')
            except IOError as e:
                dbg_print(filename + ' failed to load cache, computing...')

            result = fun(**kwargs)
            np.savez(filename, result=result, **kwargs)
            return result
        return wrapper
    return wrapper


@cache('test_cache_decorator', is_debug=True)
def test_fun(a, b, c):
    return a + b + c

@cache('test_cache_decorator_2', is_debug=True)
def test_fun_2(a, b, c):
    return (a + b, c)

if __name__ == "__main__":
    print("start")
    print(test_fun(a=1, b=2, c=np.array([1, 3])))
    print(test_fun_2(a=1, b=2, c=np.array([1, 3])))