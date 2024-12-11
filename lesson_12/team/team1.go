/*
	-----------------------------------------------------------

Course: CSE 251
Lesson Week: 12
File: team1.go

Purpose: Process URLs

Instructions:

Part 1
- Take this program and use goroutines for the function getPerson().

Part 2
  - Create a function "getSpecies()" that will receive the following urls
    using that function as a goroutine.
  - For a species, display name, average_height and language

"http://swapi.dev/api/species/1/",
"http://swapi.dev/api/species/2/",
"http://swapi.dev/api/species/3/",
"http://swapi.dev/api/species/6/",
"http://swapi.dev/api/species/15/",
"http://swapi.dev/api/species/19/",
"http://swapi.dev/api/species/20/",
"http://swapi.dev/api/species/23/",
"http://swapi.dev/api/species/24/",
"http://swapi.dev/api/species/25/",
"http://swapi.dev/api/species/26/",
"http://swapi.dev/api/species/27/",
"http://swapi.dev/api/species/28/",
"http://swapi.dev/api/species/29/",
"http://swapi.dev/api/species/30/",
"http://swapi.dev/api/species/33/",
"http://swapi.dev/api/species/34/",
"http://swapi.dev/api/species/35/",
"http://swapi.dev/api/species/36/",
"http://swapi.dev/api/species/37/",

-----------------------------------------------------------
*/
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

type Person struct {
	Birth_year string
	Created    time.Time
	Edited     time.Time
	Eye_color  string
	Films      []string
	Gender     string
	Hair_color string
	Height     string
	Homeworld  string
	Mass       string
	Name       string
	Skin_color string
	Species    []string
	Starships  []string
	Url        string
	Vehicles   []string
}

func getPerson(url string, wg *sync.WaitGroup) {
	// Ensure Done is called even if an error occurs
	defer wg.Done()

	// Make an HTTP GET request
	res, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching URL %s: %v\n", url, err)
		return
	}
	defer res.Body.Close()

	// Read all response body
	data, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Printf("Error reading response body for URL %s: %v\n", url, err)
		return
	}

	// Unmarshal the JSON data into the Person struct
	var person Person
	jsonErr := json.Unmarshal(data, &person)
	if jsonErr != nil {
		log.Printf("Error parsing JSON for URL %s: %v\n", url, jsonErr)
		return
	}

	// Print the person details
	fmt.Println("-----------------------------------------------")
	fmt.Println("Name      : ", person.Name)
	fmt.Println("Birth     : ", person.Birth_year)
	fmt.Println("Eye color : ", person.Eye_color)
}

func getSpecies(url string, wg *sync.WaitGroup) {
	// Ensure Done is called even if an error occurs
	defer wg.Done()

	// Make an HTTP GET request
	res, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching URL %s: %v\n", url, err)
		return
	}
	defer res.Body.Close()

	// Read all response body
	data, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Printf("Error reading response body for URL %s: %v\n", url, err)
		return
	}

	// Unmarshal the JSON data into the Person struct
	var person Person
	jsonErr := json.Unmarshal(data, &person)
	if jsonErr != nil {
		log.Printf("Error parsing JSON for URL %s: %v\n", url, jsonErr)
		return
	}

	// Print the person details
	fmt.Println("-----------------------------------------------")
	fmt.Println("Species      : ", person.Species)
}

func main() {
	fmt.Println("Starting...")

	// List of URLs to fetch
	urls := []string{
		"http://swapi.dev/api/people/1/",
		"http://swapi.dev/api/people/2/",
		"http://swapi.dev/api/people/3/",
		"http://swapi.dev/api/people/4/",
		"http://swapi.dev/api/people/5/",
		"http://swapi.dev/api/people/6/",
		"http://swapi.dev/api/people/7/",
		"http://swapi.dev/api/people/8/",
		"http://swapi.dev/api/people/9/",
		"http://swapi.dev/api/people/10/",
		"http://swapi.dev/api/people/12/",
		"http://swapi.dev/api/people/13/",
		"http://swapi.dev/api/people/14/",
		"http://swapi.dev/api/people/15/",
		"http://swapi.dev/api/people/16/",
		"http://swapi.dev/api/people/18/",
		"http://swapi.dev/api/people/19/",
		"http://swapi.dev/api/people/81/",
	}
	urls2 := []string{
		"http://swapi.dev/api/species/1/",
		"http://swapi.dev/api/species/2/",
		"http://swapi.dev/api/species/3/",
		"http://swapi.dev/api/species/6/",
		"http://swapi.dev/api/species/15/",
		"http://swapi.dev/api/species/19/",
		"http://swapi.dev/api/species/20/",
		"http://swapi.dev/api/species/23/",
		"http://swapi.dev/api/species/24/",
		"http://swapi.dev/api/species/25/",
		"http://swapi.dev/api/species/26/",
		"http://swapi.dev/api/species/27/",
		"http://swapi.dev/api/species/28/",
		"http://swapi.dev/api/species/29/",
		"http://swapi.dev/api/species/30/",
		"http://swapi.dev/api/species/33/",
		"http://swapi.dev/api/species/34/",
		"http://swapi.dev/api/species/35/",
		"http://swapi.dev/api/species/36/",
		"http://swapi.dev/api/species/37/",
	}

	// Create a WaitGroup to wait for all goroutines to complete
	var wg sync.WaitGroup

	for _, url := range urls {
		wg.Add(1)
		go getPerson(url, &wg) // Launch each fetch in a goroutine
	}
	for _, url := range urls2 {
		wg.Add(1)
		go getSpecies(url, &wg) // Launch each fetch in a goroutine
	}

	// Wait for all goroutines to complete
	wg.Wait()

	fmt.Println("All done!")
}
