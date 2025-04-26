"""Test runner script for Discord Truth Social Bot."""

import sys
import pytest

def main():
    """Run the test suite."""
    args = sys.argv[1:]
    
    # Default arguments for pytest
    pytest_args = [
        "-v",  # Verbose output
        "--asyncio-mode=auto",  # Handle async tests
        "-s",  # Show print statements
    ]
    
    # If specific tests are specified, add them to args
    if args:
        pytest_args.extend(args)
    else:
        # Run all tests in the tests directory
        pytest_args.append("tests/")
    
    # Run pytest with our arguments
    sys.exit(pytest.main(pytest_args))

if __name__ == "__main__":
    main() 