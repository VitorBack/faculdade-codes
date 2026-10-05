from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from casa import DesenhaCasa
from plano import DesenhaPlano


TAM_JANELA = 100.0
escala = 0.0
rotacao = 1.0
translacao = 0.0
x_translacao = 0.0
y_translacao = 0.0
x_escala = 1.0
y_escala = 1.0
angulo_rotacao = 0.0
angulo_rotacao_inferior = 0.0

g_posicao_x = 50
g_posicao_y = 50
g_largura = 600
g_altura = 600
g_titulo = "Projeto Base 2D - a4c1"

g_idle = 0
g_timer = 0
g_timer_value = 1


def gDesenha():
    glEnable(GL_DEPTH_TEST)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    DesenhaPlano(TAM_JANELA, True, True, False)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x_translacao, y_translacao, 0.0)
    glTranslatef(25, 25, 0.0)
    glRotatef(angulo_rotacao, 0, 0, 1)
    glScalef(x_escala, y_escala, 1.0)
    glTranslatef(-25, -25, 0.0)
    DesenhaCasa(0, 0, 50, True)
    glPopMatrix()

    # Centraliza a réplica no quadrante inferior esquerdo.
    deslocamento = -TAM_JANELA / 2 - 25
    glPushMatrix()
    glTranslatef(deslocamento, deslocamento, 0.0)
    glTranslatef(25, 25, 0.0)
    glRotatef(angulo_rotacao_inferior, 0, 0, 1)
    glTranslatef(-25, -25, 0.0)
    DesenhaCasa(0, 0, 50, True)
    glPopMatrix()

    glutSwapBuffers()


def gRedimensiona(largura, altura):
    if altura == 0:
        altura = 1

    if largura == 0:
        largura = 1

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glViewport(0, 0, largura, altura)

    if largura < altura:
        aspecto = altura / largura
        gluOrtho2D(
            -TAM_JANELA,
            TAM_JANELA,
            -TAM_JANELA * aspecto,
            TAM_JANELA * aspecto
        )
    else:
        aspecto = largura / altura
        gluOrtho2D(
            -TAM_JANELA * aspecto,
            TAM_JANELA * aspecto,
            -TAM_JANELA,
            TAM_JANELA
        )


def gTeclado(tecla, x, y):
    global escala, rotacao, translacao
    global angulo_rotacao_inferior

    if isinstance(tecla, bytes):
        tecla = tecla.decode("utf-8")
    tecla = tecla.lower()

    if tecla == '\x1b':
        exit(0)

    if tecla in ('w', 'd'):
        angulo_rotacao_inferior += 5
    elif tecla in ('s', 'a'):
        angulo_rotacao_inferior -= 5
    elif tecla == 'r':
        print("rotacao: x%d y%d" % (x, y))
        rotacao = 1
        translacao = escala = 0
    elif tecla == 'e':
        print("escala: x%d y%d" % (x, y))
        escala = 1
        translacao = rotacao = 0
    elif tecla == 't':
        print("translacao: x%d y%d" % (x, y))
        translacao = 1
        escala = rotacao = 0

    glutPostRedisplay()


def gEspeciais(tecla, x, y):
    global x_translacao, y_translacao
    global x_escala, y_escala
    global angulo_rotacao

    if tecla == GLUT_KEY_UP:
        print("tecla up")
        if translacao:
            y_translacao += 5
        if escala:
            y_escala += 0.1
        if rotacao:
            angulo_rotacao += 5
    elif tecla == GLUT_KEY_DOWN:
        print("tecla down")
        if translacao:
            y_translacao -= 5
        if escala:
            y_escala -= 0.1
        if rotacao:
            angulo_rotacao -= 5
    elif tecla == GLUT_KEY_LEFT:
        print("tecla left")
        if translacao:
            x_translacao -= 5
        if escala:
            x_escala -= 0.1
        if rotacao:
            angulo_rotacao -= 5
    elif tecla == GLUT_KEY_RIGHT:
        print("tecla right")
        if translacao:
            x_translacao += 5
        if escala:
            x_escala += 0.1
        if rotacao:
            angulo_rotacao += 5

    glutPostRedisplay()


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
    glClearColor(1, 1, 1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-TAM_JANELA, TAM_JANELA, -TAM_JANELA, TAM_JANELA)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()

    print("Comandos:")
    print("Setas - controlar a casa superior")
    print("W/D - girar a casa inferior em +5 graus")
    print("S/A - girar a casa inferior em -5 graus")
    print("R - modo rotacao da casa superior (ativo ao iniciar)")
    print("E - modo escala")
    print("T - modo translacao")
    print("ESC - sair")

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB
    )

    glutInitWindowPosition(
        g_posicao_x,
        g_posicao_y
    )

    glutInitWindowSize(
        g_largura,
        g_altura
    )

    glutCreateWindow(
        g_titulo.encode("utf-8")
    )

    glutDisplayFunc(gDesenha)
    glutReshapeFunc(gRedimensiona)
    glutKeyboardFunc(gTeclado)
    glutSpecialFunc(gEspeciais)
    glutMouseFunc(gMouse)
    glutMotionFunc(gMousePressionado)
    glutPassiveMotionFunc(gMouseLiberado)
    glutMouseWheelFunc(gMouseScroll)

    if g_idle:
        glutIdleFunc(gSistemaOcioso)

    if g_timer:
        glutTimerFunc(
            g_timer_value,
            gTempoExecucao,
            1
        )

    gInicializa()

    glutMainLoop()


main()
