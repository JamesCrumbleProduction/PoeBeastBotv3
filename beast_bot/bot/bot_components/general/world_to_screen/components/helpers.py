from functools import wraps


def source_auto_update(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        instance.update_source(**instance._source_kwargs)
        instance._source_kwargs.clear()

        return func(*args, **kwargs)

    return wrapper
