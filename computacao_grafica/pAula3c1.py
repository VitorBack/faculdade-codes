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
g_titulo = "Casa com Primitivas OpenGL"

g_idle = 0
g_timer = 0
g_timer_value = 1


def desenha_retangulo(x1, y1, x2, y2, cor):
    glColor3f(*cor)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def desenha_circulo(contorno_x, contorno_y, raio, segmentos=180):
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)

    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = contorno_x + raio * math.cos(angulo)
        y = contorno_y + raio * math.sin(angulo)
        glVertex2f(x, y)

    glEnd()
    glLineWidth(1.0)


def gDesenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # ========================================================
    # EIXOS CARTESIANOS
    # ========================================================

    glColor3f(0.55, 0.0, 0.0)  # vermelho escuro
    glLineWidth(1.0)
    glBegin(GL_LINES)

    # Eixo horizontal
    glVertex2f(-1.3, 0.0)
    glVertex2f(1.3, 0.0)

    # Eixo vertical
    glVertex2f(0.0, -1.0)
    glVertex2f(0.0, 1.0)

    glEnd()

    # ========================================================
    # CASA
    # ========================================================

    # Corpo azul da casa. Todas as coordenadas da figura foram
    # reduzidas para 10% do tamanho anterior.
    desenha_retangulo(
        0.008, 0.000,
        0.072, 0.055,
        (0.0, 0.0, 1.0)
    )

    # Telhado amarelo
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.000, 0.055)  # canto esquerdo
    glVertex2f(0.080, 0.055)  # canto direito
    glVertex2f(0.040, 0.086)  # ponta do telhado
    glEnd()

    # Porta cinza
    desenha_retangulo(
        0.014, 0.000,
        0.030, 0.039,
        (0.55, 0.62, 0.70)
    )

    # Maçaneta da porta
    glColor3f(0.1, 0.1, 0.1)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glVertex2f(0.027, 0.020)
    glEnd()

    # Janela cinza
    desenha_retangulo(
        0.040, 0.021,
        0.065, 0.039,
        (0.48, 0.56, 0.66)
    )

    # Contorno e divisórias da janela
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(1.0)

    glBegin(GL_LINE_LOOP)
    glVertex2f(0.040, 0.021)
    glVertex2f(0.065, 0.021)
    glVertex2f(0.065, 0.039)
    glVertex2f(0.040, 0.039)
    glEnd()

    glBegin(GL_LINES)
    # Divisão vertical
    glVertex2f(0.0525, 0.021)
    glVertex2f(0.0525, 0.039)

    # Divisão horizontal
    glVertex2f(0.040, 0.030)
    glVertex2f(0.065, 0.030)
    glEnd()

    # Circunferência ao redor da casa
    desenha_circulo(
        contorno_x=0.040,
        contorno_y=0.039,
        raio=0.062
    )

    glutSwapBuffers()


# ============================================================
# FUNÇÕES DA GLUT
# ============================================================

def gRedimensiona(largura, altura):
    if altura == 0:
        altura = 1

    glViewport(0, 0, largura, altura)

    # Ajusta a projeção sem deformar a circunferência.
    proporcao = largura / float(altura)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if largura >= altura:
        glOrtho(-proporcao, proporcao, -1.0, 1.0, -1.0, 1.0)
    else:
        glOrtho(-1.0, 1.0, -1.0 / proporcao, 1.0 / proporcao, -1.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def gTeclado(tecla, x, y):
    # Fecha o programa com ESC.
    if tecla == b"\x1b":
        sys.exit(0)


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
    glutTimerFunc(g_timer_value, gTempoExecucao, valor)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

def gInicializa():
    # Fundo branco, como na imagem de referência.
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # A cena é 2D; desativar a profundidade evita que uma forma impeça
    # a exibição de outra desenhada posteriormente na mesma profundidade.
    glDisable(GL_DEPTH_TEST)


# ============================================================
# MAIN
# ============================================================

def main():
    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_DEPTH |
        GLUT_RGB
    )

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

    try:
        glutMouseWheelFunc(gMouseScroll)
    except Exception:
        pass

    if g_idle:
        glutIdleFunc(gSistemaOcioso)

    if g_timer:
        glutTimerFunc(g_timer_value, gTempoExecucao, 1)

    gInicializa()
    glutMainLoop()


if __name__ == "__main__":
    main()