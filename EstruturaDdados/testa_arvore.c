#include <stdio.h>

#include "arvore.h"

void main (void) {
	int i;
	int nos[] = { 100, 50, 30, 70, 20, 40, 60, 80, 10, 90, 5, 15, 150, 130, 170, 120, 140, 160, 180, 190, 185, 195, 65, 155 };
	arvore a;
	inicializa_arvore (&a);
	
	for (i = 0; i < 24; i++) insere_arvore (&a, nos[i]);

	printf ("\n\n Tamanho: %d", tamanho_arvore (&a));
	printf ("\n\nPreOrdem: "); preordem_arvore (&a);
	printf ("\n\n EmOrdem: "); emordem_arvore (&a);
	printf ("\n\nPosOrdem: "); posordem_arvore (&a);
	printf ("\n\n");
	
	system ("pause");
}
