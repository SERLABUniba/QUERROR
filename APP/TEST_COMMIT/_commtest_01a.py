import math
import traceback
import symengine as se

# Setting higher precision using RealMPFR
# precision_bits = 50  # Set to 50 bits of precision for RealMPFR

# Setting higher precision using RealMPFR
precision_bits = 80  # Set to 50 bits of precision for RealMPFR

# Function to execute and capture errors or issues in code snippets
def run_code_snippet(snippet_func, description):
    print(f"Running: {description}")
    try:
        snippet_func()
        print("Result: No errors or issues detected.")
    except Exception as e:
        print("Error detected:", str(e))
        traceback.print_exc()
    print("\n" + "-"*50 + "\n")

"""# Test 1: Large Operand Value with Higher Precision
def test_large_operand_high_precision():
    operand_large = se.RealMPFR("4.5e20", precision_bits)
    scaling_factor_1e9 = se.RealMPFR("1e9", precision_bits)
    scaling_factor_10_9 = se.RealMPFR(10**9, precision_bits)

    result_1e9_large = operand_large * scaling_factor_1e9
    result_10_9_large = operand_large * scaling_factor_10_9
    difference_large = result_1e9_large - result_10_9_large

    print("Test 1 - Large Operand with Higher Precision:")
    print("Result with 1e9:", result_1e9_large)
    print("Result with 10^9:", result_10_9_large)
    print("Difference:", difference_large)
    print("-" * 50)"""


# Test with a Complex Mathematical Operand
def test_large_operand_high_precision():
    # Define a complex operand using an irrational number calculation
    operand_complex = se.RealMPFR(str(se.sqrt(2) * math.pi), precision_bits)  # sqrt(2) * pi with high precision
    scaling_factor_1e9 = se.RealMPFR("1e9", precision_bits)
    scaling_factor_10_9 = se.RealMPFR(10**9, precision_bits)

    # Calculate results with 1e9 and 10^9 scaling factors
    result_1e9_complex = operand_complex * scaling_factor_1e9
    result_10_9_complex = operand_complex * scaling_factor_10_9
    difference_complex = result_1e9_complex - result_10_9_complex

    print("Test with Complex Operand and Very High Precision:")
    print("Operand (sqrt(2) * pi):", operand_complex)
    print("Result with 1e9:", result_1e9_complex)
    print("Result with 10^9:", result_10_9_complex)
    print("Difference due to precision loss:", difference_complex)
    print("-" * 50)

# Test 2: Chained Calculations with Higher Precision
def test_chained_calculations_high_precision():
    operand_chain = se.RealMPFR("4.5", precision_bits)
    scaling_factor_1e9 = se.RealMPFR("1e9", precision_bits)
    scaling_factor_10_9 = se.RealMPFR(10**9, precision_bits)

    result_chain_1e9 = operand_chain * scaling_factor_1e9 * scaling_factor_1e9 / scaling_factor_1e9
    result_chain_10_9 = operand_chain * scaling_factor_10_9 * scaling_factor_10_9 / scaling_factor_10_9
    difference_chain = result_chain_1e9 - result_chain_10_9

    print("Test 2 - Chained Calculations with Higher Precision:")
    print("Result with 1e9 (chain):", result_chain_1e9)
    print("Result with 10^9 (chain):", result_chain_10_9)
    print("Difference:", difference_chain)
    print("-" * 50)

# Test 3: Complex Expression (Square Root) with Higher Precision
def test_complex_expression_high_precision():
    operand_complex = se.RealMPFR("4.5", precision_bits)
    scaling_factor_1e9 = se.RealMPFR("1e9", precision_bits)
    scaling_factor_10_9 = se.RealMPFR(10**9, precision_bits)

    result_complex_1e9 = se.sqrt(operand_complex * scaling_factor_1e9) * scaling_factor_1e9
    result_complex_10_9 = se.sqrt(operand_complex * scaling_factor_10_9) * scaling_factor_10_9
    difference_complex = result_complex_1e9 - result_complex_10_9

    print("Test 3 - Complex Expression (Square Root) with Higher Precision:")
    print("Result with 1e9 (complex):", result_complex_1e9)
    print("Result with 10^9 (complex):", result_complex_10_9)
    print("Difference:", difference_complex)
    print("-" * 50)

# Organize code snippets with metadata for testing
commits = [
    {
        "description": "Scaling Fix - Large Operand High Precision Test (PbD: P4, SbD: S2)",
        "before": test_large_operand_high_precision,
        "after": test_large_operand_high_precision,
        "phase": "Testing Phase",
        "principle": "PbD: Privacy Embedded into Design, SbD: Secure Defaults"
    },
    {
        "description": "Scaling Fix - Chained Calculations High Precision Test (PbD: P4, SbD: S2)",
        "before": test_chained_calculations_high_precision,
        "after": test_chained_calculations_high_precision,
        "phase": "Testing Phase",
        "principle": "PbD: Privacy Embedded into Design, SbD: Secure Defaults"
    },
    {
        "description": "Scaling Fix - Complex Expression High Precision Test (PbD: P4, SbD: S2)",
        "before": test_complex_expression_high_precision,
        "after": test_complex_expression_high_precision,
        "phase": "Testing Phase",
        "principle": "PbD: Privacy Embedded into Design, SbD: Secure Defaults"
    }
]

# Function to run all commits in the framework
def test_commit_fixes():
    for commit in commits:
        print(f"\nTesting commit in QSDLC Phase: {commit['phase']}")
        print(f"Principles Applied: {commit['principle']}")
        run_code_snippet(commit["before"], f"Before fix: {commit['description']}")
        run_code_snippet(commit["after"], f"After fix: {commit['description']}")

# Main function to execute the test framework
def main():
    print("Starting test framework for code commits with higher precision...\n")
    test_commit_fixes()
    print("\nTesting completed.")

# Run main function
if __name__ == "__main__":
    main()
