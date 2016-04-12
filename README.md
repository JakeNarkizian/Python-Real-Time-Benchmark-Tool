# Real-Time-Benchmark
Python benchmark class that calculates real time cost of running one or more python functions

Example:
```
from realTimeBenchmark import RealTimeBenchmark
from contextlib import contextmanager

def testMe():
    pass 

def testMe2():
    pass

@contextmanager
def scalingFx(scale):
    # set up pertaining to scale here
    yield 
    # tear down here 

benchmark = RealTimeBenchmark()
benchmark.benchmark(scalingFx=scalingFx, 
                    iter=range(0,10),
                    testMe, 
                    testMe2)

print benchmark
```
