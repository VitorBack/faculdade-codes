typedef struct {
	int elemento;
	struct noarvore *esquerda;
	struct noarvore *direita;
} noarvore, arvore;

void inicializa_arvore (arvore *a) {
	a->esquerda = NULL;
	a->elemento = 0; // número de nós da árvore
}

int tamanho_arvore (arvore *a) { return a->elemento; }

noarvore *raiz_arvore (arvore *a) { return a->esquerda; }

noarvore *alocano_arvore (int elemento) {
	noarvore *no = (noarvore *) malloc (sizeof (noarvore));
	if (no) {
		no->elemento = elemento;
		no->esquerda = NULL;
		no->direita = NULL;
	}
	return no;
}

void insere_arvore (arvore *a, int elemento) {
	noarvore *no = alocano_arvore (elemento);
	noarvore *noAtual = a->esquerda;
	int status_operacao = 1;
	if (no) {
		if (!raiz_arvore (a)) {
			a->elemento++;
			a->esquerda = no;
		}
		else {
			do {
				if (noAtual->elemento > elemento) {
					if (noAtual->esquerda) noAtual = noAtual->esquerda;
					else {
						a->elemento++;
						noAtual->esquerda = no;
						status_operacao = 0;
					}
				}
				else if (noAtual->elemento < elemento) {
					if (noAtual->direita) noAtual = noAtual->direita;
					else {
						a->elemento++;
						noAtual->direita = no;
						status_operacao = 0;
					}
				}
				else {
					free (no);
					status_operacao = 0;
				}
			} while (status_operacao);
		}
	}
}

void mostra_arvore (arvore *a, int ordem) {
	if (a) {
		if (ordem == 1) printf("%d, ", a->elemento);
		mostra_arvore (a->esquerda, ordem);
		if (ordem == 2) printf("%d, ", a->elemento);
		mostra_arvore (a->direita, ordem);
		if (ordem == 3) printf("%d, ", a->elemento);
	}
}

void preordem_arvore (arvore *a) {
	if (raiz_arvore (a)) mostra_arvore (a->esquerda, 1);
}

void emordem_arvore (arvore *a) {
	if (raiz_arvore (a)) mostra_arvore (a->esquerda, 2);
}

void posordem_arvore (arvore *a) {
	if (raiz_arvore (a)) mostra_arvore (a->esquerda, 3);
}