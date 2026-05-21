import pytest
import os
import sys

def run_test(test_name):
    # Extract simple name (example: test_login)
    simple_name = test_name.split("/")[-1].replace(".py", "")
    
    # Remove 'test_' prefix
    module_name = simple_name.replace("test_", "").capitalize()

    # Create report folder
    report_dir = f"reports/{module_name}"
    os.makedirs(report_dir, exist_ok=True)

    # Create report file
    report_path = f"{report_dir}/{module_name}.html"

    pytest.main([
        test_name,
        "-v",
        f"--html={report_path}",
        "--self-contained-html"
    ])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py tests/test_login.py")
    else:
        run_test(sys.argv[1])

