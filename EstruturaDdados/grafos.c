#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "busca_largura_grafo.h"
#include "busca_profundidade_grafo.h"

#define MAX_VERTICES 50   /* mesmo valor de BL_MAX e BP_MAX nos headers */
#define MAX_ARESTAS  200

int adj[MAX_VERTICES][MAX_VERTICES];
int vertices[MAX_VERTICES];
int numVertices = 0;
int numArestas  = 0;

int buscarVertice(int v) {
    for (int i = 0; i < numVertices; i++)
        if (vertices[i] == v) return i;
    return -1;
}

int inserirVertice(int v) {
    int idx = buscarVertice(v);
    if (idx != -1) return idx;
    if (numVertices >= MAX_VERTICES) {
        printf("Limite de vertices atingido.\n");
        exit(1);
    }
    vertices[numVertices] = v;
    return numVertices++;
}

void adicionarAresta(int a, int b) {
    int ia = inserirVertice(a);
    int ib = inserirVertice(b);
    adj[ia][ib] = 1;
    adj[ib][ia] = 1;
    numArestas++;
}

void apresentarMatriz() {
    if (numVertices == 0) {
        printf("Nenhum grafo cadastrado ainda.\n");
        return;
    }
    printf("\n--- Matriz de Adjacencia ---\n\n");
    printf("   ");
    for (int i = 0; i < numVertices; i++)
        printf(" %3d", vertices[i]);
    printf("\n   ");
    for (int i = 0; i < numVertices; i++)
        printf(" ---");
    printf("\n");
    for (int i = 0; i < numVertices; i++) {
        printf("%3d|", vertices[i]);
        for (int j = 0; j < numVertices; j++)
            printf(" %3d", adj[i][j]);
        printf("\n");
    }
    printf("\nVertices: %d  |  Arestas: %d\n", numVertices, numArestas);
}

int bfs(int inicio, int fim, int caminho[], int tamMax) {
    int pai[MAX_VERTICES];
    int visitado[MAX_VERTICES];
    int fila[MAX_VERTICES];
    memset(pai,      -1, sizeof(pai));
    memset(visitado,  0, sizeof(visitado));

    int frente = 0, fundo = 0;
    fila[fundo++] = inicio;
    visitado[inicio] = 1;

    while (frente < fundo) {
        int cur = fila[frente++];
        if (cur == fim) {
            int tmp[MAX_VERTICES], tam = 0, v = fim;
            while (v != -1) { tmp[tam++] = v; v = pai[v]; }
            for (int i = tam - 1; i >= 0; i--)
                caminho[tam - 1 - i] = tmp[i];
            return tam;
        }
        for (int j = 0; j < numVertices; j++) {
            if (adj[cur][j] == 1 && !visitado[j]) {
                visitado[j] = 1;
                pai[j] = cur;
                fila[fundo++] = j;
            }
        }
    }
    return 0;
}

void buscarPercurso() {
    if (numVertices == 0) {
        printf("Nenhum grafo cadastrado ainda.\n");
        return;
    }
    int va, vb;
    printf("\nVertice inicial (apenas o numero): ");
    scanf("%d", &va);
    printf("Vertice final   (apenas o numero): ");
    scanf("%d", &vb);

    int ia = buscarVertice(va);
    int ib = buscarVertice(vb);

    if (ia == -1 || ib == -1) {
        printf("Vertice(s) inexistente(s) no grafo.\n");
        return;
    }
    if (ia == ib) {
        printf("Vertice inicial e final sao iguais: %d\n", va);
        return;
    }

    int caminho[MAX_VERTICES];
    int tam = bfs(ia, ib, caminho, MAX_VERTICES);

    if (tam == 0) {
        printf("\nNao existe percurso entre %d e %d.\n", va, vb);
    } else {
        printf("\nPercurso encontrado (%d salto%s):\n  ",
               tam - 1, tam - 1 > 1 ? "s" : "");
        for (int i = 0; i < tam; i++) {
            printf("%d", vertices[caminho[i]]);
            if (i < tam - 1) printf(" -> ");
        }
        printf("\n");
    }
}

void cadastrarArestas() {
    int n;
    printf("\nQuantas arestas deseja cadastrar? ");
    scanf("%d", &n);
    if (n <= 0) return;
    for (int i = 1; i <= n; i++) {
        int a, b;
        printf("  Aresta %d - Vertice inicial: ", i);
        scanf("%d", &a);
        printf("  Aresta %d - Vertice final  : ", i);
        scanf("%d", &b);
        if (a == b) {
            printf("  (!) Vertice inicial e final iguais. Aresta ignorada.\n");
            i--; continue;
        }
        int ia = buscarVertice(a);
        int ib = buscarVertice(b);
        if (ia != -1 && ib != -1 && adj[ia][ib] == 1) {
            printf("  (!) Aresta %d-%d ja existe. Ignorada.\n", a, b);
            i--; continue;
        }
        adicionarAresta(a, b);
        printf("  Aresta %d-%d adicionada.\n", a, b);
    }
}

int main() {
    int opcao;
    memset(adj, 0, sizeof(adj));

    printf("=== Grafo Nao Dirigido - Matriz de Adjacencia ===\n");

    do {
        printf("\n--- Menu ---\n");
        printf("1. Cadastrar arestas\n");
        printf("2. Apresentar matriz de adjacencia\n");
        printf("3. Buscar percurso\n");
        printf("0. Sair\n");
        printf("Opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1: cadastrarArestas(); break;
            case 2: apresentarMatriz(); break;
            case 3: buscarPercurso();   break;
            case 0: printf("Encerrando.\n"); break;
            default: printf("Opcao invalida.\n");
        }
    } while (opcao != 0);

    if (numVertices == 0) {
        printf("Nenhum grafo cadastrado. Encerrando.\n");
        return 0;
    }

    int va, vb;
    printf("\n--- Busca externa ---\n");
    printf("Vertice de origem : "); scanf("%d", &va);
    printf("Vertice de destino: "); scanf("%d", &vb);

    int origem  = buscarVertice(va);
    int destino = buscarVertice(vb);

    if (origem == -1 || destino == -1) {
        printf("Vertice(s) inexistente(s) no grafo.\n");
        return 1;
    }

    busca_largura_grafo    (origem, destino, adj, numVertices);
    busca_profundidade_grafo(origem, destino, adj, numVertices);

    return 0;
}