from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ==========================
# Variáveis globais
# ==========================

g_posicao_x = 50
g_posicao_y = 50
g_largura = 250
g_altura = 250
g_titulo = "Projeto Base"

g_idle = False
g_timer = False
g_timer_value = 1


# ==========================
# Callbacks
# ==========================

def gDesenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Desenhe aqui

    glutSwapBuffers()


def gRedimensiona(largura, altura):
    if altura == 0:
        altura = 1

    glViewport(0, 0, largura, altura)


def gTeclado(tecla, x, y):
    tecla = tecla.decode("utf-8")

    if tecla == '\x1b':      # ESC
        exit()


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
    glutPostRedisplay()


def gTempoExecucao(valor):
    glutPostRedisplay()
    glutTimerFunc(g_timer_value, gTempoExecucao, 1)


# ==========================
# Inicialização
# ==========================

def gInicializa():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


# ==========================
# Main
# ==========================

def main():
    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB)

    glutInitWindowPosition(g_posicao_x, g_posicao_y)
    glutInitWindowSize(g_largura, g_altura)

    glutCreateWindow(g_titulo.encode("utf-8"))

    glutDisplayFunc(gDesenha)
    glutReshapeFunc(gRedimensiona)
    glutKeyboardFunc(gTeclado)
    glutSpecialFunc(gEspeciais)
    glutMouseFunc(gMouse)
    glutMotionFunc(gMousePressionado)
    glutPassiveMotionFunc(gMouseLiberado)

    # Algumas versões do PyOpenGL não possuem suporte ao scroll.
    # Se a sua possuir, descomente a linha abaixo:
    #
    # glutMouseWheelFunc(gMouseScroll)

    if g_idle:
        glutIdleFunc(gSistemaOcioso)

    if g_timer:
        glutTimerFunc(g_timer_value, gTempoExecucao, 1)

    gInicializa()

    glutMainLoop()


if __name__ == "__main__":
    main()