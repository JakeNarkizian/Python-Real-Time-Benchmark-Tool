import os
import subprocess
import urllib2
from contextlib import contextmanager
import requests

from realTimeBenchmark import RealTimeBenchmark

# These strings are removed for privacy
test_URL = ""
test_path = ""
out_path = ""

def curl_meth():
    subprocess.check_call(['curl', test_URL], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def urllib_meth():
    urllib2.urlopen(test_URL).read()

def requests_meth():
    requests.get(test_URL)._content

@contextmanager
def scaleDownloadFile(size):
    # set up
    with open(test_path, 'w') as f:
        f.write(os.urandom(size))
    yield

if __name__ == '__main__':
    benchmark = RealTimeBenchmark()
    benchmark.mark(scaleDownloadFile, range(2**15, 2**15 + 50), curl_meth, urllib_meth, requests_meth)
    with open(out_path, 'w') as f:
        benchmark.writeCSV(f)

