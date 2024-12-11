#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

#define NUMBERS 1000000
#define THREAD_COUNT 4

mutex counterLock; // lock for primes
int primes = 0;    // Global count

// ----------------------------------------------------------------------------

// Function to check if a number is prime
int isPrime(int number)
{
    if (number <= 3 && number > 1)
    {
        return 1; // 2 and 3 are prime
    }
    else if (number % 2 == 0 || number % 3 == 0)
    {
        return 0; // Not prime
    }
    else
    {
        for (unsigned int i = 5; i * i <= number; i += 6)
        {
            if (number % i == 0 || number % (i + 2) == 0)
                return 0; // Not prime
        }
        return 1; // Prime
    }
}

// Thread function to find primes in a given range
void findPrimes(int* array, int start, int end) {
    for (int i = start; i < end; ++i) {
        if (isPrime(array[i])) {
            lock_guard<mutex> lock(counterLock); // Lock when modifying shared data
            ++primes;
            cout << array[i] << endl; // Safe to output
        }
    }
}

int main()
{
    srand(42);

    // Create the array of random numbers and assign random values to them
    int *arrayValues = new int[NUMBERS];
    for (int i = 0; i < NUMBERS; i++)
    {
        arrayValues[i] = rand() % 1000000000;
    }

    cout << endl << "Starting findPrimes" << endl;

    // Create an array of threads
    thread threads[THREAD_COUNT];

    // Divide the work among threads
    int chunkSize = NUMBERS / THREAD_COUNT;

    for (int i = 0; i < THREAD_COUNT; ++i) {
        int start = i * chunkSize;
        // Ensure the last thread processes all remaining elements
        int end = (i == THREAD_COUNT - 1) ? NUMBERS : start + chunkSize;
        
        threads[i] = thread(findPrimes, arrayValues, start, end);
    }

    // Wait for all threads to finish
    for (int i = 0; i < THREAD_COUNT; ++i) {
        threads[i].join();
    }

    // Output the total number of primes found
    cout << "\nPrimes found: " << primes << endl;

    delete[] arrayValues; // Clean up memory
    return 0;
}
