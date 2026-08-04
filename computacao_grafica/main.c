#include <math.h>
#include <GL/glut.h>
#include <stdlib.h>

int g_posicao_x = 50;
int g_posicao_y = 50;
int g_largura = 500;
int g_altura = 500;
char g_titulo[] = "Projeto Base";
int g_idle = 0, g_timer = 0, g_timer_value = 1;


void gDesenha (void) {;}
void gRedimensiona (GLsizei largura, GLsizei altura) {;}
void gTeclado (unsigned char tecla, int x, int y) {;}
void gEspeciais (int tecla, int x, int y) {;}
void gMouse (int botao, int estado, int x, int y) {;}
void gMousePressionado (int x, int y) {;}
void gMouseLiberado (int x, int y) {;}
void gMouseScroll (int botao, int direcao, int x, int y) {;}
void gSistemaOcioso (void) {;}
void gTempoExecucao (void) {;}

void ginicializa (void) {;}

    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    glutSwapBuffers ();
}
int main (int argc, char *argv[]) {
	
	glutInit (&argc, argv); // Inicialização da GLUT
	glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB);

	glutInitWindowPosition (g_posicao_x, g_posicao_y);
	glutInitWindowSize (g_largura, g_altura);
	glutCreateWindow (g_titulo);

	glutDisplayFunc (gDesenha);
	glutReshapeFunc (gRedimensiona);
	glutKeyboardFunc (gTeclado);
	glutSpecialFunc (gEspeciais);
	glutMouseFunc (gMouse);
	glutMotionFunc (gMousePressionado);
	glutPassiveMotionFunc (gMouseLiberado);
	glutMouseWheelFunc (gMouseScroll);
	
	if (g_idle) glutIdleFunc (gSistemaOcioso);
	if (g_timer) glutTimerFunc (g_timer_value, gTempoExecucao, 1);
	
	gInicializa ();
	glutMainLoop ();
	
	system ("pause");
	return 0;
}