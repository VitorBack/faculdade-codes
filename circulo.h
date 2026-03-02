#ifndef CIRCULO_H
#define CIRCULO_H

#include "ponto.h" 

typedef struct {
    Ponto centro; 
    float raio;  
} Circulo;

void inicializarCirculo(Circulo *c, float x, float y, float r) {
    inicializarPonto(&(c->centro), x, y);
    c->raio = r;                         
}

void imprimirCirculo(Circulo c) {
    printf("Centro: (%.2f, %.2f) | Raio: %.2f\n", getX(c.centro), getY(c.centro), c.raio); [cite: 36]
}

int pontoNoCirculo(Circulo c, Ponto p) {

    float d = calcularDistancia(c.centro, p);
    if (d <= c.raio) {
        return 1; 
    } else {
        return 0; 
    }
}

#endif