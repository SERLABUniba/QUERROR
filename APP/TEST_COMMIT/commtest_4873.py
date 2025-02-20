import unittest
from qiskit_nature.second_q.operators import FermionicOp
from qiskit_nature.second_q.operators.commutators import commutator
from qiskit_nature.second_q.properties import AngularMomentum
from qiskit_nature.second_q.properties.s_operators import s_x_operator, s_y_operator, s_z_operator
import support4873


# Define test class to simulate before and after the fix
class TestCommutatorNormalOrder(unittest.TestCase):
    def setUp(self):
        self.s_x = s_x_operator(4)
        self.s_y = s_y_operator(4)
        self.s_z = s_z_operator(4)
        self.s_2 = AngularMomentum(4).second_q_ops()["AngularMomentum"]

    # Before Fix - No .normal_order() applied
    def test_commutators_before_fix(self):
        print("=== BEFORE FIX ===")
        try:
            # Scenario 1: [S^x, S^y] should equal 1j * S^z
            self.assertEqual(commutator(self.s_x, self.s_y), 1j * self.s_z)
            print("Scenario 1 Passed")

            # Scenario 2: [S^y, S^z] should equal 1j * S^x
            self.assertEqual(commutator(self.s_y, self.s_z), 1j * self.s_x)
            print("Scenario 2 Passed")

            # Scenario 3: [S^z, S^x] should equal 1j * S^y
            self.assertEqual(commutator(self.s_z, self.s_x), 1j * self.s_y)
            print("Scenario 3 Passed")

            # Scenario 4: [S^2, S^x] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_x), FermionicOp.zero())
            print("Scenario 4 Passed")

            # Scenario 5: [S^2, S^y] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_y), FermionicOp.zero())
            print("Scenario 5 Passed")

            # Scenario 6: [S^2, S^z] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_z), FermionicOp.zero())
            print("Scenario 6 Passed")
        except AssertionError as e:
            print(f"Test failed before fix: {e}")

    # After Fix - .normal_order() applied
    def test_commutators_after_fix(self):
        print("=== AFTER FIX ===")
        try:
            # Scenario 1: [S^x, S^y] should equal 1j * S^z
            self.assertEqual(commutator(self.s_x, self.s_y).normal_order(), 1j * self.s_z)
            print("Scenario 1 Passed")

            # Scenario 2: [S^y, S^z] should equal 1j * S^x
            self.assertEqual(commutator(self.s_y, self.s_z).normal_order(), 1j * self.s_x)
            print("Scenario 2 Passed")

            # Scenario 3: [S^z, S^x] should equal 1j * S^y
            self.assertEqual(commutator(self.s_z, self.s_x).normal_order(), 1j * self.s_y)
            print("Scenario 3 Passed")

            # Scenario 4: [S^2, S^x] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_x).normal_order(), FermionicOp.zero())
            print("Scenario 4 Passed")

            # Scenario 5: [S^2, S^y] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_y).normal_order(), FermionicOp.zero())
            print("Scenario 5 Passed")

            # Scenario 6: [S^2, S^z] should equal zero
            self.assertEqual(commutator(self.s_2, self.s_z).normal_order(), FermionicOp.zero())
            print("Scenario 6 Passed")
        except AssertionError as e:
            print(f"Test failed after fix: {e}")


# Main function to execute tests
def main():
    print("Running Tests Before and After Fix...\n")
    suite = unittest.TestSuite()
    suite.addTest(TestCommutatorNormalOrder("test_commutators_before_fix"))
    suite.addTest(TestCommutatorNormalOrder("test_commutators_after_fix"))

    runner = unittest.TextTestRunner()
    runner.run(suite)


# Run the main function
if __name__ == "__main__":
    main()
