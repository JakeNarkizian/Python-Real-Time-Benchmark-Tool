import os
import subprocess
import urllib2
from contextlib import contextmanager
import requests

from realTimeBenchmark import RealTimeBenchmark

# These strings are removed for privacy
test_URL = ''
test_path = ''
out_path = ''

chunkSize = 2**20 * 5

def _curl(buffered):
    with subprocess.Popen(('curl', test_URL),
                          bufsize=0 if not buffered else 1,
                          stdout=subprocess.PIPE).stdout as out:
        _readChunks(out)

def curlBuffered():
    _curl(False)

def curlUnbuffered():
    _curl(True)

def urllib():
    out = urllib2.urlopen(test_URL)
    _readChunks(out)

def _requests():
    out = requests.get(test_URL, stream=True).raw
    _readChunks(out)

def _readChunks(fileLikeObj):
    while fileLikeObj.read(chunkSize) not in ('', None):
        pass

@contextmanager
def scaleDownloadFile(size):
    # set up
    with open(test_path, 'w') as f:
        f.write(os.urandom(size))
    print size
    yield
    print 'benchmark with scale of size %d complete' % size

if __name__ == '__main__':
    benchmark = RealTimeBenchmark()
    benchmark.benchmark(scaleDownloadFile,
                        (2**(x*5) for x in range(0,7)),
                        curlBuffered, curlUnbuffered, urllib, _requests)
    with open(out_path, 'w') as f:
        benchmark.writeAsCSV(f)

