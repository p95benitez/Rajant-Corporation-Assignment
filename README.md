# Rajant-Corporation-Assignment
A simple Python command-line tool developed as part of an internship application assignment. It analyzes Raspberry Pi and Jetson provisioning logs, reports pass/fail status, summarizes errors, and helps engineers quickly identify where provisioning failed.

## Purpose
This program reads a Raspberry Pi or Jetson provisioning log file and prints a summary showing the device name, pass/fail status, number of errors, and error details for troubleshooting.

### Input:
- A provisioning log file provided as a command-line argument.
- Optional --json argument to display the results in JSON format.
### Output:
- Device name
- PASSED or FAILED status
- Error count
- Last successful step before the first error
- List of errors
### Additional Features:
- Returns exit code 0 for success and 1 for failure.
- Supports JSON output using the --json option.
- Handles missing files and invalid log files without crashing.

## How to run it
Run the program from a terminal or command prompt and provide the log file as a command-line argument.
    python provision_check.py <log_file> [--json]
Example command-line argument using test logs provided:
    python provision_check.py test_log_failed.txt --json
    python provision_check.py test_log_passed.txt --json
    python provision_check.py test_log_gibberish.txt --json
    python provision_check.py test_log_invalid_log.txt --json

## My approach
Analyze log line-by-line searching for keywords in the strings to determine if the input is invalid, the device name, the error count, and error descriptions. It determines if the input is invalid by checking if the text contains the string "[INFO] Device:". It determines the deviced name by searching for the string that follows after "[INFO] Device:". It determines the error count and error description by searching for the string "[ERROR]". If there error count is zero, the status is set to PASSED, else the status is set to FAILED. Finally, the program prints the device name, device status, error count and error descriptions.

## Additional Feature
I added a feature that reports the last successful provisioning step before the first error. I chose this because it gives engineers more context about where the provisioning process began to fail, which can make troubleshooting faster.

## If this ran across hundreds of Jetsons, what would you do to make provisioning reliable and easy to troubleshoot?
I would make another program that runes a provision_check.py for each device and combines the outputs into one output that shows the number of devices that passed, the number of devices that failed, and list of the names of the devices that failed. And the program also provides a way to individually access the error log of a devices that failed for further troubleshooting by the device name.

## Which AI tools you used and how
I used ChatGPT. First, I wrote the program in pseudocode and prompted ChatGPT to write a working python code. Then, I verified that the code provided by ChatGPT did what was prompted. Additionally, I prompted ChatGPT to make other example inputs for further testing.
