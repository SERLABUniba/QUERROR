import cirq

# Function to create the sample circuit
def create_test_circuit():
    # Create a sample quantum circuit
    qubits = [cirq.GridQubit(0, i) for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append([cirq.X(qubits[0]), cirq.H(qubits[1])])
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    circuit.append(cirq.measure(qubits[0], key="q0"))
    circuit.append(cirq.measure(qubits[1], key="q1"))
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

# Check if the last moments contain only measurement operations after the fix
def check_measurements_at_end(circuit):
    last_moment = circuit[-1]
    only_measurements = all(isinstance(op.gate, cirq.MeasurementGate) for op in last_moment.operations)
    return "Measurements are at the end of the circuit" if only_measurements else "Non-measurement operations found at the end"

def main():
    # Run the "before" fix optimization
    print("=== BEFORE FIX ===")
    original_circuit = create_test_circuit()
    circuit_before = original_circuit.copy()
    optimized_before = optimize_circuit_before(circuit_before)
    print("Original Circuit (Before Fix):\n", original_circuit)
    print("Optimized Circuit (Before Fix):\n", optimized_before)
    print(check_measurements_at_end(optimized_before))

    # Run the "after" fix optimization
    print("\n=== AFTER FIX ===")
    circuit_after = original_circuit.copy()
    optimized_after = optimize_circuit_after(circuit_after)
    print("Original Circuit (After Fix):\n", original_circuit)
    print("Optimized Circuit (After Fix):\n", optimized_after)
    print(check_measurements_at_end(optimized_after))

# Run the main function
if __name__ == "__main__":
    main()
