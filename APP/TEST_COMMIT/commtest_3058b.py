from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


# Mock class simulating the `SamplerQNN` before the fix
class SamplerQNNBeforeFix:
    def __init__(self, circuit: QuantumCircuit):
        # Make a copy to simulate the original, unmodified circuit state
        self._original_circuit = circuit.copy()
        # Only one circuit variable, which may get modified directly
        self._circuit = circuit  # direct reference without a backup copy
        # If no classical bits, add measurement to the circuit directly
        if len(self._circuit.clbits) == 0:
            self._circuit.measure_all()  # modifies the only version of the circuit

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit

    @property
    def original_circuit(self) -> QuantumCircuit:
        return self._original_circuit  # Returns the unmodified copy for reference

    def modify_circuit(self):
        # Simulate modification to the circuit during processing
        self._circuit.h(0)  # Add a Hadamard gate to the first qubit

    def get_output_shape(self):
        # Calculate the output shape based on _circuit.num_qubits
        return (2 ** self._circuit.num_qubits,)


# Mock class simulating the `SamplerQNN` after the fix
class SamplerQNNAfterFix:
    def __init__(self, circuit: QuantumCircuit):
        # Store the original unmodified circuit
        self._org_circuit = circuit

        # Create a modified version of the circuit for measurement, if needed
        if len(circuit.clbits) == 0:
            temp_circuit = circuit.copy()
            temp_circuit.measure_all()  # adds measurement only to _circuit
            self._circuit = temp_circuit
        else:
            self._circuit = circuit

    @property
    def circuit(self) -> QuantumCircuit:
        return self._org_circuit  # returns the unmodified original circuit

    @property
    def measured_circuit(self) -> QuantumCircuit:
        return self._circuit  # returns the modified circuit with measurements

    def modify_circuit(self):
        # Simulate modification to the circuit during processing
        self._circuit.h(0)  # Add a Hadamard gate to the first qubit

    def get_output_shape(self):
        # Calculate the output shape based on _circuit.num_qubits
        return (2 ** self._circuit.num_qubits,)


# Testing Function to Show the Difference in Outputs

def test_circuit_handling():
    # Create a sample quantum circuit with no classical bits
    param = Parameter('θ')
    sample_circuit = QuantumCircuit(2)
    sample_circuit.rx(param, 0)
    sample_circuit.ry(param, 1)

    # Test Before Fix
    print("Testing Before Fix:")
    qnn_before = SamplerQNNBeforeFix(sample_circuit)
    print("Original Circuit Copy (circuit) before measurement:")
    print(qnn_before.original_circuit)  # This should show the circuit without measurements
    print("Circuit with Measurement (_circuit):")
    print(qnn_before.circuit)  # Shows the circuit with measurements added
    print("Output Shape:", qnn_before.get_output_shape())

    # Modify circuit and display effect on original circuit in the "before" case
    qnn_before.modify_circuit()
    print("\nAfter Modification (Before Fix):")
    print("Modified Circuit (_circuit):")
    print(qnn_before._circuit)  # Shows circuit after Hadamard gate modification
    print("Original Circuit Copy after Modification:")
    print(qnn_before.circuit)  # This should return the modified copy since it is a direct reference

    print("\n" + "-" * 30 + "\n")

    # Test After Fix
    # Re-create sample_circuit for clean testing
    sample_circuit = QuantumCircuit(2)
    sample_circuit.rx(param, 0)
    sample_circuit.ry(param, 1)

    print("Testing After Fix:")
    qnn_after = SamplerQNNAfterFix(sample_circuit)
    print("Original Circuit (_org_circuit) before measurement:")
    print(qnn_after.circuit)  # This should show the unmodified original circuit
    print("Circuit with Measurement (_circuit):")
    print(qnn_after.measured_circuit)  # Shows the circuit with measurements added
    print("Output Shape:", qnn_after.get_output_shape())

    # Modify circuit and display effect on original circuit in the "after" case
    qnn_after.modify_circuit()
    print("\nAfter Modification (After Fix):")
    print("Measured Circuit After Modification (_circuit):")
    print(qnn_after.measured_circuit)  # Shows circuit after Hadamard gate modification
    print("Original Circuit (_org_circuit) after Modification:")
    print(qnn_after.circuit)  # This should remain unchanged


# Execute test function
if __name__ == "__main__":
    test_circuit_handling()
