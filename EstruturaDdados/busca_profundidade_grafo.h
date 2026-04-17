#include <stdio.h>
#include <stdlib.h>

#define BP_MAX 100
int matriz[BP_MAX][BP_MAX];
int bp_visitado[BP_MAX];
int bp_caminho[BP_MAX];
int bp_n, bp_i;

void bp_inicializa(int t){
	for(bp_i=0;bp_i<t;bp_i++){
	bp_visitado[bp_i] = 0;
	bp_i=0;
	}
}

void bp_mostra_caminho(int t){
	int i;
	for(bp_i=0;i<t;bp_i++){
		printf("%d ",bp_caminho[bp_i]);
		printf("\n");
	}
}

void busca_profundidade_grafo(int origem,int destino,int posicao,int n){
	
	
	bp_visitado[origem] = 1;
	bp_caminho [posicao] = origem;
	
	if(posicao == destino)//chegou ao destino
	  { 
 	   bp_mostra_caminho(posicao+1);
		}
 	else{
 		for(bp_i = 0;bp_i<n;bp_i ++)
		 {
 			if(matriz[origem][bp_i]==1 && !bp_visitado[bp_i]){//se existe Aresta e não foi visitado
 			busca_profundidade_grafo(bp_i,destino,posicao+1,n);
 			}
		 }
	 }
	 bp_visitado[origem] = 0;
}

void bp_inicializa(int t){
    for(bp_i=0;bp_i<t;bp_i++){
    bp_visitado[bp_i] = 0;
    bp_i=0;
    }
}