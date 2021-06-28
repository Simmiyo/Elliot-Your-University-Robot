package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"

	"golang.org/x/crypto/pbkdf2"
)

func main() {

	// var nume_var tip_var
	var secret string
	var password string
	var storeFile string
	var logFile string

	// preluare argumente
	flag.StringVar(&secret, "s", "", "Specify the secret that needs to be encrypted")
	flag.StringVar(&password, "p", "", "specify the encryption key.")
	flag.StringVar(&storeFile, "f", "", "specify where will the encrypted result will be stored.")
	flag.StringVar(&logFile, "log", "../logs/go.log", "Specify the file path where the errors will be logged.")

	flag.Parse()

	// fisierul-jurnal pt go
	fmt.Printf("Setting the log file: %s \n", logFile)
	file, err := os.OpenFile(logFile, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)

	if err != nil {
		log.Fatal(err) // Fatal = os.Exit(1)
	}

	defer file.Close()

	log.SetOutput(file)

	// logare lipsa parola sau secret(token)
	if secret == "" {
		fmt.Println("No secret was given!")
		log.Println("No secret was given!")
		os.Exit(2)
	}
	if password == "" {
		fmt.Println("No password was given!")
		log.Println("No password was given!")
		os.Exit(2)
	}

	// cod eraore 1 -> nu am putut deschide log
	// cod eraore 2 -> nu am primit un parametru necesar
	// cod eroare 3 -> nu s-a putut crea ceva
	// cod eroare 4 -> nu am putut scrie in fisier tokenul criptat

	text := []byte(secret)
	key := []byte(password)

	// declar salt de 16 bytes
	fmt.Println("Generating the salt.")
	var salt = make([]byte, 16)
	// generez aleator cei 16 bytes din salt
	_, err = rand.Read(salt[:])
	if err != nil {
		log.Println("Unable to create new salt!", err)
		os.Exit(3)
	}

	// dk = rezultatul derivarii cheii cu saltul: aplica de 4096 ori sha => dk de 32 bytes
	fmt.Println("Deriving the key.")
	dk := pbkdf2.Key(key, salt, 4096, 32, sha256.New)

	fmt.Println("Preparing the cryptosystem.")
	// genereaza un cifru aes folosind cheia derivata dk
	c, err := aes.NewCipher(dk)

	if err != nil {
		log.Println("Unable to create new AES cypher!", err)
		os.Exit(3)
	}

	// gcm = Galois/Counter Mode, aplica modul de operare GCM cifrului aes de mai sus
	gcm, err := cipher.NewGCM(c)

	if err != nil {
		log.Println("Unable to create new GCM cypher mode!", err)
		os.Exit(3)
	}

	// nonce = counterul GCM, declar un counter de marimea (in bytes) folosita de GCM
	fmt.Println("Generating the counter.")
	nonce := make([]byte, gcm.NonceSize())

	// generez aleator acei bytes din counter
	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
		log.Println("Unable to create new nonce!", err)
		os.Exit(3)
	}

	fmt.Println("Encrypting the secret.")
	// matriece cu salt = prima linie si rezultatul criptarii = a2a linie
	data := [][]byte{salt,
		gcm.Seal(nonce, nonce, text, nil)}

	// uneste liniile matricei intr-un singur vector
	result := bytes.Join(data, []byte(""))

	if storeFile != "" {

		err = ioutil.WriteFile(storeFile, result, 0777) // sterge ce e deja inauntru (scrie peste)

		if err != nil {
			log.Println("Unable to write in the store file: "+storeFile, err)
			os.Exit(4)
		}
	} else {
		fmt.Println(result)
	}
	os.Exit(0)
}
