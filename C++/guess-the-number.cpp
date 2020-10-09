#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
   srand(time(NULL));
   int nombreMystere = (rand() % (100 - 1 + 1)) + 1;
   int guess,a,cpt1=0;

    do{
   printf("quel est le nombre mystere? : ");
   scanf("%d",&guess);
   if(guess < nombreMystere)
    printf("c'est plus !\n");
   else if(guess > nombreMystere)
    printf("c'est moins !\n");
    cpt1++;

   }while(guess!=nombreMystere);
        printf("Bravo, vous avez trouve le nombre mystere en %d tentatives !!!",cpt1);
        scanf("%d",&a);

}
