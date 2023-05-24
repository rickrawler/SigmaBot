class UnknownCommandError(IOError):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)