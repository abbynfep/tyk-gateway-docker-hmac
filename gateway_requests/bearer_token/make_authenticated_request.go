package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	// Change these variables
	keyId := "default37ff84093fd141eba2c515467f05520f"
	//

	// Create the signature
	authorizationHeader := fmt.Sprintf("Bearer %s", keyId)
	fmt.Println("Authorization header: ", authorizationHeader)

	// Make an authenticated request
	postBody, _ := json.Marshal(map[string]string{
		"name":  "Toby",
		"email": "Toby@example.com",
	})

	requestBody := bytes.NewBuffer(postBody)
	resp, err := http.NewRequest(http.MethodPost, "http://localhost:8080/tokenWebhook", requestBody)
	resp.Header.Add("Authorization", authorizationHeader)
	resp.Header.Add("Content-Type", "application/json")

	response, err := http.DefaultClient.Do(resp)

	//Handle Error
	if err != nil {
		log.Fatalf("An Error Occured %v", err)
	}
	defer response.Body.Close()
	//Read the response body
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatalln(err)
	}
	sb := string(body)
	log.Printf(sb)
}
