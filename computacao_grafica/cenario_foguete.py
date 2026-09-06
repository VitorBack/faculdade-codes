from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import random
import sys

# ============================================================
# CONFIGURACAO DA JANELA
# ============================================================
G_POSICAO_X = 50
G_POSICAO_Y = 50
G_LARGURA = 600
G_ALTURA = 600
G_TITULO = b"Computacao Grafica - Cenario do Foguete com Particulas"

# Sistema de particulas reescrito a partir do codigo C fornecido.
MAX_PARTICULAS = 150

# Posicao aproximada da saida da turbina do foguete.
TURBINA_X = 0.0
TURBINA_Y = -0.56


# ============================================================
# CLASSE DA PARTICULA
# Equivalente, em Python, a struct Particula do codigo em C.
# ============================================================
class Particula:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.r = 1.0
        self.g = 1.0
        self.b = 0.0
        self.a = 1.0
        self.vida = 1.0
        self.decaimento = 0.02
        self.tamanho = 0.02
        self.resetar()

    def resetar(self):
        """Inicializa/renasce a particula na saida da turbina."""
        # No C original as particulas nasciam ao redor do centro.
        # Aqui o centro foi deslocado para a turbina do foguete.
        self.x = TURBINA_X + random.uniform(-0.045, 0.045)
        self.y = TURBINA_Y - random.uniform(0.0, 0.02)

        # Pequena dispersao lateral.
        self.vx = random.uniform(-0.0045, 0.0045)

        # No codigo C o fogo subia (+Y). Como agora e a chama de
        # uma turbina de foguete, o jato deve sair para BAIXO (-Y).
        self.vy = -random.uniform(0.010, 0.022)

        # Amarelo/laranja brilhante.
        self.r = 1.0
        self.g = random.uniform(0.4, 1.0)
        self.b = 0.0
        self.a = 1.0

        self.vida = 1.0
        self.decaimento = random.uniform(0.015, 0.045)
        self.tamanho = random.uniform(0.018, 0.042)


fogo = []


# ============================================================
# PRIMITIVAS 2D
# ============================================================
def retangulo(x1, y1, x2, y2, cor):
    glColor3f(*cor)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def triangulo(p1, p2, p3, cor):
    glColor3f(*cor)
    glBegin(GL_TRIANGLES)
    glVertex2f(*p1)
    glVertex2f(*p2)
    glVertex2f(*p3)
    glEnd()


def circulo(cx, cy, raio, cor, segmentos=64):
    glColor3f(*cor)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segmentos + 1):
        angulo = 2.0 * math.pi * i / segmentos
        glVertex2f(
            cx + math.cos(angulo) * raio,
            cy + math.sin(angulo) * raio,
        )
    glEnd()


# ============================================================
# CENARIO DO PDF
# ============================================================
def desenhar_ceu_e_chao():
    # Fundo azul claro.
    retangulo(-1.0, -1.0, 1.0, 1.0, (0.50, 0.79, 0.90))

    # Chao verde na parte inferior.
    retangulo(-1.0, -1.0, 1.0, -0.55, (0.0, 0.62, 0.0))


def desenhar_sol():
    circulo(-0.70, 0.72, 0.15, (1.0, 1.0, 0.0))


def desenhar_arvore():
    # Tronco.
    retangulo(-0.61, -0.55, -0.53, -0.25, (0.55, 0.27, 0.07))

    # Copa em triangulos sobrepostos, como na imagem.
    triangulo((-0.72, -0.25), (-0.42, -0.25), (-0.57, 0.02), (0.0, 0.48, 0.08))
    triangulo((-0.70, -0.15), (-0.44, -0.15), (-0.57, 0.14), (0.0, 0.48, 0.08))
    triangulo((-0.66, -0.04), (-0.48, -0.04), (-0.57, 0.26), (0.0, 0.48, 0.08))


def desenhar_chama_base():
    """Chama amarela simples que ja existia na imagem de referencia."""
    triangulo(
        (-0.055, TURBINA_Y),
        (0.055, TURBINA_Y),
        (0.0, -0.79),
        (1.0, 1.0, 0.0),
    )


