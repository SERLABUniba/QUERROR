import pennylane as qml

# Define a quantum device
dev = qml.device("default.qubit", wires=3)

# Define the function with the given gate sequence
@qml.qnode(dev)
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
    qml.PauliY(wires=2)
    qml.CY(wires=[1, 2])
    return qml.expval(qml.PauliZ(0))

# Set example parameter values
x_val, y_val, z_val = 0.5, 1.2, 0.8

# Draw the circuit
print(qml.draw(qfunc)(x_val, y_val, z_val))
