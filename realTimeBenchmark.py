import time
from contextlib import contextmanager

import sys


class RealTimeBenchmark(object):
    """
    This class runs realtime benchmarks on a series of functions
    """
    def __init__(self):
        super(RealTimeBenchmark, self).__init__()
        self.benchmarks = {}

    def __str__(self):
        toRet = ""
        sortedKeys = sorted(self.benchmarks.keys())
        for key in sortedKeys:
            toRet += "%s with %s -> time %f\n" % (key[0], key[1], self.benchmarks[key])

        return toRet

    def writeAsCSV(self, writable=sys.stdout, header=None):
        """
        Write benchmark results in CSV file format to the given writable. If no writable
        is given stdout is used.
        """
        if header is None:
            header = 'function, scale parameter, time\n'
        else:
            header += '\n' if '\n' not in header else ''

        writable.write(header)

        for key in sorted(self.benchmarks.keys()):
            writable.write("%s, %s, %s\n" % (key[0], key[1], self.benchmarks[key]))



    def benchmark(self, scalingFx=None, iter=None, *args):
        """
        The given functions are iterated over, and each function is timed.

        Scaling tests is possible by passing a context manager, and an iterable with a range of inputs to
        pass as scaling args. The values yielded by the context manager are passed as args to the benchmarked
        methods.

        :param function scalingFx: A context manager that performs any necessary setup and teardown.
        :param iter: an iterable of args to call scalingFx with.
        :param function args: One or more functions to call _timedRun benchmarks on.

        """
        if ((iter is None and scalingFx is not None) or
            (iter is not None and scalingFx is None)):
            raise RuntimeError('Both Scaling fxand iteration must be passed')

        @contextmanager
        def emptyContextManager(i):
            yield None

        scalingFx = scalingFx or emptyContextManager
        iter = iter or [None]

        for i in iter:
            with scalingFx(i) as fxArgs:
                for fx in args:
                    try:
                        # Keys for marks dict are tuples containing function name and scale value from iteration
                        self.benchmarks[(fx.__name__, i)] = self._timedRun(fx, *fxArgs)
                    except:
                        print("Function '%s' failed with scale value '%d' " % (fx.__name__, i))


    def _timedRun(self, fx, *args):
        """
        Times how long it takes to run the given function fx.

        :param function fx: The function to run.
        :return: The total time in seconds that it took to run
        :rtype: int
        """
        start = time.time()
        fx(*args)
        return time.time() - start

