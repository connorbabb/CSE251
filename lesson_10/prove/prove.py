"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can NOT use sleep() statements.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable from the buffer>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def reader(shareable_list, buffer_lock, items_to_read_sem, space_available_sem):
    """Reader process function"""
    while True:
        items_to_read_sem.acquire()

        with buffer_lock:
            tail = shareable_list[BUFFER_SIZE + 1]

            value = shareable_list[tail]
            if value == -1:
                break

            print(value, end=', ', flush=True)

            shareable_list[tail] = 0
            tail = (tail + 1) % BUFFER_SIZE
            shareable_list[BUFFER_SIZE + 1] = tail

            shareable_list[BUFFER_SIZE + 3] += 1

        space_available_sem.release()


def writer(shareable_list, buffer_lock, items_to_read_sem, space_available_sem, items_to_send):
    """Writer process function"""
    for _ in range(items_to_send):
        space_available_sem.acquire()

        with buffer_lock:
            head = shareable_list[BUFFER_SIZE]

            value = shareable_list[BUFFER_SIZE + 2]
            shareable_list[head] = value
            head = (head + 1) % BUFFER_SIZE

            shareable_list[BUFFER_SIZE] = head
            shareable_list[BUFFER_SIZE + 2] += 1

        items_to_read_sem.release()

    for _ in range(READERS):
      with buffer_lock:
          head = shareable_list[BUFFER_SIZE]
          shareable_list[head] = -1
          head = (head + 1) % BUFFER_SIZE
          shareable_list[BUFFER_SIZE] = head

      items_to_read_sem.release()

def main():
    items = random.randint(1000, 10000)
    items_to_send = items // WRITERS

    smm = SharedMemoryManager()
    smm.start()

    with SharedMemoryManager() as smm:
        shared_list = smm.ShareableList([0] * BUFFER_SIZE + [0, 0, 1, 0])  # Buffer, head, tail, and items_revieved

        buffer_lock = mp.Lock()
        items_to_read_sem = mp.Semaphore(0)
        space_available_sem = mp.Semaphore(BUFFER_SIZE)

        writers = [mp.Process(target=writer, args=(shared_list, buffer_lock, items_to_read_sem, space_available_sem, items_to_send)) for _ in range(WRITERS)]
        readers = [mp.Process(target=reader, args=(shared_list, buffer_lock, items_to_read_sem, space_available_sem)) for _ in range(READERS)]

        for w in writers:
            w.start()
        for r in readers:
            r.start()

        for w in writers:
            w.join()

        for r in readers:
            r.join()

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print()
    print(f'{items} values sent')
    print(f'{shared_list[BUFFER_SIZE + 3]} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
