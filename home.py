from datetime import datetime, timedelta
import requests
import multiprocessing as mp
import glob
import math

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment
PRIME_POOL_SIZE = 2
WORD_POOL_SIZE  = 2
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 1
NAME_POOL_SIZE  = 2

# Task functions (no change needed)

def is_prime(n: int):
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def task_prime(value, result_primes):
    if is_prime(value):
        formatted_value = f"{value:,}"
        result_primes.append(f'{formatted_value} is prime')
    else:
        formatted_value = f"{value:,}"
        result_primes.append(f'{formatted_value} is not prime')
    return "Done"

def task_word(word, result_words):
    word_found = False
    with open('words.txt', 'r') as words:
        for line in words:
            if word in line:
                word_found = True

    if word_found:
        result_words.append(f'{word} Found')
    else:
        result_words.append(f'{word} not found')
    return "Done"

def task_upper(text, result_upper):
    upper_text = text.upper()
    result_upper.append(f'{text} ==> {upper_text}')
    return "Done"

def task_sum(start_value, end_value, result_sums):
    total = 0
    for i in range(start_value, end_value + 1):
        total += i
    formatted_start_value = f"{start_value:,}"
    formatted_end_value = f"{end_value:,}"
    formatted_total = f"{total:,}"
    result_sums.append(f'sum of {formatted_start_value} to {formatted_end_value} = {formatted_total}')
    return "Done"

def task_name(url, result_names):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result_names.append(f"{url} has name {data['name']}")
    else:
        result_names.append(f"{url} had an error receiving the information (Status code: {response.status_code})")
    return "Done"

# Main function to manage tasks and multiprocessing
def main():
    log = Log(show_terminal=True)
    log.start_timer()

    manager = mp.Manager()
    result_primes = manager.list()
    result_words = manager.list()
    result_upper = manager.list()
    result_sums = manager.list()
    result_names = manager.list()

    pool = mp.Pool(4)  # Adjust pool size as needed

    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        print(task)  # Debugging line
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool.apply_async(task_prime, args=(task['value'], result_primes))
        elif task_type == TYPE_WORD:
            pool.apply_async(task_word, args=(task['word'], result_words))
        elif task_type == TYPE_UPPER:
            pool.apply_async(task_upper, args=(task['text'], result_upper))
        elif task_type == TYPE_SUM:
            pool.apply_async(task_sum, args=(task['start'], task['end'], result_sums))
        elif task_type == TYPE_NAME:
            pool.apply_async(task_name, args=(task['url'], result_names))
        else:
            log.write(f'Error: unknown task type {task_type}')

    # Wait for all tasks to complete
    pool.close()
    pool.join()

    # Log the results
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')

    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')

if __name__ == '__main__':
    main()
