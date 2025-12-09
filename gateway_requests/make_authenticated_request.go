package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"time"
)

func main() {
	// Change these variables
	keyId := "defaulta65ef3a1bb304d10b74ea37b0cb93a64"
	HmacSecret := "NGQyYzNlY2U0YzEwNGFlOWEyNTc5Nzg4MzBmODhmM2Q="

	// Create the signature
	refDate := "Mon, 02 Jan 2006 15:04:05 MST"
	tim := time.Now().UTC().Format(refDate)
	fmt.Println("Date: ")
	fmt.Println(tim)

	signatureString := "date: " + tim

	// SHA256 Encode the signature
	key := []byte(HmacSecret)
	h := hmac.New(sha256.New, key)
	h.Write([]byte(signatureString))

	// // Base64 and URL Encode the string
	sigString := base64.StdEncoding.EncodeToString(h.Sum(nil))
	fmt.Println(sigString)
	encodedString := url.QueryEscape(sigString)

	// // Add the header
	authorizationHeader := fmt.Sprintf("Signature keyId=\"%s\",algorithm=\"hmac-sha256\",headers=\"date\",signature=\"%s\"", keyId, encodedString)
	fmt.Println("Authorization", authorizationHeader)

	// Make an authenticated request
	postBody, _ := json.Marshal(map[string]string{
		"name":  "Toby",
		"email": "Toby@example.com",
	})

	requestBody := bytes.NewBuffer(postBody)
	resp, err := http.NewRequest(http.MethodPost, "http://localhost:8080/public/carrier/webhookTracking", requestBody)
	resp.Header.Add("Date", tim)
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
