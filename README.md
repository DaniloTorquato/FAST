# FAST Approaches to Scalable Similarity-based Test Case Prioritization

# USAGE: python3 py/fast.py --absolute-path-to-project-root \<project root\> --algorithm \<algorithm\>

## Possible values for "algorithm" are: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all.

### Experiment FAST

### Test Prioritization Steps

#### Step 1: Clone the Repository
- Clone the repository using the following command:
    ```
    git clone git@github.com:apache/commons-cli.git
    ```

#### Step 2: Locate Test Directory
- The directory containing the project will be found at: `../commons-cli/src/test`

#### Step 3: Execute FAST Algorithm
- Navigate to the FAST directory and run the following command:
    ```
    python3 py/fast.py ../commons-cli/src/test FAST-pw
    ```

    Note: `../commons-cli/src/test` is the absolute-path-to-project-root.
    ```

#### Step 4: Retrieve Prioritized Tests
- Once the command completes execution, a file named "prioritized.txt" will be created in `commons-cli/src/test/fast`, which contains the prioritized list of test cases.
