package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/sha256"
	"encoding/csv"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/zaddok/moodle"
	"golang.org/x/crypto/pbkdf2"
)

// func nume_func([param tip_param])([tip_return])
// aflarea id-ului cursului ales din csv
func getCourseId(coursesFilePath string, courseTitle string) (int64, error) {
	f, err := os.Open(coursesFilePath)
	if err != nil {
		log.Println("Unable to read input file "+coursesFilePath, err)
		return -1, err
	}
	defer f.Close()

	csvReader := csv.NewReader(f)
	records, err := csvReader.ReadAll() // records ~ lista de tupluri curs&id
	if err != nil {
		log.Println("Unable to parse file as CSV for "+coursesFilePath, err)
		return -1, err
	}

	records = records[1:]
	for _, rec := range records {
		if strings.Contains(rec[0], courseTitle) {
			i, err := strconv.ParseInt(rec[1], 10, 64) // 64 biti ca asa am declarat return
			if err != nil {
				log.Println("Unable to convert string id to integer: "+rec[1], err)
				return -1, err
			}
			return i, nil // returneaza id-ul cursului cu titlul din param
		}
	}

	return -1, nil
}

func decryptToken(tokenPath string, tokenPass string) (string, error) {
	key := []byte(tokenPass)
	cipherToken, err := ioutil.ReadFile(tokenPath)

	if err != nil {
		log.Println("Unable to read the token file: "+tokenPath, err)
		return "", err
	}

	salt, cipherToken := cipherToken[:16], cipherToken[16:]
	dk := pbkdf2.Key(key, salt, 4096, 32, sha256.New)

	c, err := aes.NewCipher(dk)
	if err != nil {
		log.Println("Unable to create new cypher block.", err)
		return "", err
	}

	gcm, err := cipher.NewGCM(c)
	if err != nil {
		log.Println("Unable to create new GCM cypher block.", err)
		return "", err
	}

	nonceSize := gcm.NonceSize()
	if len(cipherToken) < nonceSize {
		log.Println("Cyphered token size is smaller than the nonce size.", err)
		return "", err
	}

	nonce, cipherToken := cipherToken[:nonceSize], cipherToken[nonceSize:]
	token, err := gcm.Open(nil, nonce, cipherToken, nil)
	if err != nil {
		log.Println("Someting went wrong when trying to decrypt the value of the token.", err)
		return "", err
	}
	return string(token), err
}

