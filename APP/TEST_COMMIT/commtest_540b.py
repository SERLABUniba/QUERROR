import pennylane as qml
from pennylane import numpy as np
from pennylane.tape import QuantumTape

# Set up a standard device that supports decompositions more flexibly
dev = qml.device("default.qubit", wires=3)


# Define a modified quantum function with decomposable gates
def qfunc(x, y, z):
    qml.Hadamard(wires=0)
    qml.CRX(x, wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.RY(y, wires=1)
    qml.CZ(wires=[2, 0])
    # Replace RZ with a decomposed sequence (RX and RY can be used if RZ fails)
    qml.RX(np.pi / 2, wires=2)
    qml.RY(z, wires=2)
    qml.RX(-np.pi / 2, wires=2)
    return qml.expval(qml.PauliZ(0))


# Create a tape from the quantum function
with QuantumTape() as tape:
    qfunc(0.2, 0.3, 0.4)

# Parameters for expansion depth and compilation passes
expand_depth = 5
num_passes = 2


# Compilation function (Before Fix)
def compile_circuit_before(tape, expand_depth, num_passes):
    compiled_tape = tape.expand(depth=expand_depth)
    for _ in range(num_passes):
        compiled_tape = compiled_tape.expand(depth=expand_depth)
    return compiled_tape


# Compilation function (After Fix)
def compile_circuit_after(tape, expand_depth, num_passes):
    # Stopping condition to allow full decomposition up to a specific depth
    stopping_condition = lambda obj: False

    # Use the decompose function with the stopping condition
    [compiled_tape], _ = qml.devices.preprocess.decompose(
        tape, stopping_condition=stopping_condition, max_expansion=expand_depth, name="compile"
    )
    for _ in range(num_passes):
        [compiled_tape], _ = qml.devices.preprocess.decompose(
            compiled_tape, stopping_condition=stopping_condition, max_expansion=expand_depth, name="compile"
        )
    return compiled_tape


# Compile before and after fix
compiled_before = compile_circuit_before(tape, expand_depth, num_passes)
compiled_after = compile_circuit_after(tape, expand_depth, num_passes)

# Display compiled circuits for comparison
print("=== Compiled Circuit Before Fix ===")
print(compiled_before.draw())

print("\n=== Compiled Circuit After Fix ===")
print(compiled_after.draw())

# Compare gate sequences to detect differences
if compiled_before.operations == compiled_after.operations:
    print("\nNo differences in the gate sequence between before and after fix.")
else:
    print("\nDifferences detected in the gate sequence between before and after fix.")
