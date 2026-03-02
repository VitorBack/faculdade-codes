#ifndef PONTO_H
#define PONTO_H

#include <math.h> 

typedef struct {
    float x;
    float y;
} Ponto;

void inicializarPonto(Ponto *p, float x, float y) {
    p->x = x;
    p->y = y;
}


float getX(Ponto p) {
    return p.x;
}

float getY(Ponto p) {
    return p.y;
}


float calcularDistancia(Ponto p1, Ponto p2) {
    return sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2));
}

#endif