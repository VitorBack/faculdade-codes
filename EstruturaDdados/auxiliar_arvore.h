#include <stdio.h>
#include <stdlib.h>
#include "arvore.h"

int grauno_arvore (arvore *a, int no){

    noarvore *atual = raiz_arvore(a);

    //caso a árvore estiver vazia
    if (atual == NULL) {
        return -1;
    }

    while (atual != NULL) {

        //só entra no if quando encontrar o elemento certo
        if (atual->elemento == no) {
            if (atual->esquerda == NULL && atual->direita == NULL) {
                return 0; 
            } else if (atual->esquerda != NULL && atual->direita != NULL) {
                return 2; 
            } else {
                return 1; 
            }
        } 

        // Se o valor procurado for menor, vamos para a esquerda
        else if (atual->elemento > no) {
            atual = atual->esquerda;
        } 
        // Se o valor procurado for maior, vamos para a direita
        else {
            atual = atual->direita;
        }
    }
    return -1;
}

int nopai_arvore(arvore *a, int no){
    noarvore *atual = raiz_arvore(a);
    noarvore *pai = NULL;

    //caso a árvore estiver vazia
    if (atual == NULL) {
        return -1;
    }

    //caso o nó for a própria raiz, ela não tem pai
    if (atual->elemento == no) return -1;

    while (atual != NULL) {
        if (atual->elemento == no) {
            return pai->elemento;
        } 

        pai = atual; 

        // Se o valor procurado for menor, vamos para a esquerda
        if (atual->elemento > no) {
            atual = atual->esquerda;
        } 
        // Se o valor procurado for maior, vamos para a direita
        else {
            atual = atual->direita;
        }
    }
    return -1;
}

int maior_arvore(arvore *a){
    noarvore *atual = raiz_arvore(a);

    //caso a árvore estiver vazia
    if (atual == NULL) {
        return -1;
    }

    while (atual->direita != NULL){
        atual = atual->direita;
    }
    return atual->elemento;
}

int menor_arvore(arvore *a){
    noarvore *atual = raiz_arvore(a);

    //caso a árvore estiver vazia
    if (atual == NULL) {
        return -1;
    }

    while (atual->esquerda != NULL){
        atual = atual->esquerda;
    }
    return atual->elemento;
}

int descendente_arvore (arvore *a, int descendente, int ancestral) {
    noarvore *atual = raiz_arvore(a);

    //procurando ancestral
    while (atual != NULL && atual->elemento != ancestral) {
        if (ancestral < atual->elemento) {
            atual = atual->esquerda;
        } else {
            atual = atual->direita;
        }
    }

    // Se o loop terminou e 'atual' é NULL, o ancestral não existe na árvore
    if (atual == NULL) {
        return 0; 
    }

    while (atual != NULL) {
        if (atual->elemento == descendente) {
            return 1; 
        }
        
        if (descendente < atual->elemento) {
            atual = atual->esquerda;
        } else {
            atual = atual->direita;
        }
    }

    return 0;
}