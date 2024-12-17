"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = 'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE = 'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting(id):
    print(f'Cleaner: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting(id):
    print(f'Guest: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(lock, cleaned_count, start_time):
    while time.time() - start_time < TIME:
        cleaner_waiting(mp.current_process().name[8])
        with lock:
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(mp.current_process().name[8])
            print(STOPPING_CLEANING_MESSAGE)
            cleaned_count.value += 1
        time.sleep(random.uniform(0, 2))

def guest(lock, party_count, start_time):
    while time.time() - start_time < TIME:
        guest_waiting(int(mp.current_process().name[8]) - 2)
        with lock:
            print(STARTING_PARTY_MESSAGE)
            guest_partying(int(mp.current_process().name[8]) - 2, party_count.value)
            print(STOPPING_PARTY_MESSAGE)
            party_count.value += 1
        time.sleep(random.uniform(0, 2))

def main():
    lock = mp.Lock()
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)
    
    start_time = time.time()
    
    cleaners = [mp.Process(target=cleaner, args=(lock, cleaned_count, start_time)) for _ in range(CLEANING_STAFF)]
    guests = [mp.Process(target=guest, args=(lock, party_count, start_time)) for _ in range(HOTEL_GUESTS)]
    
    for cleaner_process in cleaners:
        cleaner_process.start()
    for guest_process in guests:
        guest_process.start()

    for cleaner_process in cleaners:
        cleaner_process.join()
    for guest_process in guests:
        guest_process.join()

    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')

if __name__ == '__main__':
    main()
