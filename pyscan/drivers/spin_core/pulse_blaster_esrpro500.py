from .spin_core_api import SpinCoreAPI


class PulseBlasterESRPro500(SpinCoreAPI):

    def __init__(self , clock=500, board=0):

        super().__init__(clock, board)