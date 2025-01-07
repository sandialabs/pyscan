class ReadOnlyException(Exception):

    def __init__(self, prop):

        msg = f"{prop} is a read only property and can't be set"

        super().__init__(msg)
