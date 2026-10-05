"""Conversão de plano.h: eixos, marcas e rótulos do plano cartesiano."""

from math import isfinite

from OpenGL.GL import (
    GL_LINES, glBegin, glColor3f, glEnd, glRasterPos2f, glVertex2f,
)
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_10, glutBitmapCharacter


def DesenhaPlano(h: float, pontos: int, rotulos: int, corbranca: int) -> None:
    if not isfinite(h) or h <= 0:
        raise ValueError("h deve ser um número positivo e finito.")

    intervalo = h / 10.0
    if corbranca:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(0.0, 0.0, 0.0)

    glBegin(GL_LINES)
    glVertex2f(-h, 0.0)
    glVertex2f(h, 0.0)
    glVertex2f(0.0, -h)
    glVertex2f(0.0, h)
    glEnd()

    if pontos:
        glBegin(GL_LINES)
        # 21 posições de -h a +h, incluindo o zero.
        for i in range(-10, 11):
            x = y = i * intervalo
            glVertex2f(-intervalo / 20, y)
            glVertex2f(intervalo / 20, y)
            glVertex2f(x, -intervalo / 20)
            glVertex2f(x, intervalo / 20)
        glEnd()

        if rotulos:
            # O vetor C tinha 9 itens, mas era acessado 10 vezes.
            # Geramos os rótulos 1 a 10 e desenhamos cada caractere.
            for i in range(1, 11):
                rxy = i * intervalo
                posicoes = (
                    (-(intervalo * 4) / 20, rxy),
                    (-(intervalo * 4) / 20, -rxy),
                    (rxy, -(intervalo * 3.5) / 10),
                    (-rxy, -(intervalo * 3.5) / 10),
                )
                for x, y in posicoes:
                    glRasterPos2f(x, y)
                    for caractere in str(i):
                        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(caractere))
