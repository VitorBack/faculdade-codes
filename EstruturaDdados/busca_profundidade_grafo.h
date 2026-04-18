#ifndef BUSCA_PROFUNDIDADE_GRAFO_H
#define BUSCA_PROFUNDIDADE_GRAFO_H

#include <stdio.h>

#define BP_MAX 50   

static int bp_visitado[BP_MAX];
static int bp_caminho [BP_MAX];

static void bp_inicializa(int t) {
    for (int i = 0; i < t; i++)
        bp_visitado[i] = 0;
}

static void bp_mostra_caminho(int t) {
    printf("Caminho (profundidade): ");
    for (int i = 0; i < t; i++) {
        printf("%d", bp_caminho[i]);
        if (i < t - 1) printf(" -> ");
    }
    printf("\n");
}

static void bp_dfs(int origem, int destino, int posicao,
                   int n, int mat[][BP_MAX]) {
    bp_visitado[origem]  = 1;
    bp_caminho [posicao] = origem;

    if (origem == destino) {          
        bp_mostra_caminho(posicao + 1);
    } else {
        for (int i = 0; i < n; i++) {
            if (mat[origem][i] == 1 && !bp_visitado[i]) {
                bp_dfs(i, destino, posicao + 1, n, mat);
            }
        }
    }

    bp_visitado[origem] = 0;          
}

void busca_profundidade_grafo(int origem, int destino,int mat[][BP_MAX], int n) {
    bp_inicializa(n);
    int achou = 0;

    bp_dfs(origem, destino, 0, n, mat);
    if (!bp_visitado[destino] && origem != destino) {
        printf("Nao existe caminho (profundidade) entre %d e %d.\n",
               origem, destino);
    }
}

#endif 