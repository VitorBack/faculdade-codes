#include <stdio.h>
#include <stdlib.h>

int valor_no = 0;

typedef struct nolista{
	struct nolista *proximo;
	int s, t, i;
} nolista, lista;

void inicializa_lista (lista *l, int espaco) {
	nolista *no = (nolista *) malloc ((sizeof (nolista)));
	l->proximo = NULL;
	if (no) {
		no->proximo = NULL;
		no->s = 1;
		no->t = espaco;
		no->i = 0;
		l->proximo = no;
	}
}

void exibe_lista (lista *l) {
	int nrNo = 1;
	if (l->proximo) {
		printf ("Nr. | Id. | Sit | Tam | Endereco\n");
		do {
			l = l->proximo;
			printf ("%3d | %3d | %3d | %3d |   %6x\n",
				nrNo, l->i, l->s, l->t, l->proximo);
			nrNo++;
		} while (l->proximo);
	}
}

void retira_lista (lista *l, int i) {
	int status = 1;
	if (l->proximo) {
		do {
			l = l->proximo;
			if (l->i == i) {
				l->s = 1;
				l->i = 0;
				status = 0;
				break;
			}
		} while (l->proximo);
		if (status) printf ("Id. NAO consta na Lista...\n");
	}
}

void insere_lista (lista *l, int t) {
	nolista *noAtual = (nolista *) l->proximo;
	nolista *noAnterior = (nolista *) l->proximo;
	int status = 1;
	if (l->proximo) {
		do {
			if (noAtual->s == 1 && t <= noAtual->t) {
				status = 0;
				valor_no++;
				if (noAtual->t == t) {
					noAtual->s = 0;
					noAtual->i = valor_no;
				}
				else {
					nolista *no = (nolista *) malloc (sizeof (nolista));
					if (no) {
						if (l->proximo == noAtual) l->proximo = (nolista *) no;
						else noAnterior->proximo = (nolista *) no;
						noAtual->t -= t;
						no->s = 0;
						no->t = t;
						no->i = valor_no;
						no->proximo = (nolista *) noAtual;
					}
				}
				break;
			}
			noAnterior = noAtual;
			noAtual = noAtual->proximo;
		} while (noAtual);
	}
	if (status) printf ("No' NAO pode ser inserido na Lista...\n");
}

int main(void) {
    lista minhaLista;
    int opcao = 0, valor = 0;

    printf("Informe o tamanho total da memoria inicial: ");
    scanf("%d", &valor);
    inicializa_lista(&minhaLista, valor);

    do {
        printf("\n========= MENU TAD LISTA =========\n");
        printf("1. Inserir (Alocar Memoria)\n");
        printf("2. Retirar (Liberar por ID)\n");
        printf("3. Exibir Lista\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o tamanho a ser alocado: ");
                scanf("%d", &valor);
                insere_lista(&minhaLista, valor);
                break;
            case 2:
                printf("Digite o ID para liberar: ");
                scanf("%d", &valor);
                retira_lista(&minhaLista, valor);
                break;
            case 3:
                exibe_lista(&minhaLista);
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);

    return 0;
}