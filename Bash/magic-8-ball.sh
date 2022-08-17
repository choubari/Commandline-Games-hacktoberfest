#!/bin/bash

# # magic 8 ball. Yup. Pick a random number, output message
# # messages harvested from the Wikipedia entry

shuffle() {
   local i tmp size max rand

   # $RANDOM % (i+1) is biased because of the limited range of $RANDOM
   # Compensate by using a range which is a multiple of the array size.
   size=${#array[*]}
   max=$(( 32768 / size * size ))

   for ((i=size-1; i>0; i--)); do
      while (( (rand=$RANDOM) >= max )); do :; done
      rand=$(( rand % (i+1) ))
      tmp=${array[i]} array[i]=${array[rand]} array[rand]=$tmp
   done
}

array=(
   "Signs point to yes."
   "Yes."
   "Reply hazy, try again."
   "Without a doubt."
   "My sources say no."
   "As I see it, yes."
   "You may rely on it."
   "Concentrate and ask again."
   "Outlook not so good."
   "It is decidedly so."
   "Better not tell you now."
   "Very doubtful."
   "Yes - definitely."
   "It is certain."
   "Cannot predict now."
   "Most likely."
   "Ask again later."
   "My reply is no."
   "Outlook good."
   "Don't count on it."
   "No."
   "Very unlikely."
   "No - don't even think about it."
)

shuffle
for var in "${array[@]}"
do
   # echo "Oh! Magic 8 Ball, Please Tell Me True..." ; echo ""
   echo -n "What is your question? "
   read q
   echo
   echo "I have looked into the future and I see.. "
   sleep 2
   echo
   echo "${var}"
   echo
done
