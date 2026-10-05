"""Conversão de casa.h: funções de desenho da casa em OpenGL."""

from math import cos, pi, sin

from OpenGL.GL import (
    GL_LINE_LOOP, GL_QUADS, GL_TRIANGLES,
    glBegin, glColor3f, glEnd, glPopMatrix, glPushMatrix,
    glTranslatef, glVertex2f,
)


def Modulo(n: float) -> float:
    return -n if n < 0 else n


def Distancia(p1: float, p2: float) -> float:
    if (p1 >= 0 and p2 >= 0) or (p1 < 0 and p2 < 0):
        return Modulo(p2 - p1)
    return Modulo(p1) + Modulo(p2)


def DesenhaCasa(x_p1: float, y_p1: float, altura: float, quadro: int) -> None:
    raio = 35
    linhas_pontos = 50
    fator_pi = 2
    x_p2 = x_p1 + altura
    y_p2 = y_p1 + altura

    glPushMatrix()
    glTranslatef(25, 25, 0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINE_LOOP)
    # 100 vértices, sem acumular erros de arredondamento no ângulo.
    for i in range(fator_pi * linhas_pontos):
        angulo = i * pi / linhas_pontos
        glVertex2f(raio * cos(angulo), raio * sin(angulo))
    glEnd()
    glPopMatrix()

    if quadro:
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x_p1, y_p1)
        glVertex2f(x_p1, y_p2)
        glVertex2f(x_p2, y_p2)
        glVertex2f(x_p2, y_p1)
        glEnd()

    glColor3f(0.0, 0.0, 1.0)
    x_base = Distancia(x_p1, x_p2) / 10
    glBegin(GL_QUADS)  # Base.
    glVertex2f(x_p1 + x_base, y_p1)
    glVertex2f(x_p1 + x_base, y_p2 - altura / 2.5)
    glVertex2f(x_p2 - x_base, y_p2 - altura / 2.5)
    glVertex2f(x_p2 - x_base, y_p1)
    glEnd()

    # Valor original preservado: o OpenGL limita o verde 5.0 a 1.0.
    glColor3f(1.0, 5.0, 0.0)
    x_base = Distancia(x_p1, x_p2) / 2
    glBegin(GL_TRIANGLES)  # Telhado.
    glVertex2f(x_p1, y_p2 - altura / 2.5)
    glVertex2f(x_p1 + x_base, y_p2)
    glVertex2f(x_p2, y_p2 - altura / 2.5)
    glEnd()
