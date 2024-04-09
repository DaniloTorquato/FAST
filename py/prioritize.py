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
import sys
from copy import deepcopy
from algorithms import fast_pw, fast_, loadTestSuite
import fast
import multiprocessing
from multiprocessing import Pool
import argparse


usage = """USAGE: python3 fast.py <project-root> <algorithm> r b python3 py/prioritize.py -project_root  <project-root> -algorithm <algorithm> -r <r> -b <b>
    	OPTIONS:
  	<project-root>: absolute path to the project.
  	<algorithm>: possible values for <algorithm> are: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all.
"""


def read_file(file_path):
    with open(file_path, "r") as f:
        return  list(
                    filter(lambda line: len(line) > 0 and "$" not in line,
                        map(lambda line: line.strip(), 
                            f.readlines() 
                        ) 
                    ) 
                )
    return []


def save_file(file_path, data):
    with open(file_path, "w") as f:
        f.write("\n".join(data)+"\n")

def bboxPrioritization(iteration, r, b):

    # Standard FAST parameters
    #r, b = 1, 10
    
    print(" Run", iteration+ 1)
    
    if algorithm == "FAST-pw":
        stime, ptime, prioritization = fast_pw(
                r, b, test_suite)
    if algorithm == "FAST-one":
        def one_(x): return 1
        stime, ptime, prioritization = fast_(
                one_, r, b, test_suite)
     
    if algorithm == "FAST-log":
        def log_(x): return int(math.log(x, 2)) + 1
        stime, ptime, prioritization = fast_(
                log_, r, b, test_suite)       

    if algorithm == "FAST-sqrt":
        def sqrt_(x): return int(math.sqrt(x)) + 1
        stime, ptime, prioritization = fast_(
                sqrt_, r, b, test_suite)
    
    if algorithm == "FAST-all":
        def all_(x): return x
        stime, ptime, prioritization = fast_(
                all_, r, b, test_suite)
    
    out_path = os.path.join(output_dir, str("prioritized")+".txt")
    save_file(out_path, map(lambda p: id_map[p], prioritization))


    print("  Progress: 100%  ")
    print("  Running time:", stime + ptime)
    print("  File with prioritized tests saved: ", out_path)
    print("")
    return stime + ptime
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run FAST with various algorithms on a test suite')
    parser.add_argument('-t', '--tests_dir', type=str, help='Absolute path to the project root')
    parser.add_argument('-a', '--algorithm', choices=["FAST-pw", "FAST-one", "FAST-log", "FAST-sqrt", "FAST-all"], help='Algorithm to use')
    parser.add_argument('-o', '--output', type=str, help='Output directory where the prioritized list "prioritized.txt" will be saved')
    args = parser.parse_args()
    #print(args)
    #print(args.tests_dir)
    #sys.exit()
    #args = parser.parse_args(['-a', 'FAST-pw', '-t', '../small', '-o', 'out'])
    #args = {algorithm='FAST-pw', b=10, project_root='../small', r=1}

    working_dir = args.tests_dir
    algorithm = args.algorithm
    output_dir = args.output


    # FAST parameters
    k, n, r, b = 5, 10, 1, 10    
    fast_dir = os.path.join(working_dir, '.fast')


    test_suite = {}
    id_map = {}
    total_time = {}
    
    tests = fast.parseTests(working_dir, r, b, k)
    test_suite, id_map = loadTestSuite(tests, input_dir=fast_dir)
    #output_dir = os.path.join(working_dir, "fast")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    num_cores = multiprocessing.cpu_count()
    

    with Pool(num_cores) as pool:
        running_time = pool.starmap(bboxPrioritization, [(i, r, b) for i in range(1)])

    total_time = deepcopy(running_time)
