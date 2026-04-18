#ifndef BUSCA_LARGURA_GRAFO_H
#define BUSCA_LARGURA_GRAFO_H

#include <stdio.h>

#define BL_MAX 50   

static int bl_i, bl_j;
static int bl_fila[BL_MAX];
static int bl_ini = 0, bl_fim = 0;

static void bl_enfileira(int x)     { bl_fila[bl_fim++] = x;        }
static int  bl_desenfileira(void)   { return bl_fila[bl_ini++];      }
static int  bl_vazia(void)          { return bl_ini == bl_fim;       }

static void bl_mostra_caminho(int pai[], int destino) {
    int caminho[BL_MAX];
    int tamanho = 0;
    int v = destino;

    while (v != -1) {
        caminho[tamanho++] = v;
        v = pai[v];
    }

    printf("Menor Caminho (largura): ");
    for (int i = tamanho - 1; i >= 0; i--) {
        printf("%d", caminho[i]);
        if (i > 0) printf(" -> ");
    }
    printf("\n");
}

void busca_largura_grafo(int origem, int destino, int mat[][BL_MAX], int n) {
    int visitado[BL_MAX] = {0};
    int pai[BL_MAX];

    bl_ini = 0;
    bl_fim = 0;

    for (bl_i = 0; bl_i < n; bl_i++)
        pai[bl_i] = -1;

    bl_enfileira(origem);
    visitado[origem] = 1;

    while (!bl_vazia()) {
        bl_j = bl_desenfileira();

        if (bl_j == destino) break;     

        for (bl_i = 0; bl_i < n; bl_i++) {
            if (mat[bl_j][bl_i] == 1 && !visitado[bl_i]) {
                bl_enfileira(bl_i);
                visitado[bl_i] = 1;
                pai[bl_i]      = bl_j;
            }
        }
    }

    if (!visitado[destino]) {
        printf("Nao existe caminho (largura) entre %d e %d.\n",
               origem, destino);
    } else {
        bl_mostra_caminho(pai, destino);
    }
}

#endif 