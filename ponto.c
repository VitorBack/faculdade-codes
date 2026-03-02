#include <stdio.h>
#include "ponto.h" 

int main() {
    Ponto p1, p2;
    float x, y;

    printf("Digite as coordenadas do Ponto 1 (x y): ");
    scanf("%f %f", &x, &y);
    inicializarPonto(&p1, x, y);

    printf("Digite as coordenadas do Ponto 2 (x y): ");
    scanf("%f %f", &x, &y);
    inicializarPonto(&p2, x, y);

    printf("\n--- Dados dos Pontos ---\n");
    printf("Ponto 1: (%.2f, %.2f)\n", getX(p1), getY(p1));
    printf("Ponto 2: (%.2f, %.2f)\n", getX(p2), getY(p2));

    float dist = calcularDistancia(p1, p2); 
    printf("\nDistancia entre os pontos: %.4f\n", dist);

    return 0;
}