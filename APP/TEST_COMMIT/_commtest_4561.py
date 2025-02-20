import tensorflow as tf
import numpy as np
import strawberryfields as sf
from strawberryfields.ops import Dgate, Kgate, Sgate, Rgate, BSgate

# Hyperparameters
batch_size = 24
cutoff = 10
disp_clip = 5
kerr_clip = 1
depth_before = 6
depth_after = 4
reps_before = 10  # Number of repetitions before the fix
reps_after = 30  # Number of repetitions after the fix
mode_number = 2

# Simulated random output layer for input_qnn_layer function
output_layer = tf.random.normal([batch_size, 14])


# QNN layer functions with corrected mode targeting for "after" scenario
def input_qnn_layer_before(q):
    Sgate(output_layer[:, 0], output_layer[:, 1]) | q[0]
    Sgate(output_layer[:, 2], output_layer[:, 3]) | q[1]
    BSgate(output_layer[:, 4], output_layer[:, 5]) | (q[0], q[1])
    Rgate(output_layer[:, 6]) | q[0]
    Rgate(output_layer[:, 7]) | q[1]
    Dgate(tf.clip_by_value(output_layer[:, 8], -disp_clip, disp_clip), output_layer[:, 9]) | q[0]
    Dgate(tf.clip_by_value(output_layer[:, 10], -disp_clip, disp_clip), output_layer[:, 11]) | q[0]  # Incorrect target
    Kgate(tf.clip_by_value(output_layer[:, 12], -kerr_clip, kerr_clip)) | q[0]
    Kgate(tf.clip_by_value(output_layer[:, 13], -kerr_clip, kerr_clip)) | q[0]  # Incorrect target


def input_qnn_layer_after(q):
    Sgate(output_layer[:, 0], output_layer[:, 1]) | q[0]
    Sgate(output_layer[:, 2], output_layer[:, 3]) | q[1]
    BSgate(output_layer[:, 4], output_layer[:, 5]) | (q[0], q[1])
    Rgate(output_layer[:, 6]) | q[0]
    Rgate(output_layer[:, 7]) | q[1]
    Dgate(tf.clip_by_value(output_layer[:, 8], -disp_clip, disp_clip), output_layer[:, 9]) | q[0]
    Dgate(tf.clip_by_value(output_layer[:, 10], -disp_clip, disp_clip), output_layer[:, 11]) | q[1]  # Corrected target
    Kgate(tf.clip_by_value(output_layer[:, 12], -kerr_clip, kerr_clip)) | q[0]
    Kgate(tf.clip_by_value(output_layer[:, 13], -kerr_clip, kerr_clip)) | q[1]  # Corrected target


# Standard QNN layer function
def qnn_layer(q, layer_number, bs_variables, phase_variables, sq_magnitude_variables, sq_phase_variables,
              disp_magnitude_variables, disp_phase_variables, kerr_variables):
    BSgate(bs_variables[layer_number, 0, 0, 0], bs_variables[layer_number, 0, 0, 1]) | (q[0], q[1])
    for i in range(2):
        Rgate(phase_variables[layer_number, i, 0]) | q[i]
    for i in range(2):
        Sgate(tf.clip_by_value(sq_magnitude_variables[layer_number, i], -5, 5), sq_phase_variables[layer_number, i]) | \
        q[i]
    BSgate(bs_variables[layer_number, 0, 1, 0], bs_variables[layer_number, 0, 1, 1]) | (q[0], q[1])
    for i in range(2):
        Rgate(phase_variables[layer_number, i, 1]) | q[i]
    for i in range(2):
        Dgate(tf.clip_by_value(disp_magnitude_variables[layer_number, i], -disp_clip, disp_clip),
              disp_phase_variables[layer_number, i]) | q[i]
    for i in range(2):
        Kgate(tf.clip_by_value(kerr_variables[layer_number, i], -kerr_clip, kerr_clip)) | q[i]


# Testing function for "before" and "after" scenarios
def test_qnn_layers_before():
    # Initialize parameters
    bs_variables = tf.random.normal([depth_before, 1, 2, 2])
    phase_variables = tf.random.normal([depth_before, 2, 2])
    sq_magnitude_variables = tf.random.normal([depth_before, 2])
    sq_phase_variables = tf.random.normal([depth_before, 2])
    disp_magnitude_variables = tf.random.normal([depth_before, 2])
    disp_phase_variables = tf.random.normal([depth_before, 2])
    kerr_variables = tf.random.normal([depth_before, 2])

    # Construct the engine-based structure
    """eng, q = sf.Engine(num_subsystems=2)

    with eng:
        input_qnn_layer_before(q)
        for i in range(depth_before):
            qnn_layer(q, i, bs_variables, phase_variables, sq_magnitude_variables, sq_phase_variables,
                      disp_magnitude_variables, disp_phase_variables, kerr_variables)"""
    # Construct the engine-based structure using Program context for "before"
    prog_before = sf.Program(mode_number)
    with prog_before.context as q:
        input_qnn_layer_before(q)
        for i in range(depth_before):
            qnn_layer(q, i, bs_variables, phase_variables, sq_magnitude_variables, sq_phase_variables,
                      disp_magnitude_variables, disp_phase_variables, kerr_variables)

    # Create an engine and run the program for reps_before
    eng_before = sf.Engine("tf", backend_options={"cutoff_dim": cutoff, "batch_size": batch_size})
    for rep in range(reps_before):
        state_before = eng_before.run(prog_before, run_options={"eval": False}).state
        print(f"Before fix - Quantum state shape at rep {rep + 1}: {state_before.dm().shape}")

    """# Run the engine with specific backend options for reps_before
    for rep in range(reps_before):
        state_before = eng.run("tf", cutoff_dim=cutoff, eval=False, batch_size=batch_size).state
        print(f"Before fix - Quantum state shape at rep {rep + 1}: {state_before.dm().shape}")"""


def test_qnn_layers_after():
    # Initialize parameters
    bs_variables = tf.random.normal([depth_after, 1, 2, 2])
    phase_variables = tf.random.normal([depth_after, 2, 2])
    sq_magnitude_variables = tf.random.normal([depth_after, 2])
    sq_phase_variables = tf.random.normal([depth_after, 2])
    disp_magnitude_variables = tf.random.normal([depth_after, 2])
    disp_phase_variables = tf.random.normal([depth_after, 2])
    kerr_variables = tf.random.normal([depth_after, 2])

    # Construct the program-based structure
    prog = sf.Program(mode_number)
    with prog.context as q:
        input_qnn_layer_after(q)
        for i in range(depth_after):
            qnn_layer(q, i, bs_variables, phase_variables, sq_magnitude_variables, sq_phase_variables,
                      disp_magnitude_variables, disp_phase_variables, kerr_variables)

    # Create and run the engine on the program with TensorFlow backend for reps_after
    eng = sf.Engine("tf", backend_options={"cutoff_dim": cutoff, "batch_size": batch_size})
    for rep in range(reps_after):
        state_after = eng.run(prog, run_options={"eval": False}).state
        print(f"After fix - Quantum state shape at rep {rep + 1}: {state_after.dm().shape}")


# Main function to execute the test
def main():
    print("Starting QNN layer test for 'before' bug fix scenario...\n")
    test_qnn_layers_before()

    print("\nStarting QNN layer test for 'after' bug fix scenario...\n")
    test_qnn_layers_after()

    print("\nQNN layer testing completed for both scenarios.")


# Execute main function
if __name__ == "__main__":
    main()
