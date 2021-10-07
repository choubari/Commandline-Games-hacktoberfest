using System;
using System.Text;

namespace Number_Guesser
{
    class Program
    {
        static void Main()
        {

            string homeTown;
            Console.WriteLine("Welcome, Adventurer!");
            Console.WriteLine("You must be weary from your travels.");
            Console.WriteLine("Come...have a seat by the fire.");
            Console.WriteLine("I sense that you have come far. Where are you from, adventurer?");
            homeTown = Console.ReadLine();
            Console.WriteLine("Ah yes. " + homeTown + " is a wonderful place. I've been there myself, many years ago.");
            Console.WriteLine("While you eat your meal, shall we play a game?");
            Console.WriteLine("Please, think of a number between 1 and 100.");
            Console.WriteLine("Now I shall try to guess your number...");

            int min = 1;
            int max = 101;
            GuessNumber(min, max);

            Console.ReadKey();

        }

        static void GuessNumber(int min, int max)
        {
            Random random = new Random();

            int guess = random.Next(min, max);
            Console.WriteLine("Tell me.... is your number " + guess + " ?");
            string answer;
            answer = Console.ReadLine();
            if (answer == "Yes" || answer == "Y" || answer == "y" || answer == "yes" || answer == "YES")
            {
                Console.WriteLine("Excellent! The great number wizard is right again!");
                Console.WriteLine("***LET'S PLAY AGAIN***.");
                min = 1;
                max = 101;
                GuessNumber(min, max);
            }
            else if (answer == "No" || answer == "N" || answer == "n" || answer == "no" || answer == "NO")
            {
                Console.WriteLine("Hmmmm...my magic must be out of balance today.");
                Console.WriteLine("Tell me: was the number you were thinking of LOWER or HIGHER than my magical guess?");
                string Hint;
                Hint = Console.ReadLine();
                if (Hint == "Higher" || Hint == "higher" || Hint == "HIGHER")
                {
                    Console.WriteLine("Ah. So it was higher? I will use this information for my next guess.");
                    if (guess <= 99)
                    {
                        min = guess + 1;
                    }
                    else
                    {
                        guess = 100;
                    }
                    GuessNumber(min, max);
                }
                else if (Hint == "Lower" || Hint == "lower" || Hint == "LOWER")
                {
                    Console.WriteLine("Ah. So it was lower? I will use this information for my next guess.");
                    if (guess > 1)
                    {
                        max = guess - 1;
                    }
                    else
                    {
                        guess = 1;
                    }
                    GuessNumber(min, max);
                }
                else
                {
                    TryAgain(min, max);
                }

            }
            else
            {
                TryAgain(min, max);
            }
        }

        static void TryAgain(int min, int max)
        {
            Console.WriteLine("I sense a disturbance in the force. Perhaps we should try again.");
            GuessNumber(min, max);

        }
    }
}

