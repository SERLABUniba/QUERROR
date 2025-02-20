from qiskit.circuit import QuantumCircuit, Parameter
import numpy as np


class MockSamplerQNNBefore:
    """Mock class simulating the behavior of SamplerQNN before the bug fix."""

    def __init__(self, circuit: QuantumCircuit):
        self._circuit = circuit.copy()  # Direct copy of the original circuit
        if len(self._circuit.clbits) == 0:
            self._circuit.measure_all()  # Adds measurement if no classical bits are present

    @property
    def circuit(self):
        """Return the underlying circuit used."""
        return self._circuit

    def compute_output_shape(self):
        """Calculate output shape using _circuit's num_qubits as in before."""
        return (2 ** self._circuit.num_qubits,)


class MockSamplerQNNAfter:
    """Mock class simulating the behavior of SamplerQNN after the bug fix."""

    def __init__(self, circuit: QuantumCircuit):
        self._org_circuit = circuit  # Store original circuit
        if len(circuit.clbits) == 0:
            circuit = circuit.copy()
            circuit.measure_all()  # Adds measurement if no classical bits are present
        self._circuit = circuit  # Save reparameterized circuit if needed

    @property
    def circuit(self):
        """Return the underlying original circuit."""
        return self._org_circuit

    def compute_output_shape(self):
        """Calculate output shape using circuit's num_qubits as in after."""
        return (2 ** self.circuit.num_qubits,)


def test_scenario():
    # Create a simple QuantumCircuit without classical bits for testing
    param_x = Parameter("x")
    test_circuit = QuantumCircuit(1)
    test_circuit.rx(param_x, 0)

    # Scenario 1: Testing with MockSamplerQNNBefore (before the fix)
    print("Testing 'before' fix scenario...")
    model_before = MockSamplerQNNBefore(test_circuit)
    print("Circuit after 'before' fix processing:")
    print(model_before.circuit)
    print("Measurement present (before fix):", any(op[0].name == "measure" for op in model_before.circuit.data))
    print("Output shape (before fix):", model_before.compute_output_shape())

    # Scenario 2: Testing with MockSamplerQNNAfter (after the fix)
    print("\nTesting 'after' fix scenario...")
    model_after = MockSamplerQNNAfter(test_circuit)
    print("Circuit after 'after' fix processing (original circuit returned):")
    print(model_after.circuit)
    print("Measurement present in _circuit (after fix):",
          any(op[0].name == "measure" for op in model_after._circuit.data))
    print("Output shape (after fix):", model_after.compute_output_shape())

    # Verifying that _org_circuit does not have measurement
    print("Measurement present in _org_circuit (after fix):",
          any(op[0].name == "measure" for op in model_after.circuit.data))


# Main function to execute the test
def main():
    print("Starting test framework for SamplerQNN modifications...\n")
    test_scenario()
    print("\nTesting completed.")


# Run the main function
if __name__ == "__main__":
    main()