def desenhar_foguete():
    # Aletas azuis laterais.
    triangulo((-0.12, -0.55), (-0.27, -0.55), (-0.12, -0.08), (0.03, 0.05, 0.88))
    triangulo((0.12, -0.55), (0.27, -0.55), (0.12, -0.08), (0.03, 0.05, 0.88))

    # Corpo cinza.
    retangulo(-0.12, -0.55, 0.12, 0.49, (0.72, 0.72, 0.72))

    # Ponta vermelha.
    triangulo((-0.12, 0.49), (0.12, 0.49), (0.0, 0.78), (1.0, 0.0, 0.0))

    # Janelas azuis.
    circulo(0.0, 0.27, 0.073, (0.03, 0.50, 0.90), segmentos=48)
    circulo(0.0, -0.04, 0.073, (0.03, 0.50, 0.90), segmentos=48)

    # Pequena saida da turbina para deixar claro de onde o fogo nasce.
    retangulo(-0.055, -0.59, 0.055, -0.55, (0.20, 0.20, 0.20))


# ============================================================
# SISTEMA DE FOGO - TRADUCAO/ADAPTACAO DO C PARA PYTHON
# ============================================================
def inicializar_sistema_fogo():
    global fogo
    random.seed()
    fogo = [Particula() for _ in range(MAX_PARTICULAS)]

    # Assim como no C, distribui a vida inicial para nao parecer que
    # todas as particulas nasceram exatamente no mesmo instante.
    for particula in fogo:
        particula.vida = random.random()

    # Pequeno "aquecimento" para a chama ja aparecer espalhada no
    # primeiro quadro, sem mudar as regras do sistema.
    for _ in range(25):
        atualizar_fogo()


def desenhar_fogo_2d():
    # Blending aditivo: equivalente a glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    # usado no arquivo C para criar brilho nas particulas sobrepostas.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    for particula in fogo:
        if particula.vida > 0.0:
            glColor4f(
                particula.r,
                particula.g,
                particula.b,
                particula.vida,
            )

            metade = particula.tamanho / 2.0

            glBegin(GL_QUADS)
            glVertex2f(particula.x - metade, particula.y - metade)
            glVertex2f(particula.x + metade, particula.y - metade)
            glVertex2f(particula.x + metade, particula.y + metade)
            glVertex2f(particula.x - metade, particula.y + metade)
            glEnd()

    glDisable(GL_BLEND)


def atualizar_fogo():
    for particula in fogo:
        if particula.vida > 0.0:
            # Atualiza a posicao conforme a velocidade.
            particula.x += particula.vx
            particula.y += particula.vy

            # Perde vida/alpha.
            particula.vida -= particula.decaimento

            # Amarelo -> laranja -> vermelho.
            particula.g -= 0.02
            if particula.g < 0.0:
                particula.g = 0.0

            # Diminui conforme se afasta da turbina.
            particula.tamanho *= 0.98
        else:
            # Particula morta renasce na turbina.
            particula.resetar()


# ============================================================
# CALLBACKS GLUT
# ============================================================
def g_desenha():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Ordem de desenho: fundo -> elementos -> fogo -> foguete.
    desenhar_ceu_e_chao()
    desenhar_sol()
    desenhar_arvore()

    # Mantem a chama triangular da referencia e adiciona as particulas.
    desenhar_chama_base()
    desenhar_fogo_2d()

    # Foguete por ultimo para as particulas parecerem sair de tras da turbina.
    desenhar_foguete()

    glutSwapBuffers()


def g_redimensiona(largura, altura):
    if altura == 0:
        altura = 1

    glViewport(0, 0, largura, altura)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Mantem a area de desenho entre -1 e 1, preservando a proporcao.
    aspecto = largura / float(altura)
    if aspecto >= 1.0:
        glOrtho(-aspecto, aspecto, -1.0, 1.0, -1.0, 1.0)
    else:
        glOrtho(-1.0, 1.0, -1.0 / aspecto, 1.0 / aspecto, -1.0, 1.0)

    glMatrixMode(GL_MODELVIEW)


def g_teclado(tecla, x, y):
    if tecla == b"\x1b":  # ESC
        try:
            glutLeaveMainLoop()
        except Exception:
            sys.exit(0)


def g_timer(valor):
    atualizar_fogo()
    glutPostRedisplay()
    glutTimerFunc(16, g_timer, 1)  # aproximadamente 60 FPS


def g_inicializa():
    glClearColor(0.50, 0.79, 0.90, 1.0)
    glDisable(GL_DEPTH_TEST)
    inicializar_sistema_fogo()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

    glutInitWindowPosition(G_POSICAO_X, G_POSICAO_Y)
    glutInitWindowSize(G_LARGURA, G_ALTURA)
    glutCreateWindow(G_TITULO)

    glutDisplayFunc(g_desenha)
    glutReshapeFunc(g_redimensiona)
    glutKeyboardFunc(g_teclado)

    g_inicializa()
    glutTimerFunc(16, g_timer, 1)

    glutMainLoop()


if __name__ == "__main__":
    main()
