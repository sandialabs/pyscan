class AbstractBaseScanOptimizer():

    def step_optimizer():
        pass

    def to_json():
        pass


class AbstractScanOptimizer(AbstractBaseScanOptimizer):

    def to_json(self):
        return self.__dict__


class AbstractRuninfoScanOptimizer(AbstractScanOptimizer):

    def __init__(self, runinfo):
        super().__init__()
        self.runinfo = runinfo

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if k != 'runinfo'}


class AbstractExitScanOptimizer(AbstractScanOptimizer):

    def __init__(self):
        super().__init__()
        self.running = True


class AbstractRuninfoExitScanOptimizer(AbstractRuninfoScanOptimizer, AbstractExitScanOptimizer):

    def __init__(self, runinfo):
        super().__init__(runinfo)
