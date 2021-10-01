#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <string.h>


// Parametri del gioco
const  int LEN   = 4;             // lunghezza del codice segreto
const bool RIP   = false;         // permetti ripetizione dei simboli nel codice
const char ABC[] = "0123456789";  // definisci alfabeto del gioco


// RESTITUISCE un simbolo casuale
// appartenente all'alfabeto ABC
int nuovo_simbolo(char codice[]) {
    char simbolo;
    simbolo = ABC[rand() % strlen(ABC)];
    if (!RIP)
        while (strchr(codice, simbolo))
            simbolo = ABC[rand() % strlen(ABC)];
    return simbolo;
}

// Genera un codice di LEN simboli casuali
// appartenenti all'alfabeto ABC
void genera_codice(char codice[]) {
    int i;
    char simbolo;
    for (i = 0; i < LEN; i++) {
        simbolo = nuovo_simbolo(codice);
        codice[i] = simbolo;
    }
    codice[LEN] = '\0';
}

// RESTITUISCE il numero di simboli giusti
// alla posizione giusta
int trova_posti_giusti(char codice[], char tentativo[]) {
    int i, corrispondenza = 0;
    for (i = 0; i < LEN; i++)
        if (codice[i] == tentativo[i])
            corrispondenza++;
    return corrispondenza;
}

// RESTITUISCE il numero di occorrenze
// di carattere in stringa
int occorrenze(char stringa[], char carattere) {
    int i, n = 0;
    for (i = 0; i < strlen(stringa); i++)
        if (stringa[i] == carattere)
            n++;
    return n;
}

// RESTITUISCE il numero di simboli giusti,
// a prescindere dalla posizione
int trova_simboli_giusti(char codice[], char tentativo[]) {
    int i, corrispondenza = 0;
    char elemento, simboli_giusti[LEN];
    for (i = 0; i < LEN; i++) {
        elemento = tentativo[i];
        if (occorrenze(codice, elemento) > occorrenze(simboli_giusti, elemento)) {
            simboli_giusti[corrispondenza] = elemento;
            corrispondenza++;
        }
    }
    return corrispondenza;
}

// Genera il risultato del tentativo
void genera_risultato(char risultato[], char codice[], char tentativo[]) {
    int posti_giusti, simboli_giusti, i, j;
    posti_giusti = trova_posti_giusti(codice, tentativo);
    simboli_giusti = trova_simboli_giusti(codice, tentativo);
    for (i = 0; i < posti_giusti; i++)
        risultato[i] = '+';
    for (j = i; j < (simboli_giusti - posti_giusti) + i; j++)
        risultato[j] = '-';
    risultato[j] = '\0';
}


int main() {

    // Stampa titolo e istruzioni
    printf("\n- MasterMind -\n");
    printf("\nIndovina il codice segreto di %i simboli", LEN);
    printf("\nappartenenti all'alfabeto '%s'", ABC);
    printf("\nNOTA: il codice %s ripetizioni", RIP ? "puo' contenere" : "non prevede");
    printf("\n\nLEGENDA:");
    printf("\n(+) Simbolo giusto al posto giusto");
    printf("\n(-) Simbolo giusto al posto sbagliato");

    // Imposta un seed sempre diverso
    srand(time(NULL));

    // Genera il codice segreto
    char codice[LEN];
    genera_codice(codice);

    // Loop tentativi
    bool decifrato = false;
    int tentativi = 0;
    char tentativo[LEN], risultato[LEN];
    while (!decifrato) {
        printf("\n\n> ");
        gets(tentativo);
        if (strlen(tentativo) != LEN)
            printf("Il codice segreto e' di %i simboli!", LEN);
        else {
            decifrato = strcmp(codice, tentativo) == 0;
            genera_risultato(risultato, codice, tentativo);
            printf("> %s", risultato);
            tentativi++;
        }
    }

    // Codice indovinato
    printf("\n\n- COMPLIMENTI -\nHai indovinato!");
    printf("\n\nCodice: %s\nTentativi: %i\n", codice, tentativi);

    return 0;

}
