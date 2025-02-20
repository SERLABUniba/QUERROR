import pennylane as qml
from pennylane import numpy as np
from pennylane.tape import QuantumTape
from pennylane.ops import __all__ as all_ops  # Importing all available operators

# Define a sample quantum function for testing
def qfunc(x, y, z):
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.Hadamard(wires=2)
    qml.RZ(z, wires=2)
    qml.CNOT(wires=[2, 1])
    qml.RX(z, wires=0)
    qml.CNOT(wires=[1, 0])
    qml.RX(x, wires=0)
    qml.CNOT(wires=[1, 0])
    qml.RZ(-z, wires=2)
    qml.RX(y, wires=2)
    qml.Y(2)
    qml.CY(wires=[1, 2])
    return qml.expval(qml.Z(0))

# Setup
dev = qml.device('default.qubit', wires=[0, 1, 2])

# Function to compile and execute the circuit
def compile_and_run(qfunc, x, y, z, fix_applied=False):
    with QuantumTape() as tape:
        qfunc(x, y, z)

    # Function to define the stopping condition based on the code commit
    def stop_at(obj):
        if not isinstance(obj, qml.operation.Operator):
            return True
        if not obj.has_decomposition:
            return True
        return obj.name in all_ops and (not getattr(obj, "only_visual", False))

    # Apply compilation transform with or without the fix
    if fix_applied:
        [expanded_tape], _ = qml.devices.preprocess.decompose(
            tape, stopping_condition=stop_at, max_expansion=5, name="compile"
        )
        compiled_tapes = [expanded_tape]
    else:
        compiled_tapes = [tape]  # No compilation in the "before fix" scenario

    # Execute and store results
    results = []
    for ct in compiled_tapes:
        result = qml.execute([ct], device=dev)
        results.append(result)

    return compiled_tapes, results

def main():
    x, y, z = 0.2, 0.3, 0.4

    print("=== Before Fix ===")
    compiled_tapes_before, results_before = compile_and_run(qfunc, x, y, z, fix_applied=False)
    for tape in compiled_tapes_before:
        print("Original Circuit:\n", tape.draw())
    print("Results:", results_before)

    print("\n=== After Fix ===")
    compiled_tapes_after, results_after = compile_and_run(qfunc, x, y, z, fix_applied=True)
    for tape in compiled_tapes_after:
        print("Compiled Circuit:\n", tape.draw())
    print("Results:", results_after)

# Run the main function to execute the tests
if __name__ == "__main__":
    main()
