class AbstractOptimizer():

    def run_optimizer():
        pass


class ScanOptimizer(AbstractOptimizer):

    def __init__(self, optimization_function):
        self.opt_f = optimization_function
    
    def run_optimizer(self, args, kwargs):
        return self.opt_f(*args, **kwargs)


class ScanRunOptimizer(ScanOptimizer):

    def run_optimizer(self, args, kwargs, runinfo):
        kwargs_runinfo = {k: v for k, v in kwargs.items()}
        kwargs_runinfo['runinfo'] = runinfo
        return super().run_optimizer(args, kwargs_runinfo)


class ScanExitOptimizer(ScanOptimizer):

    def __init__(self, optimization_function):
        super().__init__(optimization_function)
        self.running = True

    def run_optimizer(self, args, kwargs):
        opt_res, keep_running = super().run_optimizer(args, kwargs)
        self.running = keep_running
        return opt_res


class ScanExitRunOptimizer(ScanExitOptimizer, ScanRunOptimizer):

    def run_optimizer(self, args, kwargs, runinfo):
        opt_res, keep_running = ScanRunOptimizer.run_optimizer(self, args, kwargs, runinfo)
        self.running = keep_running
        return opt_res
