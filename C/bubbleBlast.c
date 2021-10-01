#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <string.h>


// Parametri del gioco
const  int X = 5;      // Numero di colonne della griglia (MAX 9)
const  int Y = 6;      // Numero di righe della griglia   (MAX 9)
const bool R = false;  // Calcolo ricorsivo delle mosse minime


// Genera una matrice di dimensioni X, Y
// di interi casuali compresi tra 0 e 3
void genera_griglia(int griglia[Y][X]) {
    int i, j;
    for (i = 0; i < Y; i++)
        for (j = 0; j < X; j++)
            griglia[i][j] = rand() % 4;
}

// Stampa le riga di
// coordinate x della griglia
void stampa_coordinate() {
    int i, j;
    for (i = 0; i < X; i++) {
        if (i == 0)
            printf("\n\n    ");
        printf("%i ", i + 1);
    }
    printf("\n");
}

// Stampa le righe della griglia
// con le relative coordinate
void stampa_griglia(int griglia[Y][X]) {
    int i, j;
    stampa_coordinate();
    for (i = 0; i < Y; i++) {
        for (j = 0; j < X; j++) {
            if (j == 0)
                printf("\n%i   ", i + 1);
            if (griglia[i][j] == 0)       // Bolla sgonfia
                printf(". ");
            else if (griglia[i][j] == 1)  // Bolla gonfia a meta'
                printf("o ");
            else if (griglia[i][j] == 2)  // Bolla in procinto di esplodere
                printf("0 ");
            else                          // Bolla esplosa
                printf("  ");
        }
    }
}

// Copia tutti gli elementi della
// griglia in copia_griglia
void crea_copia(int griglia[Y][X], int copia_griglia[Y][X]) {
    int i, j;
    for (i = 0; i < Y; i++)
        for (j = 0; j < X; j++)
            copia_griglia[i][j] = griglia[i][j];
}

// Incrementa lo stato della bolla specificata,
// se questa esplode, incrementa lo stato di quelle adiacenti
void tocca_bolla(int griglia[Y][X], int x, int y) {
    if (griglia[y][x] < 2)
        griglia[y][x]++;
    else if (griglia[y][x] == 2) {
        griglia[y][x]++;
        if (x - 1 >= 0)
            tocca_bolla(griglia, x - 1, y);
        if (x + 1 < X)
            tocca_bolla(griglia, x + 1, y);
        if (y - 1 >= 0)
            tocca_bolla(griglia, x, y - 1);
        if (y + 1 < Y)
            tocca_bolla(griglia, x, y + 1);
    }
}

// RESTITUISCE vero se tutti gli elementi della
// matrice sono uguali a 3, falso altrimenti
bool griglia_vuota(int griglia[Y][X]) {
    int i, j;
    bool vuota = true;
    for (i = 0; i < Y && vuota; i++)
        for (j = 0; j < X && vuota; j++)
            vuota = griglia[i][j] == 3;
    return vuota;
}

// Funzione ricorsiva per il calcolo delle mosse minime
// necessarie per svuotare la griglia
int calcola_mosse_r(int griglia[Y][X]) {
    int copia_griglia[Y][X];
    int mosse, mosse_minime = 0;
    int i, j;
    for (i = 0; i < Y; i++) {
        for (j = 0; j < X; j++) {
            if (griglia[i][j] < 3) {
                crea_copia(griglia, copia_griglia);
                tocca_bolla(copia_griglia, j, i);
                if (griglia_vuota(copia_griglia))
                    return 1;
                mosse = 1 + calcola_mosse_r(copia_griglia);
                if (mosse_minime == 0 || mosse < mosse_minime)
                    mosse_minime = mosse;
            }
        }
    }
    return mosse_minime;
}

// Imposta tutti gli elementi della griglia a 3
void genera_griglia_finita(int griglia[Y][X]) {
    int i, j;
    for (i = 0; i < Y; i++)
        for (j = 0; j < X; j++)
            griglia[i][j] = 3;
}

// RESTITUISCE le coordinate x,y della prima bolla
// minore di griglia1 rispetto a griglia2,
// se non esiste restituisce le coordinate -1,-1
void prima_bolla_minore(int griglia1[Y][X], int griglia2[Y][X], int coordinate[2]) {
    int i, j;
    coordinate[0] = -1;
    coordinate[1] = -1;
    for (i = 0; i < Y; i++) {
        for (j = 0; j < X; j++) {
            if (griglia1[i][j] < griglia2[i][j]) {
                coordinate[0] = j;
                coordinate[1] = i;
                break;
            }
        }
    }
}

// RESTITUISCE vero se il tocco inverso della
// bolla specificata e' valido, falso altrimenti
bool tocco_inverso_valido(
    int griglia_finita[Y][X], int griglia[Y][X],
    int x, int y, int x_precedente, int y_precedente
) {
    if (x >= 0 && x < X && y >= 0 && y < Y)           // Coordinate della bolla valide
        if (
            griglia_finita[y][x] > griglia[y][x] &&   // Necessita' di decrementarla
            (x != x_precedente || y != y_precedente)  // Bolla diversa dalla precedente
        ) return true;
    return false;
}

