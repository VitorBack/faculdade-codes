from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# Configurações da janela
g_posicao_x = 50
g_posicao_y = 50
g_largura = 500
g_altura = 500
g_titulo = "Projeto Base"

g_idle = 0
g_timer = 0
g_timer_value = 1


def gDesenha():
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(0, 0, 0)

    # Eixos (já existentes)
    glBegin(GL_LINE_STRIP)
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(0.0, -1.0)
    glVertex2f(0.0, 1.0)
    glEnd()







    glutSwapBuffers()


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


def gInicializa():
    # Cor de fundo: branco
    glClearColor(1, 1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glutSwapBuffers()


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
    glutCreateWindow(g_titulo.encode("utf-8"))

    # Funções da GLUT
    glutDisplayFunc(gDesenha)
    glutReshapeFunc(gRedimensiona)
    glutKeyboardFunc(gTeclado)
    glutSpecialFunc(gEspeciais)
    glutMouseFunc(gMouse)

    # Movimento do mouse
    glutMotionFunc(gMousePressionado)
    glutPassiveMotionFunc(gMouseLiberado)

    # Scroll do mouse
    # Nem todas as versões do PyOpenGL possuem essa função
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