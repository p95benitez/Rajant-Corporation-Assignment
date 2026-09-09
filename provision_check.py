# -----------------------------------------------------------------------------
# Author: Patricio Benitez Palermo, p95benite@gmail.com
# Date: September 9, 2026
# 
# Program: provision_check.py
#
# Purpose:
#   Reads a Raspberry Pi or Jetson provisioning log file and prints a summary
#   showing the device name, pass/fail status, number of errors, and error details.
#
# Input:
#   A provisioning log file provided as a command-line argument.
#   Optional --json argument to display the results in JSON format.
#
# Output:
#   - Device name
#   - PASSED or FAILED status
#   - Error count
#   - List of errors
#
# Additional Features:
#   - Returns exit code 0 for success and 1 for failure.
#   - Supports JSON output using the --json option.
#   - Handles missing files and invalid log files without crashing.
#
# -----------------------------------------------------------------------------


import sys
import json

# Make sure a log file was provided
if len(sys.argv) < 2:
    print("Usage: python provision_check.py <log_file> [--json]")
    sys.exit(1)

log_file = sys.argv[1]

# Check if JSON output was requested
json_output = "--json" in sys.argv

# Initialize variables
error_count = 0
error_list = []
device_status_is_passed = None
str_device_name = "Unknown"
valid_log_line_found = False
last_info_message = None
first_error_previous_step = None

try:
    with open(log_file, "r") as file:

        # Check the file line by line
        for line in file:

            # Remove extra spaces/newlines
            line = line.strip()

            # Check INFO lines
            if line.startswith("[INFO]"):

                info_message = line[len("[INFO]"):]
                last_info_message = info_message

                if info_message.startswith(" Device:"):
                    str_device_name = info_message[len(" Device:"):].strip()
                    valid_log_line_found = True

            # Check ERROR lines
            elif line.startswith("[ERROR]"):

                error_count += 1

                if first_error_previous_step is None:
                    first_error_previous_step = last_info_message

                error_description = line[len("[ERROR]"):].strip()

                error_list.append(error_description)

    # Check if the file appeared to be a valid provisioning log
    if not valid_log_line_found:
        raise ValueError("The provided file does not appear to be a valid provisioning log.")

    # Determine device status
    if error_count == 0:
        device_status_is_passed = True
    else:
        device_status_is_passed = False

    # Convert Boolean status into readable text
    if device_status_is_passed:
        status = "PASSED"
    else:
        status = "FAILED"

    # JSON output
    if json_output:

        result = {
            "device": str_device_name,
            "status": status,
            "error_count": error_count,
            "last_successful_step": first_error_previous_step,
            "errors": error_list
        }

        print(json.dumps(result, indent=4))

    # Normal human-readable output
    else:

        print(f"Device: {str_device_name}")
        print(f"Status: {status}")
        print(f"Errors: {error_count}")

        if first_error_previous_step is not None:
            print(f"Last successful step: {first_error_previous_step}")

        if error_count > 0:
            print("\nErrors:")

            for error in error_list:
                print(error)

    # Exit code
    if device_status_is_passed:
        sys.exit(0)
    else:
        sys.exit(1)

except ValueError as error:
    print(f"Error: {error}")
    sys.exit(1)

except FileNotFoundError:
    print(f"Error: File '{log_file}' was not found.")
    sys.exit(1)