package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"io/ioutil"
	"net/http"
	"os"
)

// The beginning of the web server program.
func main() {
	if err := run(); err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(1)
	}
}

// Used to generate the HTML website
type executeData struct {
	Data
	Err error
}
type Data map[string]interface{}

// loadData reads a json file and unmarshalls it into Data.
func loadData(filename string) (d Data, err error) {
	b, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	d = Data{}
	if err = json.Unmarshal(b, &d); err != nil {
		return nil, err
	}
	return d, nil
}

// run parses all flags, the html template file and runs the webserver.
func run() error {
	// Parse flags
	port := flag.String("p", "8080", "Port to listen")
	dataFile := flag.String("data", "data.json", "Sensor data json file")
	tplFile := flag.String("f", "index.html", "HTML template file")
	flag.Parse()

	// Read & parse our HTML template
	tpl, err := template.ParseFiles(*tplFile)
	if err != nil {
		return err
	}

	// Start the webserver.
	addr := ":" + *port
	fmt.Printf("Serving %s at %s\n", *tplFile, addr)
	return http.ListenAndServe(addr, http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Log a request
		fmt.Println(r.Method, r.RequestURI, r.RemoteAddr)
		// Try to load the sensor data file.
		data, err := loadData(*dataFile)
		// Generate HTML to respond with
		var b bytes.Buffer
		if err = tpl.Execute(&b, &executeData{
			// Passing the sensor data.
			Data: data,
			Err:  err,
		}); err != nil {
			// Write error response if we couldn't load the sensor data.
			fmt.Fprint(w, err)
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Println(err)
			return
		}
		// Write successful response.
		w.Write(b.Bytes())
	}))
}
