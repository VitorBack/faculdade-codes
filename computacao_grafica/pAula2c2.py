from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys


# Configurações da janela
g_posicao_x = 50
g_posicao_y = 50
g_largura = 600
g_altura = 600
g_titulo = "Projeto Base"

g_idle = 0
g_timer = 0
g_timer_value = 1


# ============================================================
# MEUS DESENHOS
# ============================================================

def gMeusDesenhos():

    # --------------------------------------------------------
    # Circunferência usando seno e cosseno
    # --------------------------------------------------------

    raio = 0.2
    linhas_pontas = 30
    fator_pi = 2

    glColor3f(1, 0, 0)
    glPointSize(2)
    glPushMatrix()

    glPushMatrix()
    glTranslatef(0.25, -0.75, 0)
    glBegin(GL_LINES)

    angulo = 0

    while angulo < (fator_pi * math.pi):

        glVertex2f(
            raio * math.cos(angulo),
            raio * math.sin(angulo)
        )

        angulo += math.pi / linhas_pontas

    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.75, -0.7, 0)
    glBegin(GL_LINE_LOOP)

    angulo = 0

    while angulo < (fator_pi * math.pi):

        glVertex2f(
            raio * math.cos(angulo),
            raio * math.sin(angulo)
        )

        angulo += math.pi / linhas_pontas

    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.75, -0.25, 0)
    glBegin(GL_LINE_STRIP)

    angulo = 1

    while angulo < (fator_pi * math.pi):

        glVertex2f(
            raio * math.cos(angulo),
            raio * math.sin(angulo)
        )

        angulo += math.pi / linhas_pontas

    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.25, -0.25, 0)
    glBegin(GL_POINTS)

    angulo = 0

    while angulo < (fator_pi * math.pi):

        glVertex2f(
            raio * math.cos(angulo),
            raio * math.sin(angulo)
        )

        angulo += math.pi / linhas_pontas

    glEnd()
    glPopMatrix()
# ============================================================
# DESENHA
# ============================================================

