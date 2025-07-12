import time
from functools import wraps
from collections import defaultdict

class CountingProxy:
    def __init__(self, obj, stats):
        self._obj = obj
        self._stats = stats

    def __getattr__(self, attr):
        orig_attr = getattr(self._obj, attr)

        if callable(orig_attr):
            def hooked(*args, **kwargs):
                self._stats['total_calls'] += 1
                key = f"{type(self._obj).__name__}.{attr}"
                self._stats['api_counter'][key] += 1

                result = orig_attr(*args, **kwargs)

                # If result is PyGithub object → wrap
                if hasattr(result, '__class__') and result.__class__.__module__.startswith('github.'):
                    return CountingProxy(result, self._stats)

                # If result is list/tuple of PyGithub objects → wrap each
                if isinstance(result, (list, tuple)):
                    if len(result) > 0 and hasattr(result[0], '__class__') and result[0].__class__.__module__.startswith('github.'):
                        return [CountingProxy(item, self._stats) for item in result]

                return result
            return hooked
        else:
            return orig_attr

    def __iter__(self):
        for item in self._obj:
            if hasattr(item, '__class__') and item.__class__.__module__.startswith('github.'):
                yield CountingProxy(item, self._stats)
            else:
                yield item

    def __len__(self):
        """Pass length calls to wrapped object if it supports it."""
        return len(self._obj)

    def __getitem__(self, item):
        """Support indexing."""
        return self._obj[item]


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
