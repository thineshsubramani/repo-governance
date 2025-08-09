import time
from functools import wraps
from collections import defaultdict

def is_pygithub_obj(obj):
    return hasattr(obj, '__class__') and obj.__class__.__module__.startswith('github.')

class CountingProxy:
    def __init__(self, obj, stats):
        object.__setattr__(self, '_obj', obj)
        object.__setattr__(self, '_stats', stats)

    def __getattribute__(self, attr):
        _obj = object.__getattribute__(self, '_obj')
        _stats = object.__getattribute__(self, '_stats')
        orig_attr = getattr(_obj, attr)

        if callable(orig_attr):
            def hooked(*args, **kwargs):
                _stats['total_calls'] += 1
                key = f"{type(_obj).__name__}.{attr}"
                _stats['api_counter'][key] += 1

                result = orig_attr(*args, **kwargs)
                return wrap_result(result, _stats)
            return hooked
        else:
            # For property access, wrap if PyGithub object
            if is_pygithub_obj(orig_attr):
                return CountingProxy(orig_attr, _stats)
            return orig_attr

    def __iter__(self):
        _obj = object.__getattribute__(self, '_obj')
        _stats = object.__getattribute__(self, '_stats')
        for item in _obj:
            yield wrap_result(item, _stats)

    def __len__(self):
        _obj = object.__getattribute__(self, '_obj')
        return len(_obj)

    def __getitem__(self, item):
        _obj = object.__getattribute__(self, '_obj')
        _stats = object.__getattribute__(self, '_stats')
        result = _obj[item]
        return wrap_result(result, _stats)

def wrap_result(result, stats):
    if is_pygithub_obj(result):
        return CountingProxy(result, stats)
    if isinstance(result, (list, tuple)):
        return type(result)(wrap_result(item, stats) for item in result)
    if hasattr(result, '__iter__') and not isinstance(result, (str, bytes, dict)):
        # For generators/iterators
        try:
            return (wrap_result(item, stats) for item in result)
        except Exception:
            return result
    return result

def measure_api_stats(func):
    """
    Decorator: build CountingProxy, track stats, print summary.
    """
    @wraps(func)
    def wrapper(client, *args, **kwargs):
        stats = {
            "total_calls": 0,
            "api_counter": defaultdict(int)
        }
        wrapped_client = CountingProxy(client, stats)
        start = time.time()

        result = func(wrapped_client, *args, **kwargs)

        elapsed_ms = (time.time() - start) * 1000
        print(f"\n[STATS] {func.__name__}: total {stats['total_calls']} API calls, {elapsed_ms:.2f} ms")
        for api, count in stats['api_counter'].items():
            print(f"  {api}: {count}")
        return result
    return wrapper
