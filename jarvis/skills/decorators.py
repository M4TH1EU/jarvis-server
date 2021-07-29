def intent_handler(*args):
    """
    Creates an attribute on the method, so it can
    be discovered by the metaclass
    """

    def decorator(f):
        f._type = "adapt"
        f._data = args
        return f

    return decorator


def intent_file_handler(*args):
    """
    Creates an attribute on the method, so it can
    be discovered by the metaclass
    """

    def decorator(f):
        f._type = "padatious"
        f._data = args
        return f

    return decorator