def gDesenha():

    glEnable(GL_DEPTH_TEST)

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    # ========================================================
    # EIXOS
    # ========================================================

    glColor3f(0, 0, 0)

    # Eixo horizontal
    glBegin(GL_LINES)
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glEnd()

    # Eixo vertical
    glBegin(GL_LINES)
    glVertex2f(0.0, -1.0)
    glVertex2f(0.0, 1.0)
    glEnd()


    # ========================================================
    # TRIÂNGULOS
    # ========================================================

    glColor3f(1, 0, 0)

    glBegin(GL_TRIANGLES)

    glVertex2f(-0.9, 0.9)
    glVertex2f(-0.8, 0.8)
    glVertex2f(-0.7, 0.9)

    glVertex2f(-0.6, 0.8)
    glVertex2f(-0.5, 0.9)
    glVertex2f(-0.4, 0.8)

    glEnd()


    # ========================================================
    # TRIÂNGULOS EM SEQUÊNCIA
    # ========================================================

    glColor3f(1, 0, 0)

    glBegin(GL_TRIANGLES)

    glVertex2f(-0.9, 0.6)
    glVertex2f(-0.8, 0.5)
    glVertex2f(-0.7, 0.6)

    glVertex2f(-0.8, 0.5)
    glVertex2f(-0.7, 0.6)
    glVertex2f(-0.6, 0.5)

    glVertex2f(-0.7, 0.6)
    glVertex2f(-0.6, 0.5)
    glVertex2f(-0.5, 0.6)

    glVertex2f(-0.6, 0.5)
    glVertex2f(-0.5, 0.6)
    glVertex2f(-0.4, 0.5)

    glEnd()


    # ========================================================
    # TRIANGLE FAN
    # ========================================================

    glColor3f(1, 0, 0)

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(-0.2, 0.9)
    glVertex2f(-0.4, 0.7)
    glVertex2f(-0.3, 0.6)
    glVertex2f(-0.1, 0.6)
    glVertex2f(-0.0, 0.7)

    glEnd()


    # ========================================================
    # QUADRADO
    # ========================================================

    glColor3f(1, 0, 0)

    glBegin(GL_QUADS)

    glVertex2f(-0.9, 0.3)
    glVertex2f(-0.9, 0.1)
    glVertex2f(-0.8, 0.1)
    glVertex2f(-0.8, 0.3)

    glEnd()


    # ========================================================
    # QUAD STRIP
    # ========================================================

    glColor3f(1, 0, 0)

    glBegin(GL_QUAD_STRIP)

    glVertex2f(-0.7, 0.3)
    glVertex2f(-0.7, 0.1)

    glVertex2f(-0.5, 0.3)
    glVertex2f(-0.5, 0.1)

    glVertex2f(-0.3, 0.4)
    glVertex2f(-0.3, 0.0)

    glVertex2f(-0.1, 0.3)
    glVertex2f(-0.1, 0.1)

    glEnd()


    # ========================================================
    # LINHA LOOP
    # ========================================================

    glBegin(GL_LINE_LOOP)

    glVertex2f(-0.7, 0.9)
    glVertex2f(-0.6, 0.8)

    glEnd()


    # ========================================================
    # TRIANGLE FAN
    # ========================================================

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(-0.2, 0.9)
    glVertex2f(-0.4, 0.7)
    glVertex2f(-0.3, 0.6)
    glVertex2f(-0.1, 0.6)
    glVertex2f(-0.0, 0.7)

    glEnd()


    # ========================================================
    # LINHA ZIG-ZAG
    # ========================================================

    glBegin(GL_LINE_STRIP)

    glVertex2f(-0.9, -0.1)
    glVertex2f(-0.8, -0.2)
    glVertex2f(-0.7, -0.1)
    glVertex2f(-0.6, -0.2)
    glVertex2f(-0.5, -0.1)
    glVertex2f(-0.4, -0.2)

    glEnd()


    # ========================================================
    # LINE LOOP
    # ========================================================

    glBegin(GL_LINE_LOOP)

    glVertex2f(-0.9, -0.5)
    glVertex2f(-0.8, -0.6)
    glVertex2f(-0.7, -0.5)
    glVertex2f(-0.6, -0.6)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.4, -0.6)
    glVertex2f(-0.9, -0.5)

    glEnd()


    # ========================================================
    # OUTRO LINE STRIP
    # ========================================================

    glBegin(GL_LINE_STRIP)

    glVertex2f(-0.2, -0.1)
    glVertex2f(-0.4, -0.3)
    glVertex2f(-0.3, -0.4)
    glVertex2f(-0.1, -0.4)
    glVertex2f(-0.0, -0.3)

    glEnd()


    # ========================================================
    # OUTRO LINE LOOP
    # ========================================================

    glBegin(GL_LINE_LOOP)

    glVertex2f(-0.2, -0.5)
    glVertex2f(-0.4, -0.7)
    glVertex2f(-0.3, -0.8)
    glVertex2f(-0.1, -0.8)
    glVertex2f(-0.0, -0.7)
    glVertex2f(-0.2, -0.5)

    glEnd()


    # ========================================================
    # DESENHO DA FUNÇÃO gMeusDesenhos
    # ========================================================

    gMeusDesenhos()


    # Atualiza a tela
    glutSwapBuffers()


# ============================================================
# FUNÇÕES DA GLUT
# ============================================================

def gRedimensiona(largura, altura):
    pass


def gTeclado(tecla, x, y):
    pass


def gEspeciais(tecla, x, y):
    pass


def gMouse(botao, estado, x, y):
    pass


def gMousePressionado(x, y):
    pass


def gMouseLiberado(x, y):
    pass


def gMouseScroll(botao, direcao, x, y):
    pass


def gSistemaOcioso():
    pass


def gTempoExecucao(valor):
    pass


# ============================================================
# INICIALIZAÇÃO
# ============================================================

def gInicializa():

    # Cor de fundo: ciano
    glClearColor(0, 1, 1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    glutSwapBuffers()


# ============================================================
# MAIN
# ============================================================

def main():

    # Inicialização da GLUT
    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_DEPTH |
        GLUT_RGB
    )

    # Posição da janela
    glutInitWindowPosition(
        g_posicao_x,
        g_posicao_y
    )

    # Tamanho da janela
    glutInitWindowSize(
        g_largura,
        g_altura
    )

    # Criação da janela
    glutCreateWindow(
        g_titulo.encode("utf-8")
    )

    # Funções da GLUT
    glutDisplayFunc(gDesenha)
    glutReshapeFunc(gRedimensiona)
    glutKeyboardFunc(gTeclado)
    glutSpecialFunc(gEspeciais)
    glutMouseFunc(gMouse)

    glutMotionFunc(gMousePressionado)
    glutPassiveMotionFunc(gMouseLiberado)

    # Scroll do mouse
    try:
        glutMouseWheelFunc(gMouseScroll)
    except:
        pass

    # Idle
    if g_idle:
        glutIdleFunc(gSistemaOcioso)

    # Timer
    if g_timer:
        glutTimerFunc(
            g_timer_value,
            gTempoExecucao,
            1
        )

    # Inicialização
    gInicializa()

    # Loop principal
    glutMainLoop()


if __name__ == "__main__":
    main()