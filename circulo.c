#include <stdio.h>
#include "circulo.h"

int main() {
    Circulo circ;
    Ponto p_teste;
    float x, y, r;

    printf("Digite o centro do circulo (x y) e o raio: ");
    scanf("%f %f %f", &x, &y, &r);
    inicializarCirculo(&circ, x, y, r);

    printf("\n--- Dados do Circulo ---\n");
    imprimirCirculo(circ);

    printf("\nDigite as coordenadas de um ponto para testar (x y): ");
    scanf("%f %f", &x, &y);
    inicializarPonto(&p_teste, x, y);

    if (pontoNoCirculo(circ, p_teste)) { [cite: 37]
        printf("O ponto (%.2f, %.2f) PERTENCE ao circulo.\n", x, y);
    } else {
        printf("O ponto (%.2f, %.2f) NAO pertence ao circulo.\n", x, y);
    }

    return 0;
}