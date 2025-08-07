package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	name := os.Getenv("NAME")
	if name == "" {
		name = "World"
	}
	
	message := fmt.Sprintf("Hello, %s!", name)
	fmt.Println(message)
	
	if len(os.Args) > 1 && os.Args[1] == "--verbose" {
		log.Printf("Greeting message: %s", message)
	}
}