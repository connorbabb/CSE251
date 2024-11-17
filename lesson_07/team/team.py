"""
Course: CSE 251 
Lesson: L07 Team
File:   team.py
Author: Connor, Bryan, and Ryan

Purpose: Retrieve Star Wars details from a server.

Instructions:

1) Make a copy of your lesson 2 prove assignment. Since you are  working in a team for this
   assignment, you can decide which assignment 2 program that you will use for the team activity.

2) You can continue to use the Request_Thread() class that makes the call to the server.

3) Convert the program to use a process pool that uses apply_async() with callback function(s) to
   retrieve data from the Star Wars website. Each request for data must be a apply_async() call;
   this means 1 url = 1 apply_async call, 94 urls = 94 apply_async calls.
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# URL for the Star Wars API
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

def worker_function(url, names):

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        names.append(data['name'])
    else:
        print('RESPONSE = ', response.status_code)
    return data['name']

def main():
    print(f'{datetime.now().strftime('%H:%M:%S')}| Starting to retrieve data from the server')
    print(f'{datetime.now().strftime('%H:%M:%S')}| ----------------------------------------')
    start_time = datetime.now()
    response = requests.get(TOP_API_URL)

    api_urls = response.json()

    film_6_url = api_urls['films'] + '6'
    response = requests.get(film_6_url)
    film_6_data = response.json()

    print(f"{datetime.now().strftime('%H:%M:%S')}| Title   : {film_6_data['title']}")
    print(f"{datetime.now().strftime('%H:%M:%S')}| Director: {film_6_data['director']}")
    print(f"{datetime.now().strftime('%H:%M:%S')}| Producer: {film_6_data['producer']}")
    print(f"{datetime.now().strftime('%H:%M:%S')}| Released: {film_6_data['release_date']}")
    print(f"{datetime.now().strftime('%H:%M:%S')}|")

    categories = ['characters', 'starships', 'vehicles', 'planets', 'species']
    result_dict = {category: [] for category in categories}
    names = []

    def call_back(value):
        print(value)

    pool = mp.Pool(4)
    for category in categories:
        urls = film_6_data[category]
        for url in urls:
            pool.apply_async(worker_function, args=(url, names), callback = call_back)

    for category in categories:
        result_dict[category].sort()
        print(f"{datetime.now().strftime('%H:%M:%S')}| {category.capitalize()}: {len(result_dict[category])}")
        items_line = ', '.join(result_dict[category])
        print(f"{datetime.now().strftime('%H:%M:%S')}| {items_line}")
        print(f'{datetime.now().strftime('%H:%M:%S')}|')

    pool.close()
    pool.join()

    end_time = datetime.now()
    total_time = end_time - start_time
    total_time = total_time.total_seconds()
    print(f'{datetime.now().strftime('%H:%M:%S')}| Total Time To Complete = {total_time:.8f} ')
    print(f'{datetime.now().strftime('%H:%M:%S')}| There were {call_count} calls to swapi server')

if __name__ == "__main__":
    main()
