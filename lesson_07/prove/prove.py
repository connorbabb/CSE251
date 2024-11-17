"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: <Add name here>

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

TODO:
I decided 4 for a pool would be a max
Prime: 4 - I know that finding the prime of a large number can take extremely long.
Word: 3 - Searching for a word can also take awhile but shouldn't take as long.
Upper: 1 - Simple function call shouldn't take long at all.
Sum: 3 - Similar to prime but shouldn't take as long.
Name: 3- Can take awhile due to making calls to the url, but there aren't many tasks to work through.

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
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

# base speed: 75-80, highest speed(with these settings) 42 seconds.
PRIME_POOL_SIZE = 4
WORD_POOL_SIZE  = 3
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 3
NAME_POOL_SIZE  = 3

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
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
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        formatted_value = f"{value:,}"
        result_primes.append(f'{formatted_value} is prime')
    else:
        formatted_value = f"{value:,}"
        result_primes.append(f'{formatted_value} is not prime')


def task_word(word, result_words):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    word_found = False
    with open('words.txt', 'r') as words:
        for line in words:
            if word in line:
                word_found = True

    if word_found:
        result_words.append(f'{word} Found')
    else:
        result_words.append(f'{word} not found')


def task_upper(text, result_upper):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    upper_text = text.upper()
    result_upper.append(f'{text} ==> {upper_text}')


def task_sum(start_value, end_value, result_sums):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """
    total = 0
    for i in range(start_value, end_value + 1):
        total += i
    formatted_start_value = f"{start_value:,}"
    formatted_end_value = f"{end_value:,}"
    formatted_total = f"{total:,}"
    result_sums.append(f'sum of {formatted_start_value} to {formatted_end_value} = {formatted_total}')


def task_name(url, result_names):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result_names.append(f"{url} has name {data['name']}")
    else:
        result_names.append(f"{url} had an error receiving the information (Status code: {response.status_code})")


def callback(res):
    pass

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    manager = mp.Manager()
    result_primes = manager.list()
    result_words = manager.list()
    result_upper = manager.list()
    result_sums = manager.list()
    result_names = manager.list()

    prime_pool = mp.Pool(PRIME_POOL_SIZE)
    word_pool = mp.Pool(WORD_POOL_SIZE)
    upper_pool = mp.Pool(UPPER_POOL_SIZE)
    sum_pool = mp.Pool(SUM_POOL_SIZE)
    name_pool = mp.Pool(NAME_POOL_SIZE)

    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(task_prime, args=(task['value'], result_primes), callback=callback)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'], result_words), callback=callback)
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(task_upper, args=(task['text'], result_upper), callback=callback)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'], task['end'], result_sums), callback=callback)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args=(task['url'], result_names), callback=callback)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # Wait for all tasks to complete
    prime_pool.close()
    prime_pool.join()

    word_pool.close()
    word_pool.join()

    upper_pool.close()
    upper_pool.join()

    sum_pool.close()
    sum_pool.join()

    name_pool.close()
    name_pool.join()

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
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