from pyscan_tlk.definitions.kinesisexception import KinesisException


def check_return_for_error(ret):

    if ret != 0:
        raise KinesisException(ret)


def check_for_error(func, *arg, **kwarg):

    def new_function(*arg, **kwarg):

        ret = func(*arg, **kwarg)

        check_for_error(ret)

    return new_function
