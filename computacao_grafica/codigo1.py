from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

title = "3D Shapes"


def initGL():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    # ==========================
    # Cubo
    # ==========================
    glLoadIdentity()
    glTranslatef(1.5, 0.0, -7.0)

    glBegin(GL_QUADS)

    # Topo
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)

    # Base
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Frente
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Trás
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)

    # Esquerda
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)

    # Direita
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    glEnd()

    # ==========================
    # Pirâmide
    # ==========================
    glLoadIdentity()
    glTranslatef(-1.5, 0.0, -6.0)

    glBegin(GL_TRIANGLES)

    # Frente
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Direita
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Trás
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    # Esquerda
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)

    glEnd()

    glutSwapBuffers()


def reshape(width, height):
    if height == 0:
        height = 1

    aspect = width / height

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, aspect, 0.1, 100.0)


def main():
    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(640, 480)
    glutInitWindowPosition(50, 50)

    glutCreateWindow(title.encode("utf-8"))

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    initGL()

    glutMainLoop()


if __name__ == "__main__":
    main()