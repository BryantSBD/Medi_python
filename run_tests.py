import pytest
import os
import sys
import subprocess

def get_test_functions(test_file):
    """Extract all test function names from a test file"""
    result = subprocess.run(
        ["pytest", test_file, "--collect-only", "-q"],
        capture_output=True,
        text=True
    )
    
    test_functions = []
    for line in result.stdout.split('\n'):
        if '::' in line and 'test_' in line:
            # Extract test function name (e.g., "TestLogin::test_login_success")
            parts = line.strip().split('::')
            if len(parts) >= 2:
                test_functions.append(f"{test_file}::{parts[-1].strip()}")
    
    return test_functions


def run_individual_tests(test_name=None):
    """
    Run tests with individual HTML reports for each test function.
    Each test gets its own report with the exact test function name.
    
    Usage:
        python run_tests.py                          # Run all tests
        python run_tests.py tests/test_login.py      # Run all tests in that file
        
    Output structure:
        reports/test_login/test_login_success.html
        reports/test_login/test_login_success_failure.png
        reports/test_patient/test_patient_add.html
    """
    
    os.makedirs("reports", exist_ok=True)
    
    if test_name is None:
        # Get all test files from tests directory
        test_files = []
        if os.path.exists("tests"):
            for file in os.listdir("tests"):
                if file.startswith("test_") and file.endswith(".py"):
                    test_files.append(f"tests/{file}")
        
        # Run each test file
        for test_file in sorted(test_files):
            run_individual_tests(test_file)
    else:
        # Extract test filename (example: test_login)
        test_filename = test_name.split("/")[-1].replace(".py", "")
        
        # Create report folder with test filename
        report_dir = f"reports/{test_filename}"
        os.makedirs(report_dir, exist_ok=True)
        
        # Get all test functions in this file
        test_functions = get_test_functions(test_name)
        
        if not test_functions:
            print(f"No test functions found in {test_name}")
            return
        
        # Run each test function individually with its own report
        for test_function in test_functions:
            # Extract just the function name (e.g., "test_login_success")
            func_name = test_function.split("::")[-1]
            
            # Create report path with test function name
            report_path = f"{report_dir}/{func_name}.html"
            
            print(f"\n{'='*60}")
            print(f"Running: {func_name}")
            print(f"Report: {report_path}")
            print(f"{'='*60}")
            
            pytest.main([
                test_function,
                "-v",
                f"--html={report_path}",
                "--self-contained-html",
                "--tb=short"
            ])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Run all tests if no argument provided
        run_individual_tests()
    else:
        run_individual_tests(sys.argv[1])

