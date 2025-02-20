import cirq

# Function to create the sample circuit with intentional empty moments
# Function to create the sample circuit with intentional empty moments
def create_test_circuit():
    # Create a sample quantum circuit
    qubits = [cirq.GridQubit(0, i) for i in range(2)]
    circuit = cirq.Circuit()

    # Add operations with empty moments in between
    circuit.append([cirq.X(qubits[0]), cirq.H(qubits[1])])
    circuit.append(cirq.Moment())  # Intentional empty moment
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    circuit.append(cirq.Moment())  # Another intentional empty moment
    circuit.append(cirq.measure(qubits[0], key="q0"))
    circuit.append(cirq.Moment())  # Empty moment after measurement
    circuit.append(cirq.measure(qubits[1], key="q1"))
    circuit.append(cirq.Moment())  # Final empty moment
    return circuit


# Optimization function simulating "before" the fix
def optimize_circuit_before(circuit):
    # Simulate the old optimization methods (direct mutation style)
    cirq.merge_single_qubit_gates_to_phxz(circuit)
    circuit = cirq.drop_empty_moments(circuit)
    circuit = cirq.synchronize_terminal_measurements(circuit)
    return circuit

# Optimization function simulating "after" the fix
def optimize_circuit_after(circuit):
    # New API with functional optimization methods
    circuit = cirq.merge_single_qubit_gates_to_phxz(circuit)
    circuit = cirq.drop_empty_moments(circuit)
    circuit = cirq.synchronize_terminal_measurements(circuit)
    return circuit

# Check if the last moments contain only measurement operations
def check_measurements_at_end(circuit):
    last_moment = circuit[-1]
    only_measurements = all(isinstance(op.gate, cirq.MeasurementGate) for op in last_moment.operations)
    return "Measurements are at the end of the circuit" if only_measurements else "Non-measurement operations found at the end"

def main():
    # Scenario 1: Initial Circuit without Optimization
    print("=== Scenario 1: Initial Circuit without Optimization ===")
    original_circuit = create_test_circuit()
    print("Original Circuit:\n", original_circuit)

    # Scenario 2: Merging Single-Qubit Gates
    print("\n=== Scenario 2: Merging Single-Qubit Gates ===")
    circuit_before_merge = original_circuit.copy()
    circuit_after_merge = original_circuit.copy()
    cirq.merge_single_qubit_gates_to_phxz(circuit_before_merge)  # Before fix (direct mutation)
    circuit_after_merge = cirq.merge_single_qubit_gates_to_phxz(circuit_after_merge)  # After fix
    print("Before Fix - Merged Circuit:\n", circuit_before_merge)
    print("After Fix - Merged Circuit:\n", circuit_after_merge)

    # Scenario 3: Removing Empty Moments
    print("\n=== Scenario 3: Removing Empty Moments ===")
    circuit_before_empty = circuit_before_merge.copy()
    circuit_after_empty = circuit_after_merge.copy()
    circuit_before_empty = cirq.drop_empty_moments(circuit_before_empty)  # Before fix
    circuit_after_empty = cirq.drop_empty_moments(circuit_after_empty)    # After fix
    print("Before Fix - Empty Moments Removed:\n", circuit_before_empty)
    print("After Fix - Empty Moments Removed:\n", circuit_after_empty)

    # Scenario 4: Aligning Measurements at the End
    print("\n=== Scenario 4: Aligning Measurements at the End ===")
    circuit_before_align = circuit_before_empty.copy()
    circuit_after_align = circuit_after_empty.copy()
    circuit_before_align = cirq.synchronize_terminal_measurements(circuit_before_align)  # Before fix
    circuit_after_align = cirq.synchronize_terminal_measurements(circuit_after_align)    # After fix
    print("Before Fix - Measurements Aligned:\n", circuit_before_align)
    print("After Fix - Measurements Aligned:\n", circuit_after_align)
    print("Check Measurements at End (Before Fix):", check_measurements_at_end(circuit_before_align))
    print("Check Measurements at End (After Fix):", check_measurements_at_end(circuit_after_align))

    # Scenario 5: Final Optimized Circuit Comparison
    print("\n=== Scenario 5: Final Optimized Circuit Comparison ===")
    print("Final Optimized Circuit (Before Fix):\n", circuit_before_align)
    print("Final Optimized Circuit (After Fix):\n", circuit_after_align)
    if circuit_before_align == circuit_after_align:
        print("Both circuits are identical.")
    else:
        print("Circuits differ between before and after fix.")

# Run the main function
if __name__ == "__main__":
    main()
