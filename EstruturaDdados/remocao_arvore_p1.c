#ifndef REMOCAO_ARVORE_P1_H
#define REMOCAO_ARVORE_P1_H
#include "arvore.h"

static int eh_folha(No *no) {
    return (no->esquerda == NULL && no->direita == NULL);
}

static int conta_filhos(No *no) {
    int c = 0;
    if (no->esquerda) c++;
    if (no->direita)  c++;
    return c;
}

static No* _remove_folha(No *raiz, int valor, int *removido) {
    if (raiz == NULL) {
        *removido = 0;   // nó não encontrado
        return NULL;
    }

    if (valor < raiz->elemento) {
        raiz->esquerda = _remove_folha(raiz->esquerda, valor, removido);
    } else if (valor > raiz->elemento) {
        raiz->direita  = _remove_folha(raiz->direita,  valor, removido);
    } else {
        // Nó encontrado — verifica se é folha
        if (eh_folha(raiz)) {
            free(raiz);
            *removido = 1;
            return NULL;   // desliga o nó da árvore
        } else {
            *removido = -1; // existe mas não é folha
        }
    }

    return raiz;
}

void remove_folha_arvore(arvore *a, int no) {
    int removido = 0;
    a->raiz = _remove_folha(a->raiz, no, &removido);

    if (removido == 1)
        printf("[remove_folha] No %d removido com sucesso.\n", no);
    else if (removido == -1)
        printf("[remove_folha] No %d existe mas nao e folha; operacao cancelada.\n", no);
    else
        printf("[remove_folha] No %d nao encontrado na arvore.\n", no);
}

static No* _remove_filho(No *raiz, int valor, int *status) {
    if (raiz == NULL) {
        *status = 0;   // não encontrado
        return NULL;
    }

    if (valor < raiz->elemento) {
        raiz->esquerda = _remove_filho(raiz->esquerda, valor, status);
    } else if (valor > raiz->elemento) {
        raiz->direita  = _remove_filho(raiz->direita,  valor, status);
    } else {
        // Nó encontrado — verifica se tem exatamente 1 filho
        int filhos = conta_filhos(raiz);

        if (filhos != 1) {
            // 0 filhos = folha; 2 filhos = outro caso
            *status = -1;
            return raiz;
        }

        // Identifica o único filho existente
        No *filho_unico = (raiz->esquerda != NULL)
                          ? raiz->esquerda
                          : raiz->direita;

        printf("[remove_filho] No %d removido; filho %d assume seu lugar.\n",
               raiz->elemento, filho_unico->elemento);

        free(raiz);
        *status = 1;
        return filho_unico;   // filho sobe no lugar do pai removido
    }

    return raiz;
}

void remove_filho_arvore(arvore *a, int no) {
    int status = 0;
    a->raiz = _remove_filho(a->raiz, no, &status);

    if (status == -1)
        printf("[remove_filho] No %d nao tem exatamente 1 filho; operacao cancelada.\n", no);
    else if (status == 0)
        printf("[remove_filho] No %d nao encontrado na arvore.\n", no);
}

static No* _remove_noparcial(No *raiz, int valor, int *status) {
    if (raiz == NULL) {
        *status = 0;   // não encontrado
        return NULL;
    }

    if (valor < raiz->elemento) {
        raiz->esquerda = _remove_noparcial(raiz->esquerda, valor, status);
    } else if (valor > raiz->elemento) {
        raiz->direita  = _remove_noparcial(raiz->direita,  valor, status);
    } else {
        // Nó encontrado
        if (conta_filhos(raiz) != 2) {
            *status = -1;   // não tem 2 filhos
            return raiz;
        }

        int esq_folha = eh_folha(raiz->esquerda);
        int dir_folha = eh_folha(raiz->direita);

        if (!esq_folha && !dir_folha) {
            *status = -2;   // tem 2 filhos mas nenhum é folha
            return raiz;
        }

        No *filho_folha;
        No *filho_nao_folha;

        if (esq_folha) {
            // Prefere o filho esquerdo folha (se ambos forem folha,
            // qualquer um serve; aqui usamos o esquerdo por padrão)
            filho_folha     = raiz->esquerda;
            filho_nao_folha = raiz->direita;
        } else {
            filho_folha     = raiz->direita;
            filho_nao_folha = raiz->esquerda;
        }

        if (filho_nao_folha->elemento > filho_folha->elemento) {
            filho_folha->direita  = filho_nao_folha;
            filho_folha->esquerda = NULL;
        } else {
            filho_folha->esquerda = filho_nao_folha;
            filho_folha->direita  = NULL;
        }

        printf("[remove_parcial] No %d removido; folha %d assume seu lugar.\n",
               raiz->elemento, filho_folha->elemento);

        free(raiz);
        *status = 1;
        return filho_folha;   // folha sobe no lugar do nó removido
    }

    return raiz;
}

void remove_noparcial_arvore(arvore *a, int no) {
    int status = 0;
    a->raiz = _remove_noparcial(a->raiz, no, &status);

    if (status == -1)
        printf("[remove_parcial] No %d nao possui 2 filhos; operacao cancelada.\n", no);
    else if (status == -2)
        printf("[remove_parcial] No %d tem 2 filhos mas nenhum e folha; operacao cancelada.\n", no);
    else if (status == 0)
        printf("[remove_parcial] No %d nao encontrado na arvore.\n", no);
}

#endif 