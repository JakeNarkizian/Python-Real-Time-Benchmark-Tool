import time
from contextlib import contextmanager

import sys


class RealTimeBenchmark(object):
    """
    This class runs realtime benchmarks on a series of functions
    """
    def __init__(self):
        super(RealTimeBenchmark, self).__init__()
        self.marks = {}

    def __str__(self):
        toRet = ""
        sortedKeys = sorted(self.marks.keys())
        for key in sortedKeys:
            toRet += "%s with %s -> time %f\n" % (key[0], key[1], self.marks[key])

        return toRet

    def writeCSV(self, writable=sys.stdout):
        """
        Write a CSV file to the given writable. If no writable is given stdout is used.
        """
        writable.write('function, parameter, time\n')
        sortedKeys = sorted(self.marks.keys())
        for key in sortedKeys:
            writable.write("%s, %s, %s\n" % (key[0], key[1], self.marks[key]))



    def mark(self, scalingFx=None, iter=None, *args):
        """
        The given functions are iterated over, and each function is timed.

        Scaling tests is possible by passing a context manager, and an iterable with a range of inputs to
        pass as args.

        :param function scalingFx: A context manager that performs any necessary setup and teardown.
        :param iter: an iterable of args to call scalingFx with.
        :param function args: One or more functions to call _timeRun benchmarks on

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
            with scalingFx(i):
                for fx in args:
                    try:
                        # Keys for marks dict are tuples containing function name and scale value from iteration
                        self.marks[(fx.__name__, i)] = self._timeRun(fx)
                    except:
                        print("Function '%s' failed with scale value '%d' " % (fx.__name__, i))


    def _timeRun(self, fx):
        """
        Times how long it takes to run the given function fx.

        :param function fx: The function to run.
        :return: The total time in seconds that it took to run
        :rtype: int
        """
        start = time.time()
        fx()
        return time.time() - start

