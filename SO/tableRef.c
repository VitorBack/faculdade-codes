#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int comparar(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

void imprimeTableRef(int quant_processos, int vetor_vsc[], int vetor_bt[], int vetor_prty[], int vetor_td[]) {
    int i = 1;
    while (i <= quant_processos) {
        printf("\nProcesso %d: ", i);
        printf("\nChegada: %d", vetor_vsc[i-1]);
        printf("\nBurst Time: %d", vetor_bt[i-1]);
        printf("\nPrioridade: %d", vetor_prty[i-1]);
        printf("\nTempo de Espera: %d\n", vetor_td[i-1]);
        i++;
    }
}

void defineVSC(int quant_processos, int chg_em_zero, int vetor_vsc[]) {
    int i = 0;
    int menor_chegada, maior_chegada;

    while (1) {
        printf("\nMenor Chegada: ");
        scanf("%d", &menor_chegada);

        if (chg_em_zero == 1 && menor_chegada == 0) {
            break;
        } else if (menor_chegada > 0) {
            break;
        } else {
            printf("O valor informado deve ser maior que 0 (ou 0 se confirmou chegada em zero)!\n");
        }
    }

    while (1) {
        printf("\nMaior Chegada: ");
        scanf("%d", &maior_chegada);
        if (maior_chegada >= menor_chegada) {
            break;
        } else {
            printf("O valor informado para maior chegada deve ser MAIOR ou IGUAL a menor chegada!\n");
        }
    }

    if (chg_em_zero == 1) {
        vetor_vsc[0] = 0;
        for (i = 1; i < quant_processos; i++) {
            vetor_vsc[i] = rand() % (maior_chegada - menor_chegada + 1) + menor_chegada;
        }
    } else {
        for (i = 0; i < quant_processos; i++) {
            vetor_vsc[i] = rand() % (maior_chegada - menor_chegada + 1) + menor_chegada;
        }
    }

    qsort(vetor_vsc, quant_processos, sizeof(int), comparar);
}

void defineBT(int quant_processos, int vetor_bt[]) {
    int menor_BT, maior_BT;

    while (1) {
        printf("\nMenor Burst Time: ");
        scanf("%d", &menor_BT);
        if (menor_BT > 0) {
            break;
        } else {
            printf("O valor informado nao pode ser 0!\n");
        }
    }

    while (1) {
        printf("\nMaior Burst Time: ");
        scanf("%d", &maior_BT);
        if (maior_BT >= menor_BT) {
            break;
        } else {
            printf("O valor informado para maior burst time deve ser MAIOR ou IGUAL ao menor burst time!\n");
        }
    }

    for (int i = 0; i < quant_processos; i++) {
        vetor_bt[i] = rand() % (maior_BT - menor_BT + 1) + menor_BT;
    }
}

void definePrty(int quant_processos, int vetor_prty[]) {

    int menor_prty;

    while (1) {
        printf("\nMenor Prioridade: ");
        scanf("%d", &menor_prty);
        if (menor_prty > 0) {
            break;
        } else {
            printf("O valor informado nao pode ser 0!\n");
        }
    }
    for (int i = 0; i < quant_processos; i++) {
        vetor_prty[i] = rand() % menor_prty + 1;
    }
}

void defineTd(int quant_processos, int chg_em_zero, int vetor_td[], int vetor_vsc[]) {
    for (int i = 0; i < quant_processos; i++) {
        if (chg_em_zero == 0) {
            vetor_td[i] = vetor_vsc[i];
        } else {
            if(vetor_vsc[i] == 0) {
                vetor_td[i] = 0;
            } else {
            vetor_td[i] = vetor_vsc[i] + vetor_td[i-1];
            }
        }
    }
}

int main() {
    srand(time(NULL)); 

    int quant_processos, chg_em_zero;

    printf("\nQuantidade de processos: ");
    scanf("%d", &quant_processos);

    printf("\nChegada em Zero? 1-Sim; 2-Nao: ");
    scanf("%d", &chg_em_zero);

    int vetor_vsc[quant_processos];
    defineVSC(quant_processos, chg_em_zero, vetor_vsc);

    int vetor_bt[quant_processos];
    defineBT(quant_processos, vetor_bt);

    int vetor_prty[quant_processos];
    definePrty(quant_processos, vetor_prty);

    int vetor_td[quant_processos];
    defineTd(quant_processos, chg_em_zero, vetor_td, vetor_vsc);

    imprimeTableRef(quant_processos, vetor_vsc, vetor_bt, vetor_prty, vetor_td);

    return 0;
}