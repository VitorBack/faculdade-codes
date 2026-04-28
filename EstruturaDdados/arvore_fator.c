#include <stdio.h>
#include <stdlib.h>

typedef struct noarvore {
    int elemento;
    int fator_balanceamento;  
    struct noarvore *esquerda;
    struct noarvore *direita;
} noarvore;

typedef struct {
    int elemento;             
    noarvore *esquerda;      
} arvore;

static int altura_no(noarvore *no) {
    if (!no) return 0;
    int alt_esq = altura_no(no->esquerda);
    int alt_dir = altura_no(no->direita);
    return 1 + (alt_esq > alt_dir ? alt_esq : alt_dir);
}

static void recalcula_fatores(noarvore *no) {
    if (!no) return;
    recalcula_fatores(no->esquerda);
    recalcula_fatores(no->direita);
    no->fator_balanceamento = altura_no(no->direita) - altura_no(no->esquerda);
}

void inicializa_arvore(arvore *a) {
    a->esquerda = NULL;
    a->elemento = 0;
}

int tamanho_arvore(arvore *a) {
    return a->elemento;
}

noarvore *raiz_arvore(arvore *a) {
    return a->esquerda;
}

static noarvore *aloca_no(int elemento) {
    noarvore *no = (noarvore *) malloc(sizeof(noarvore));
    if (no) {
        no->elemento            = elemento;
        no->fator_balanceamento = 0;
        no->esquerda            = NULL;
        no->direita             = NULL;
    }
    return no;
}

void insere_arvore(arvore *a, int elemento) {
    noarvore *no = aloca_no(elemento);
    if (!no) {
        fprintf(stderr, "Erro: memória insuficiente.\n");
        return;
    }

    if (!raiz_arvore(a)) {
        a->elemento++;
        a->esquerda = no;
    } else {
        noarvore *atual = a->esquerda;
        int inserido = 0;

        while (!inserido) {
            if (elemento < atual->elemento) {
                if (atual->esquerda)
                    atual = atual->esquerda;
                else {
                    atual->esquerda = no;
                    a->elemento++;
                    inserido = 1;
                }
            } else if (elemento > atual->elemento) {
                if (atual->direita)
                    atual = atual->direita;
                else {
                    atual->direita = no;
                    a->elemento++;
                    inserido = 1;
                }
            } else {
                free(no);
                printf("Aviso: elemento %d ja existe na arvore.\n", elemento);
                return;         
            }
        }
    }

    recalcula_fatores(raiz_arvore(a));
}


static void imprime_no(noarvore *no) {
    printf("%d(%d) ", no->elemento, no->fator_balanceamento);
}

static void percorre(noarvore *no, int ordem) {
    if (!no) return;
    if (ordem == 1) imprime_no(no);        
    percorre(no->esquerda, ordem);
    if (ordem == 2) imprime_no(no);         
    percorre(no->direita, ordem);
    if (ordem == 3) imprime_no(no);        
}

void preordem_arvore(arvore *a) {
    if (raiz_arvore(a)) percorre(a->esquerda, 1);
}

void emordem_arvore(arvore *a) {
    if (raiz_arvore(a)) percorre(a->esquerda, 2);
}

void posordem_arvore(arvore *a) {
    if (raiz_arvore(a)) percorre(a->esquerda, 3);
}

static void libera_nos(noarvore *no) {
    if (!no) return;
    libera_nos(no->esquerda);
    libera_nos(no->direita);
    free(no);
}

void libera_arvore(arvore *a) {
    libera_nos(a->esquerda);
    a->esquerda = NULL;
    a->elemento = 0;
}


static void exibe_menu(void) {
    printf("\n╔══════════════════════════════════════╗\n");
    printf("║   ARVORE COM FATOR DE BALANCEAMENTO  ║\n");
    printf("╠══════════════════════════════════════╣\n");
    printf("║  1 - Inserir elemento                ║\n");
    printf("║  2 - Percurso Em Ordem               ║\n");
    printf("║  3 - Percurso Pre-Ordem              ║\n");
    printf("║  4 - Percurso Pos-Ordem              ║\n");
    printf("║  5 - Tamanho da arvore               ║\n");
    printf("║  0 - Sair                            ║\n");
    printf("╚══════════════════════════════════════╝\n");
    printf("Opcao: ");
}


int main(void) {
    arvore a;
    inicializa_arvore(&a);

    int opcao, valor;

    do {
        exibe_menu();
        if (scanf("%d", &opcao) != 1) break;

        switch (opcao) {
            case 1:
                printf("Valor a inserir: ");
                if (scanf("%d", &valor) == 1)
                    insere_arvore(&a, valor);
                break;

            case 2:
                printf("\nPercurso Em Ordem: ");
                emordem_arvore(&a);
                printf("\n");
                break;

            case 3:
                printf("\nPercurso Pre-Ordem: ");
                preordem_arvore(&a);
                printf("\n");
                break;

            case 4:
                printf("\nPercurso Pos-Ordem: ");
                posordem_arvore(&a);
                printf("\n");
                break;

            case 5:
                printf("\nTotal de nos: %d\n", tamanho_arvore(&a));
                break;

            case 0:
                printf("Encerrando...\n");
                break;

            default:
                printf("Opcao invalida.\n");
        }
    } while (opcao != 0);

    libera_arvore(&a);
    return 0;
}