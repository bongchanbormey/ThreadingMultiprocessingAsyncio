import asyncio
import multiprocessing
import requests

# Function to check if a number is prime
def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while (i * i) <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to check a chunk of numbers for primality
def check_prime_chunk(numbers):
    """Check a chunk of numbers for primality."""
    primes = [n for n in numbers if is_prime(n)]
    return primes

# Function to download the file and find prime numbers
def find_primes_in_range(file_url, chunk_size):
    """Download the file and find prime numbers in chunks."""
    response = requests.get(file_url)
    numbers = [int(line.strip()) for line in response.text.splitlines() if line.strip()]
    
    with multiprocessing.Pool() as pool:
        # Divide numbers into chunks
        chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
        results = pool.map(check_prime_chunk, chunks)
    
    # Flatten the list of results
    primes = [prime for sublist in results for prime in sublist]
    return primes

# Async function to write data to a file
async def async_write_to_file(filename, data):
    """Asynchronously write data to a file."""
    await asyncio.to_thread(write_to_file, filename, data)

# Blocking function to write data to a file
def write_to_file(filename, data):
    """Write data to a file (blocking)."""
    with open(filename, 'w') as f:
        for number in data:
            f.write(f"{number}\n")

# Async function to run file writing tasks
async def run_async_tasks(primes):
    """Run multiple asynchronous file writing tasks."""
    tasks = []
    chunk_size = 100  # Define how many primes per file
    for i in range(0, len(primes), chunk_size):
        chunk = primes[i:i + chunk_size]
        filename = f"primes_{i // chunk_size}.txt"
        tasks.append(async_write_to_file(filename, chunk))
    await asyncio.gather(*tasks)


def main():
    # Github raw url to num_file.txt
    file_url = "https://raw.githubusercontent.com/bongchanbormey/ThreadingMultiprocessingAsyncio/refs/heads/main/num_file.txt"
    chunk_size = 100 

    # Find prime numbers
    primes = find_primes_in_range(file_url, chunk_size)
    
    print(f"Found {len(primes)} prime numbers.")

    # Run the async file writing tasks
    asyncio.run(run_async_tasks(primes))

if __name__ == "__main__":
    main()