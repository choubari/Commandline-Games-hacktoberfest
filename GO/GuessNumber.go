package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

// this function will do literaly its name ;)
func createRandomNumber(RngEdge int) int {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	return r.Intn(RngEdge)
}

func main() {
	var RngEdge int = 10
	var Chances int = 3
	TrueNmb := createRandomNumber(RngEdge)

	fmt.Println("Enter an integer from 0 to ", RngEdge)
	state := true
	reader := bufio.NewReader(os.Stdin)
	for state {
		if Chances == 0 {
			fmt.Println("Game Over ;(")
			break
		}
		input, _, _ := reader.ReadLine()
		command, err := strconv.Atoi(string(input))
		if err != nil {
			fmt.Println("What are you doing BRO!")
		} else {
			if command == TrueNmb {
				state = false
				fmt.Println("Well Well! You got right this time :)")
			} else if command < TrueNmb {
				Chances -= 1
				fmt.Println("GO BIGGER BRO!", '\n', "BTW u still have ", Chances, " Chances")
			} else if command > TrueNmb {
				Chances -= 1
				fmt.Println("A bit smaller!", '\n', "BTW u still have ", Chances, " Chances")
			}
		}
	}
}
