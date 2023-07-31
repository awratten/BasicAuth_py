# Async Basic Auth Tester

This Python script is an asynchronous login tester that attempts to log in to a web service using basic authentication with multiple username and password combinations. It uses the `aiohttp` library for making asynchronous HTTP requests and the `asyncio` library for managing asynchronous tasks.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `aiohttp` library
- `tqdm` library

You can install the required libraries using the following command:

```
pip install aiohttp tqdm
```

## Usage

1. Replace the `login_url` variable with the actual login URL of the web service you want to test.
2. Replace the `username` variable with the actual username you want to use for testing.
3. Place the list of passwords in a file (e.g., `rockyou.txt`) to use for login attempts. Update the `filename` variable with the path to this file.

## How it works

The script follows these steps:

1. Reads the list of passwords from the specified file in chunks using the `read_credentials_from_file()` function.
2. Sends login requests to the specified `login_url` with each password in the list using the `run_with_semaphore()` function. The `semaphore` is used to control the maximum number of concurrent login attempts.
3. Prints a progress bar using the `tqdm` library to show the status of the login attempts.

## Important Notes

- The script uses asynchronous programming to improve performance by making multiple login attempts concurrently.
- A global flag `login_successful` is used to indicate if a successful login has been achieved. If successful, the script stops processing further credentials.
- The `chunk_size` variable is used to control the number of passwords to read from the file in each chunk. You can adjust this value based on the memory available and performance requirements.
- The `max_workers` variable defines the maximum number of concurrent login attempts. You can change this value according to your needs and system capabilities.

## Running the Script

To run the script, execute the following command in the terminal:

```
python script_name.py
```

Replace `script_name.py` with the name of the Python file containing the provided code.

## Disclaimer

Please use this script responsibly and only on systems that you have explicit permission to test. Unauthorized login attempts can be illegal and may lead to severe consequences. Ensure you have proper authorization from the system owner before using this script.

## Troubleshooting

If you encounter any issues or have questions about using this script, feel free to reach out for support.
