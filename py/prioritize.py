'''
This file is part of an AST'22 submission that is currently under review.

It is a modified version of a file from the FAST test case prioritization tool. 
For more information visit: https://github.com/icse18-FAST/FAST.

================================================================

This file is the entry point of FAST. It executes FAST in four modes:
- FAST_pw on the entire test suite;
- FAST_1 on the entire test suite;
- FAST_pw on the selected test suite;
- FAST_1 on the selected test suite.

Modifications were made to:
- Use the multiprocessing library to parallelize iterations.
- Output the prioritized test suite in a format compatible with Ekstazi.
- Simplify logic/parameters that are unnecessary for Fastazi experiments.

================================================================

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

import math
import os
# import pickle
import sys
from copy import deepcopy

from algorithms import fast_pw, fast_, loadTestSuite
from functions import read_file, save_file
#from constants import *
# import metric

import fast

# Multiprocessing tools
import multiprocessing
from multiprocessing import Pool
# from functools import partial
# from contextlib import contextmanager



working_dir = '.'
output_dir = '.'
method = sys.argv[4]

test_suite = {}
id_map = {}
total_time = {}

def bboxPrioritization(iteration):
    global working_dir
    global output_dir
    global id_map

    # Standard FAST parameters
    r, b = 1, 10
    
    print(" Run", iteration)
    
    if method == "fast-pw":
        stime, ptime, prioritization = fast_pw(
                r, b, test_suite)
    if method == "FAST-one":
        def one_(x): return 1
        stime, ptime, prioritization = fast_(
                one_, r, b, test_suite)
     
    if method == "FAST-log":
        def log_(x): return int(math.log(x, 2)) + 1
        stime, ptime, prioritization = fast_(
                log_, r, b, test_suite)       

    if method == "FAST-sqrt":
        def sqrt_(x): return int(math.sqrt(x)) + 1
        stime, ptime, prioritization = fast_(
                sqrt_, r, b, test_suite)
    
    if method == "FAST-all":
        def all_(x): return x
        stime, ptime, prioritization = fast_(
                all_, r, b, test_suite)
    
    # writePrioritizedOutput(output_dir, prioritization, iteration)
    out_path = os.path.join(output_dir, str("prioritized")+".txt")
    save_file(out_path, map(lambda p: id_map[p], prioritization))
    # out_path = os.path.join(output_dir, str(iteration)+"_ids.txt")
    # save_file(out_path, map(lambda p: "{}".format(p), prioritization))


    print("  Progress: 100%  ")
    print("  Running time:", stime + ptime)
    print("  Arquivo com os testes priorizados salvo em: ", out_path)
    print("")
    return stime + ptime
    


if __name__ == "__main__":
    num_iterations = 1
    what_to_prioritize = "all"
    working_dir = sys.argv[2]
    results_dir = sys.argv[2]
    fast_dir = os.path.join(working_dir,'.fast')
    what_to_prioritize == "all"
    suite = "fast"
    tests = all_tests
    test_suite, id_map = loadTestSuite(tests, input_dir=fast_dir)
    output_dir = os.path.join(results_dir, suite)
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    num_cores = multiprocessing.cpu_count()
    with Pool(num_cores) as pool:
            running_time = pool.map(bboxPrioritization, range(1, num_iterations + 1))

    total_time = deepcopy(running_time)
    
