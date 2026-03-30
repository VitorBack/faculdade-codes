#ifndef EMNIVEL_ARVORE_H
#define EMNIVEL_ARVORE_H

#include <stdio.h>
#include <stdlib.h>
#include "arvore.h"

// Estrutura da fila
typedef struct fila {
    noarvore *no;
    struct fila *prox;
} fila;

void enfileira(fila **inicio, fila **fim, noarvore *no) {
    fila *novo = (fila *) malloc(sizeof(fila));
    novo->no = no;
    novo->prox = NULL;

    if (*fim) {
        (*fim)->prox = novo;
    } else {
        *inicio = novo;
    }

    *fim = novo;
}

noarvore *desenfileira(fila **inicio, fila **fim) {
    if (!*inicio) return NULL;

    fila *temp = *inicio;
    noarvore *no = temp->no;

    *inicio = temp->prox;
    if (!*inicio) *fim = NULL;

    free(temp);
    return no;
}

void emnivel_arvore(arvore *a) {
    if (!raiz_arvore(a)) return;

    fila *inicio = NULL;
    fila *fim = NULL;

    // começa pela raiz
    enfileira(&inicio, &fim, raiz_arvore(a));

    while (inicio) {
        noarvore *atual = desenfileira(&inicio, &fim);

        printf("%d, ", atual->elemento);

        if (atual->esquerda)
            enfileira(&inicio, &fim, atual->esquerda);

        if (atual->direita)
            enfileira(&inicio, &fim, atual->direita);
    }
}

#endif