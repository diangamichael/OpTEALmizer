#!/bin/env python3

import os
import sys
from pyteal import *

if len(sys.argv) != 2:
    print(f"Usage python3 {sys.argv[0]} <filename>")
    sys.exit(1)

filename = sys.argv[1]

try:
    with open(os.path.join("src", filename)) as f:
        original_program = compileTeal(f.read(), Mode.Application)
except FileNotFoundError:
    # We don't have a hacked optimization so lets bail out
    with open(filename) as file:
        original_program = compileTeal(f.read(), Mode.Application)

# Define the improved program
improved_program = Seq([
    # TODO: Add optimizations here
    # ...
    
    # Return
    Return(Int(1))
])

# Evaluate the improved program against the original program on the provided tests
test_results = []

# TODO: Add tests here
# ...

# Score the optimizations
def score(test_results):
    gas_improvements = 0
    size_improvements = 0

    for original, improved in test_results:
        gas_improvements += gas_used_in_testsuite(original) - gas_used_in_testsuite(improved)
        size_improvements += len(original_program.result) - len(improved.result)

    return gas_improvements * 0.8 + size_improvements * 0.2

def gas_used_in_testsuite(contract):
    total_gas = 0

    for transaction in contract.test_cases:
        total_gas += transaction["expected_output"]["gas_used"]

    return total_gas

# Print the improved program and the score
print(improved_program.prettyStr())
print(score(test_results))