// Decrementa lo stato della bolla specificata,
// se questa era esplosa, sceglie se decrementare
// lo stato delle bolle adiacenti
void tocco_inverso(
    int griglia_finita[Y][X], int griglia[Y][X],
    int x, int y, int x_precedente, int y_precedente
) {
    if (griglia_finita[y][x] == 3) {  // Passaggio da 'esplosa' a
        griglia_finita[y][x]--;       // 'in procinto di esplodere'
        if (tocco_inverso_valido(griglia_finita, griglia, x - 1, y, x_precedente, y_precedente))
            tocco_inverso(griglia_finita, griglia, x - 1, y, x, y);
        if (tocco_inverso_valido(griglia_finita, griglia, x + 1, y, x_precedente, y_precedente))
            tocco_inverso(griglia_finita, griglia, x + 1, y, x, y);
        if (tocco_inverso_valido(griglia_finita, griglia, x, y - 1, x_precedente, y_precedente))
            tocco_inverso(griglia_finita, griglia, x, y - 1, x, y);
        if (tocco_inverso_valido(griglia_finita, griglia, x, y + 1, x_precedente, y_precedente))
            tocco_inverso(griglia_finita, griglia, x, y + 1, x, y);
    }
    else if (griglia_finita[y][x] > 0)  // Altre bolle che non
        griglia_finita[y][x]--;         // siano sgonfie
}

// RESTITUISCE il numero minimo di mosse
// necessarie per svuotare la griglia
int calcola_mosse(int griglia[Y][X]) {
    bool griglie_uguali = false;
    int mosse = 0, coordinate[2], x, y;
    int griglia_finita[Y][X];
    genera_griglia_finita(griglia_finita);
    do {
        prima_bolla_minore(griglia, griglia_finita, coordinate);
        x = coordinate[0];
        y = coordinate[1];
        griglie_uguali = x == -1 && y == -1;
        if (!griglie_uguali) {
            tocco_inverso(griglia_finita, griglia, x, y, -1, -1);
            mosse++;
        }
    } while (!griglie_uguali);
    return mosse;
}

// RESTITUISCE vero se la stringa coordinate
// e' valida, falso altrimenti
bool input_valido(char coordinate[]) {
    if (
        strlen(coordinate) == 3 &&
        coordinate[0] >= 1 &&
        coordinate[0] <= X + '0' &&
        coordinate[1] == ',' &&
        coordinate[2] >= 1 &&
        coordinate[2] <= Y + '0'
    ) return true;
    return false;
}

// Loop del gioco con selezione della bolla
// e stampa della griglia aggiornata
int loop_gioco(int griglia[Y][X]) {
    int x, y, mosse = 0;
    bool finito = false;
    char coordinate[3];
    while (!finito) {
        printf("\n\n> ");
        gets(coordinate);
        if (input_valido(coordinate)) {
            x = (coordinate[0] - '0') - 1;
            y = (coordinate[2] - '0') - 1;
            if (griglia[y][x] < 3) {
                tocca_bolla(griglia, x, y);
                finito = griglia_vuota(griglia);
                mosse++;
            }
            stampa_griglia(griglia);
        } else {
            printf("\nDevi inserire le coordinate x,y");
            printf("\ndella bolla che vuoi selezionare!");
        }
    }
    return mosse;
}


int main() {

    // Stampa titolo e istruzioni
    printf("\n- BubbleBlast -\n");
    printf("\nFai esplodere tutte le bolle della griglia %ix%i", X, Y);
    printf("\nTocca la bolla inserendo le sue coordinate x,y\n");
    printf("\nLEGENDA:");
    printf("\n(.) Bolla sgonfia");
    printf("\n(o) Bolla gonfia a meta'");
    printf("\n(0) Bolla in procinto di esplodere\n");

    // Imposta un seed sempre diverso
    srand(time(NULL));

    // Genera e stampa la griglia iniziale
    int griglia[Y][X];
    genera_griglia(griglia);
    stampa_griglia(griglia);

    // Calcola e stampa le mosse minime
    // per svuotare la griglia
    int mosse_minime;
    if (R) {
        printf("\n\nCalcolo mosse in corso...");
        mosse_minime = calcola_mosse_r(griglia);
    } else
        mosse_minime = calcola_mosse(griglia);
    printf("\n\nMosse minime: %i\n", mosse_minime);

    // Avvio loop del gioco
    // e conteggio delle mosse
    int mosse;
    mosse = loop_gioco(griglia);

    // Griglia vuota
    printf("\n\n- COMPLIMENTI -\nLa griglia e' vuota!");
    printf("\n\nMosse: %i\n", mosse);

    return 0;

}
