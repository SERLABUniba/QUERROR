class MockUCC:
    def __init__(self, num_spatial_orbitals, num_particles):
        self.num_spatial_orbitals = num_spatial_orbitals
        self.num_particles = num_particles
        self._generalized = False  # Assume `_generalized` is False to trigger checks

    # Before Fix: Original configuration check
    def _check_ucc_configuration_before(self, raise_on_failure=True):
        if not self._generalized:
            if any(n >= self.num_spatial_orbitals for n in self.num_particles):
                if raise_on_failure:
                    raise ValueError(
                        f"The number of spatial orbitals {self.num_spatial_orbitals} "
                        f"must be greater than number of particles of any spin kind "
                        f"{self.num_particles}."
                    )
            return False
        return True

    # After Fix: Updated configuration check with specific conditions
    def _check_ucc_configuration_after(self, raise_on_failure=True):
        if not self._generalized:
            if all(n == self.num_spatial_orbitals for n in self.num_particles):
                if raise_on_failure:
                    raise ValueError(
                        f"UCC calculations for fully occupied alpha and beta orbitals "
                        f"is still not implemented. The current system contains "
                        f"{self.num_spatial_orbitals} orbitals for {self.num_particles} "
                        f"(alpha, beta) particles."
                    )
                return False
            if any(n > self.num_spatial_orbitals for n in self.num_particles):
                if raise_on_failure:
                    raise ValueError(
                        f"The number of spatial orbitals {self.num_spatial_orbitals} "
                        f"must be greater than number of particles of any spin kind "
                        f"{self.num_particles}."
                    )
            return False
        return True

# Test framework
def run_test_scenario(mock_ucc, description, use_after_fix):
    print(f"Running Test: {description}")
    try:
        if use_after_fix:
            mock_ucc._check_ucc_configuration_after()
        else:
            mock_ucc._check_ucc_configuration_before()
        print("Result: No errors.")
    except ValueError as e:
        print(f"Result: Caught ValueError - {str(e)}")
    print("-" * 50)

# Test cases
def main():
    # Scenario 1: All particles lass than spatial orbitals - Should trigger No errors
    mock_ucc1 = MockUCC(num_spatial_orbitals=5, num_particles=[3, 4])

    # Scenario 2: Any particle number exceeding spatial orbitals - Should trigger the exceeded limit error
    mock_ucc2 = MockUCC(num_spatial_orbitals=5, num_particles=[4, 6])

    # Scenario 3: All particles equal to spatial orbitals - Should trigger the fully occupied error
    mock_ucc3 = MockUCC(num_spatial_orbitals=5, num_particles=[5, 5])

    print("Testing before fix (Original Logic):")
    run_test_scenario(mock_ucc1, "All particles less than spatial orbitals", use_after_fix=False)
    run_test_scenario(mock_ucc2, "Any particle exceeds spatial orbitals", use_after_fix=False)
    run_test_scenario(mock_ucc3, "All particles equal to spatial orbitals", use_after_fix=False)

    print("\nTesting after fix (Updated Logic):")
    run_test_scenario(mock_ucc1, "All particles less than spatial orbitals", use_after_fix=True)
    run_test_scenario(mock_ucc2, "Any particle exceeds spatial orbitals", use_after_fix=True)
    run_test_scenario(mock_ucc3, "All particles equal to spatial orbitals", use_after_fix=True)

# Run the main function to execute tests
if __name__ == "__main__":
    main()
