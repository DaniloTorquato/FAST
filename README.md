# FAST Approaches to Scalable Similarity-based Test Case Prioritization

This is a modified version of [FAST](https://github.com/brenomiranda/FAST) that can be used to produce a prioritized test suite given a target test directory. Currently it supports only the black-box version of the prioritization, i.e., it does not assume that coverage data is available.

## Usage: 
```
python3 py/fast.py <target-dir> <algorithm>
```

Possible values for "algorithm" are: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all.

## Usage example

### Step 1: Locate the Target Test Directory

For our example we will use the Apache commons-cli project. After cloning the project with `git clone https://github.com/apache/commons-cli.git`, the test directory will be available at `../commons-cli/src/test`

### Step 2: Execute FAST

From the FAST directory, run the command:
    ```
    python3 py/fast.py ../commons-cli/src/test FAST-pw
    ```

After running FAST, a file containing the prioritized list of test cases should be created in `commons-cli/src/test/fast/prioritized.txt`.
