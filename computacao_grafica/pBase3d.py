"""Projeto Base 3D, convertido de C para Python com PyOpenGL e freeglut."""

import sys

from OpenGL import GL, GLU, platform


# PyOpenGL 3.1 procura nomes específicos de DLL no Windows.
if sys.platform == "win32" and platform.PLATFORM.GLUT is None:
    from ctypes import WinDLL
    from pathlib import Path

    dll_local = Path(__file__).resolve().with_name("freeglut.dll")
    nome_dll = str(dll_local) if dll_local.is_file() else "freeglut.dll"
    try:
        platform.PLATFORM.GLUT = WinDLL(nome_dll)
    except OSError:
        pass

from OpenGL import GLUT


TAM_JANELA = 10.0


class ProjetoBase3D:
    def __init__(self):
        self.obs_x = 0.0
        self.obs_y = 0.0
        self.obs_z = -4 * TAM_JANELA
        self.rotacao_x = 20.0
        self.rotacao_y = 25.0
        self.operacao = None
        self.inicio_arrasto = None

    def posiciona_observador(self):
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslatef(self.obs_x, self.obs_y, self.obs_z)
        GL.glRotatef(self.rotacao_x, 1, 0, 0)
        GL.glRotatef(self.rotacao_y, 0, 1, 0)

    @staticmethod
    def desenha_plano_3d():
        tamanho = TAM_JANELA

        # Eixos X, Y e Z.
        GL.glColor3f(1, 0, 0)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(-tamanho, 0, 0)
        GL.glVertex3f(tamanho, 0, 0)
        GL.glVertex3f(0, -tamanho, 0)
        GL.glVertex3f(0, tamanho, 0)
        GL.glVertex3f(0, 0, -tamanho)
        GL.glVertex3f(0, 0, tamanho)
        GL.glEnd()

        # O plano translúcido deixa visíveis os objetos em arame abaixo dele.
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glColor4f(0, 1, 1, 0.25)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3f(-tamanho, 0, -tamanho)
        GL.glVertex3f(-tamanho, 0, tamanho)
        GL.glVertex3f(tamanho, 0, tamanho)
        GL.glVertex3f(tamanho, 0, -tamanho)
        GL.glEnd()
        GL.glDisable(GL.GL_BLEND)
        GL.glColor3f(1, 1, 1)

    @staticmethod
    def desenha_objetos():
        distancia = TAM_JANELA / 2
        altura = TAM_JANELA / 2
        altura_cone = 2.8

        # Um objeto em cada quadrante XZ, com a mesma cor e tamanho nos dois níveis.
        objetos = (
            (
                distancia, distancia, (0.12, 0.32, 0.9),
                GLUT.glutSolidSphere, GLUT.glutWireSphere, (1.45, 20, 12),
            ),
            (
                -distancia, distancia, (0.85, 0.18, 0.13),
                GLUT.glutSolidCube, GLUT.glutWireCube, (2.3,),
            ),
            (
                -distancia, -distancia, (0.85, 0.43, 0.06),
                GLUT.glutSolidCone, GLUT.glutWireCone, (1.35, altura_cone, 20, 8),
            ),
            (
                distancia, -distancia, (0.55, 0.22, 0.75),
                GLUT.glutSolidTorus, GLUT.glutWireTorus, (0.42, 1.18, 12, 24),
            ),
        )

        for y, solido in ((altura, True), (-altura, False)):
            if solido:
                GL.glEnable(GL.GL_LIGHTING)
            else:
                GL.glDisable(GL.GL_LIGHTING)

            for x, z, cor, desenha_solido, desenha_arame, parametros in objetos:
                GL.glPushMatrix()
                GL.glTranslatef(x, y, z)
                if desenha_solido is GLUT.glutSolidCone:
                    # Centraliza o cone e alinha sua ponta com o eixo Y.
                    GL.glTranslatef(0, -altura_cone / 2, 0)
                    GL.glRotatef(-90, 1, 0, 0)
                GL.glColor3f(*cor)
                desenha = desenha_solido if solido else desenha_arame
                desenha(*parametros)
                GL.glPopMatrix()

    def desenha(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.posiciona_observador()
        self.desenha_objetos()
        self.desenha_plano_3d()
        GLUT.glutSwapBuffers()

    @staticmethod
    def redimensiona(largura, altura):
        largura = max(1, largura)
        altura = max(1, altura)

        GL.glViewport(0, 0, largura, altura)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45, largura / altura, TAM_JANELA / 10, 8 * TAM_JANELA)

    def teclado(self, tecla, _x, _y):
        if tecla == b"\x1b":  # Esc
            GLUT.glutLeaveMainLoop()
            return

        self.operacao = tecla if tecla in (b"r", b"t", b"a") else None

    @staticmethod
    def teclas_especiais(_tecla, _x, _y):
        GLUT.glutPostRedisplay()

    def mouse(self, botao, estado, x, y):
        if botao == GLUT.GLUT_LEFT_BUTTON:
            if estado == GLUT.GLUT_DOWN:
                self.inicio_arrasto = (
                    x, y, self.obs_x, self.obs_y, self.rotacao_x, self.rotacao_y
                )
            else:
                self.inicio_arrasto = None

    def arrasta_mouse(self, x, y):
        if self.inicio_arrasto is None:
            return

        mouse_x, mouse_y, obs_x, obs_y, rotacao_x, rotacao_y = self.inicio_arrasto
        delta_x = (x - mouse_x) / 3
        delta_y = (y - mouse_y) / 3

        if self.operacao == b"r":
            self.rotacao_x = rotacao_x - delta_y
            self.rotacao_y = rotacao_y - delta_x
        elif self.operacao == b"t":
            self.obs_x = obs_x + delta_x
            self.obs_y = obs_y + delta_y
        else:
            return

        GLUT.glutPostRedisplay()

    def roda_mouse(self, _roda, direcao, _x, _y):
        if self.operacao == b"a":
            self.obs_z += (TAM_JANELA / 10) * direcao
            GLUT.glutPostRedisplay()


def main():
    if not GLUT.glutLeaveMainLoop:
        raise SystemExit("Instale o freeglut para abrir a janela 3D.")

    GLUT.glutInit(sys.argv)
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH | GLUT.GLUT_RGB)
    GLUT.glutInitWindowPosition(50, 50)
    GLUT.glutInitWindowSize(500, 500)
    GLUT.glutCreateWindow(b"Projeto Base 3D")
    GLUT.glutSetOption(
        GLUT.GLUT_ACTION_ON_WINDOW_CLOSE, GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS
    )

    GL.glClearColor(1, 1, 1, 0)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glEnable(GL.GL_COLOR_MATERIAL)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, (-0.4, 0.7, 1, 0))

    projeto = ProjetoBase3D()
    GLUT.glutDisplayFunc(projeto.desenha)
    GLUT.glutReshapeFunc(projeto.redimensiona)
    GLUT.glutKeyboardFunc(projeto.teclado)
    GLUT.glutSpecialFunc(projeto.teclas_especiais)
    GLUT.glutMouseFunc(projeto.mouse)
    GLUT.glutMotionFunc(projeto.arrasta_mouse)
    GLUT.glutMouseWheelFunc(projeto.roda_mouse)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()