func main() {
	var commandType string
	var coursesStoreFilePath string
	var tokenStoreFilePath string
	var tokenPassword string
	var tokenValue string
	var username string
	var courseName string
	var respFilePath string
	var logFile string

	flag.StringVar(&commandType, "type", "refresh", "Specify what should the program do.\n -refresh: refresh courses list"+
		"\n -materials: gets materials for specified course \n Default is refresh.")
	flag.StringVar(&coursesStoreFilePath, "cfile", "", "Specify the path where the list of current courses is stored.")
	flag.StringVar(&tokenValue, "tval", "", "Specify the clear token value.")
	flag.StringVar(&tokenStoreFilePath, "tfile", "", "Specify the path where the encrypted value of the token is stored.")
	flag.StringVar(&tokenPassword, "tpass", "", "Specify the password that was used to encrypt the token.")
	flag.StringVar(&username, "uname", "", "Specify the username.")
	flag.StringVar(&courseName, "cname", "", "Specify the wanted course name.")
	flag.StringVar(&respFilePath, "rfile", "", "Specify the file path where the moodle response will be stored.")
	flag.StringVar(&logFile, "log", "../logs/go.log", "Specify the file path where the errors will be logged.")

	flag.Parse() // after declaring flags we need to call it

	fmt.Printf("Setting the log file: %s \n", logFile)
	file, err := os.OpenFile(logFile, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)

	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	log.SetOutput(file)

	// cod eraore 1 -> nu am putut deschide log
	// cod eraore 2 -> nu am primit un parametru necesar
	// cod eroare 3 -> nu s-a putut decripta
	// alte numere -> alte probleme

	if tokenValue == "" {
		if tokenStoreFilePath == "" {
			log.Println("No token store file was given!")
			os.Exit(2)
		}
		if tokenPassword == "" {
			log.Println("No password was given!")
			os.Exit(2)
		}

		// in caz ca nu am primit valoarea tokenului in clar, o decriptez din fisier
		fmt.Println("Decrypting the Moodle security token.")
		token, err := decryptToken(tokenStoreFilePath, tokenPassword)
		if err != nil {
			os.Exit(3)
		}
		tokenValue = token
	}

	// date pt request API
	api := moodle.NewMoodleApi("http://moodle.unibuc.ro//webservice/rest/server.php", tokenValue)

	if commandType == "refresh" {

		// Autentificare Moodle
		if username == "" {
			log.Println("No username was given!")
			os.Exit(2)
		}
		fmt.Println("Get the user's Moodle Profile.")
		person, err := api.GetPersonByUsername(username)
		if err != nil {
			log.Println("Unable to find user with the given username: "+username, err)
			os.Exit(4)
		}

		// Obtinere lista cu nume de cursuri plus stocare
		fmt.Println("Get the user's courses.")
		courses, err := api.GetPersonCourseList(person.MoodleId)
		if err != nil {
			log.Println("Unable to find courses list.", err)
			os.Exit(5)
		}

		if coursesStoreFilePath == "" {
			log.Println("No courses store file path was given!")
			os.Exit(2)
		}
		fmt.Println("Create/open the courses store file.")
		f, err := os.Create(coursesStoreFilePath)
		if err != nil {
			log.Println("Unable to create file for storing the courses list: "+coursesStoreFilePath, err)
			os.Exit(6)
		}

		csvWriter := csv.NewWriter(f)
		fmt.Println("Prepare the data.")
		data := make([][]string, len(courses)+1) // declarare matrice-tabel (dimensiune cursuri plus header)
		for i := 0; i < len(courses)+1; i++ {
			data[i] = make([]string, 2) // declarare lista cursuri (liniile matricei, 2 coloane = curs&Id)
		}
		data[0][0] = "Curs"
		data[0][1] = "Id"
		for index, course := range courses {
			data[index+1][0] = course.Name
			data[index+1][1] = strconv.FormatInt(course.MoodleId, 10) // conversie din int baza 10 in string
		}

		fmt.Println("Write the data to the file.")
		err = csvWriter.WriteAll(data)
		if err != nil {
			log.Println("Unable to store list to file: "+coursesStoreFilePath, err)
			os.Exit(7)
		}

	} else if commandType == "materials" {
		if courseName == "" {
			log.Println("No course name was given!")
			os.Exit(2)
		}
		fmt.Println("Get the Moodle id of the given course.")
		courseId, err := getCourseId(coursesStoreFilePath, courseName)
		if err != nil {
			os.Exit(8)
		}

		fmt.Println("Get the contents list of the given course.")
		response, err := api.GetCourseContents(courseId) // continutul cursului e memorat in response (json)
		if err != nil {
			log.Println("Unable to find the conents of: "+courseName, err)
			os.Exit(9)
		}

		if respFilePath == "" {
			log.Println("No response file was given!")
			os.Exit(2)
		}
		fmt.Println("Create/open the contents list store file.")
		f, err := os.Create(respFilePath) // creeaza fisierul pt raspuns
		if err != nil {
			log.Println("Unable to create response file: "+respFilePath, err)
			os.Exit(10)
		}
		defer f.Close()

		fmt.Println("Write the data to the file.")
		_, err = f.WriteString(*response) // stocheaza raspunsul; in fisierul creat
		if err != nil {
			log.Println("Unable to write response.", err)
			os.Exit(11)
		}
	}
	os.Exit(0)
}
