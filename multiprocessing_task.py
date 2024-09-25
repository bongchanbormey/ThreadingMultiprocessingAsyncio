import multiprocessing
import requests

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

def check_prime_chunk(numbers):
    """Check a chunk of numbers for primality."""
    primes = [n for n in numbers if is_prime(n)]
    non_primes = [n for n in numbers if n not in primes]
    return primes, non_primes

def find_primes_in_range(file_url, chunk_size):
    """Download the file and find prime numbers in chunks."""
    response = requests.get(file_url)
    numbers = []
    for line in response.text.splitlines():
        line = line.strip()
        if line:  # Only process non-empty lines
            numbers.append(int(line))
    
    with multiprocessing.Pool() as pool:
        # Divide numbers into chunks
        chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
        results = pool.map(check_prime_chunk, chunks)
    
    # Flatten the list of results and separate primes and non-primes numbers
    primes = []
    non_primes = []
    for prime_list, non_prime_list in results:
        primes.extend(prime_list)
        non_primes.extend(non_prime_list)

    return primes, non_primes, numbers

def main():
    # Corrected URL to the raw content of the numbers.txt file
    file_url = "https://raw.githubusercontent.com/bongchanbormey/ThreadingMultiprocessingAsyncio/refs/heads/main/num_file.txt"
    chunk_size = 100  

    primes, non_primes, all_numbers = find_primes_in_range(file_url, chunk_size)

    print(f"Found {len(primes)} prime numbers.")
    print(f"Found {len(non_primes)} non-prime numbers.")
    
    # Prompt the user for a number
    user_input = input("Type a number to check if it's prime: ")
    
    try:
        user_number = int(user_input)
        if user_number in all_numbers:
            if user_number in primes:
                print(f"{user_number} is a prime number.")
            else:
                print(f"{user_number} is a non-prime number.")
        else:
            print("Not existing.")
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()