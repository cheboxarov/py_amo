def with_kwargs_filter(func):
    def wrapper(*args, **kwargs):
        if "with_" in kwargs.keys():
            kwargs["with"] = kwargs["with_"]
            del kwargs["with_"]
        return func(*args, **kwargs)

    return wrapper
