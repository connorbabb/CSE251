"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Connor Babb

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

"""

from datetime import datetime, timedelta
import requests
import json
import threading

# URL for the Star Wars API
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

class Request_Thread(threading.Thread):
    
    def __init__(self, url, result_list, name):
        threading.Thread.__init__(self)
        self.url = url
        self.result_list = result_list
        self.name = name

    def run(self):
        global call_count
        response = requests.get(self.url)
        self.status_code = response.status_code
        if response.status_code == 200:
            data = response.json()
            self.result_list.append(data['name'])
            call_count += 1
        else:
            print('RESPONSE = ', response.status_code)

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
    threads = []

    for category in categories:
        urls = film_6_data[category]
        for url in urls:
            thread = Request_Thread(url, result_dict[category], category)
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    for category in categories:
        result_dict[category].sort()
        print(f"{datetime.now().strftime('%H:%M:%S')}| {category.capitalize()}: {len(result_dict[category])}")
        items_line = ', '.join(result_dict[category])
        print(f"{datetime.now().strftime('%H:%M:%S')}| {items_line}")
        print(f'{datetime.now().strftime('%H:%M:%S')}|')

    end_time = datetime.now()
    total_time = end_time - start_time
    total_time = total_time.total_seconds()
    print(f'{datetime.now().strftime('%H:%M:%S')}| Total Time To Complete = {total_time:.8f} ')
    print(f'{datetime.now().strftime('%H:%M:%S')}| There were {call_count} calls to swapi server')

if __name__ == "__main__":
    main()
