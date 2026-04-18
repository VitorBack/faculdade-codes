#include <stdio.h>
#include <stdlib.h>

typedef struct no {
  int elemento;
  struct no *esquerda;
  struct no *direita;
} No;

typedef struct {
    No *raiz;
} arvore;

void inicializaArvore(arvore *a) {
    a->raiz = NULL;
}

No* insereNo(No *raiz, int elemento) {
    if (raiz == NULL) {
      No *novo = (No*) malloc(sizeof(No));
      novo->elemento = elemento;
        novo->esquerda = NULL;
        novo->direita = NULL;
        return novo;
    }

    if (elemento < raiz->elemento) {
        raiz->esquerda = insereNo(raiz->esquerda, elemento);
    } else if (elemento > raiz->elemento) {
        raiz->direita = insereNo(raiz->direita, elemento);
    }

    return raiz;
}

void insereArvore(arvore *a, int elemento) {
    a->raiz = insereNo(a->raiz, elemento);
}

void ordenacao(No *raiz) {
    if (raiz != NULL) {
        ordenacao(raiz->esquerda);
        printf("%d ", raiz->elemento);
        ordenacao(raiz->direita);
    }
}

int main() {
    arvore arvore;

    inicializaArvore(&arvore);
    insereArvore(&arvore, 7);
    insereArvore(&arvore, 5);
    insereArvore(&arvore, 10);
    insereArvore(&arvore, 15);
    insereArvore(&arvore, 12);

    printf("Elementos em ordem: ");
    ordenacao(arvore.raiz);

    return 0;
}