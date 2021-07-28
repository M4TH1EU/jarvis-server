def intent_handler(*args):
    """
    Creates an attribute on the method, so it can
    be discovered by the metaclass
    """

    def decorator(f):
        f._register = args
        return f

    return decorator