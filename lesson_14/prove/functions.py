"""
Course: CSE 251, week 14
File: functions.py
Author: Connor Babb

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family_id = 6128784944
request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
person_id = 2373686152
request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

Without Threads: 136 seconds, 3.7 families per second
With Threads: 36.2 seconds, 13.7 families per second

This function works without threads to retrieve the last family in the stack using pop, and
then adding that to a tree. After that it takes that specific person or child id and then uses that as a parent.
It continues recursively until it reaches the end of the 6th generation.

With threads it works by taking a family and finding all of the individuals it needs, then
it creates a thread for each one of those people, this is done in order so that requests can happen concurrently
and all come back within the same fraction of a second.


Describe how to speed up part 2

Without Threads: 133 seconds, 3.7 families per second
With Threads: 36 seconds, 13 families per second

This works in a similar way to the depth first search, but it uses a queue instead and gets the first family id
from the stack. This tree pattern goes level by level instead(bfs).


Extra (Optional) 10% Bonus to speed up part 3

It is sped up but not as much as parts 1 or 2 given that we can only use 5 threads.
It is sped up the same way but using a semaphore so that there can only be 5 threads to reduce overhead.

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    family_stack = [family_id]
    visited_families = set() # Empty set to keep already processed fams
    threads = []

    while family_stack:
        current_family_id = family_stack.pop()

        if current_family_id in visited_families:
            continue

        visited_families.add(current_family_id)

        family = tree.get_family(current_family_id)

        if family is None:
            family_thread = Request_thread(f"{TOP_API_URL}/family/{current_family_id}")
            family_thread.start()
            threads.append(family_thread)
            family_thread.join()

            family_data = family_thread.get_response()

            new_family = Family(family_data)
            tree.add_family(new_family)
            family = new_family

        def process_person(person_id):
            person_thread = Request_thread(f"{TOP_API_URL}/person/{person_id}")
            person_thread.start()
            threads.append(person_thread)
            person_thread.join()
            person_data = person_thread.get_response()

            if person_data:
                person = Person(person_data)
                tree.add_person(person)

            parent_family_id = person_data.get("parent_id")
            if parent_family_id and parent_family_id not in visited_families:
                family_stack.append(parent_family_id)

        def process_child(child_id):
            child_person = tree.get_person(child_id)
            if child_person:
                child_family_id = child_person.get_familyid()
                if child_family_id and child_family_id not in visited_families:
                    family_stack.append(child_family_id)

        for person_id in [family.get_husband(), family.get_wife()] + family.get_children():
            thread = threading.Thread(target=process_person, args=(person_id,))
            threads.append(thread)
            thread.start()

        for child_id in family.get_children():
            thread = threading.Thread(target=process_child, args=(child_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        threads = []  # Clear threads

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    family_queue = queue.Queue()
    visited_families = set()
    family_queue.put(family_id)

    threads = []

    while not family_queue.empty():
        current_family_id = family_queue.get()

        if current_family_id in visited_families:
            continue
        
        visited_families.add(current_family_id)

        family = tree.get_family(current_family_id)
        if family is None:
            family_thread = Request_thread(f"{TOP_API_URL}/family/{current_family_id}")
            family_thread.start()
            threads.append(family_thread)
            family_thread.join()

            family_data = family_thread.get_response()
            new_family = Family(family_data)
            tree.add_family(new_family)
            family = new_family

        def process_person(person_id):
            person_thread = Request_thread(f"{TOP_API_URL}/person/{person_id}")
            person_thread.start()
            threads.append(person_thread)
            person_thread.join()
            person_data = person_thread.get_response()

            if person_data:
                person = Person(person_data)
                tree.add_person(person)

            parent_family_id = person_data.get("parent_id")
            if parent_family_id and parent_family_id not in visited_families:
                family_queue.put(parent_family_id)

        for person_id in [family.get_husband(), family.get_wife()] + family.get_children():
            thread = threading.Thread(target=process_person, args=(person_id,))
            threads.append(thread)
            thread.start()

        def process_child(child_id):
            child_person = tree.get_person(child_id)
            if child_person:
                child_family_id = child_person.get_familyid()
                if child_family_id and child_family_id not in visited_families:
                    family_queue.put(child_family_id)

        for child_id in family.get_children():
            thread = threading.Thread(target=process_child, args=(child_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        threads = []


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    family_queue = queue.Queue()
    visited_families = set()
    family_queue.put(family_id)

    threads = []

    # Semaphore limits threads to 5
    semaphore = threading.Semaphore(5)

    def process_person(person_id):
        person_thread = Request_thread(f"{TOP_API_URL}/person/{person_id}")
        person_thread.start()
        person_thread.join()
        person_data = person_thread.get_response()

        if person_data:
            person = Person(person_data)
            tree.add_person(person)

        parent_family_id = person_data.get("parent_id")
        if parent_family_id and parent_family_id not in visited_families:
            family_queue.put(parent_family_id)

        semaphore.release()

    def process_child(child_id):
        child_person = tree.get_person(child_id)
        if child_person:
            child_family_id = child_person.get_familyid()
            if child_family_id and child_family_id not in visited_families:
                family_queue.put(child_family_id)

        semaphore.release()

    while not family_queue.empty():
        current_family_id = family_queue.get()

        if current_family_id in visited_families:
            continue
        
        visited_families.add(current_family_id)

        family = tree.get_family(current_family_id)
        if family is None:
            family_thread = Request_thread(f"{TOP_API_URL}/family/{current_family_id}")
            family_thread.start()
            family_thread.join()

            family_data = family_thread.get_response()

            new_family = Family(family_data)
            tree.add_family(new_family)
            family = new_family

        for person_id in [family.get_husband(), family.get_wife()] + family.get_children():
            semaphore.acquire()

            thread = threading.Thread(target=process_person, args=(person_id,))
            threads.append(thread)
            thread.start()

        for child_id in family.get_children():
            semaphore.acquire()

            thread = threading.Thread(target=process_child, args=(child_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        threads = []

