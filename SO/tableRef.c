#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <limits.h>

typedef struct {
    int pid;
    int vsc;  
    int td;  
    int bt;  
    int p;    
} Processo;

void lerDados(int *quant, int *chg_em_zero,int *menor_chegada, int *maior_chegada,int *menor_bt,  int *maior_bt,int *menor_prty) {

    printf("\nQuantidade de Processos a simular: ");
    scanf("%d", quant);

    printf("Chegada em Zero (1-Sim): ");
    scanf("%d", chg_em_zero);

    while (1) {
        printf("Menor Chegada (> 0): ");
        scanf("%d", menor_chegada);
        if (*menor_chegada > 0) break;
        printf("  Valor deve ser > 0!\n");
    }

    while (1) {
        printf("Maior Chegada (>= %d): ", *menor_chegada);
        scanf("%d", maior_chegada);
        if (*maior_chegada >= *menor_chegada) break;
        printf("  Valor deve ser >= %d!\n", *menor_chegada);
    }

    while (1) {
        printf("Menor Burst Time (> 0): ");
        scanf("%d", menor_bt);
        if (*menor_bt > 0) break;
        printf("  Valor deve ser > 0!\n");
    }

    while (1) {
        printf("Maior Burst Time (>= %d): ", *menor_bt);
        scanf("%d", maior_bt);
        if (*maior_bt >= *menor_bt) break;
        printf("  Valor deve ser >= %d!\n", *menor_bt);
    }

    while (1) {
        printf("Menor Prioridade (> 0): ");
        scanf("%d", menor_prty);
        if (*menor_prty > 0) break;
        printf("  Valor deve ser > 0!\n");
    }
}

void gerarProcessos(int quant, int chg_em_zero,int menor_chegada, int maior_chegada,int menor_bt,  int maior_bt, int menor_prty, Processo vtr_processos[]) {
    int i;

    if (chg_em_zero == 1) {
        vtr_processos[0].vsc = 0;
        for (i = 1; i < quant; i++){
            vtr_processos[i].vsc = rand() % (maior_chegada - menor_chegada + 1) + menor_chegada;
        }
    } else {
        for (i = 0; i < quant; i++){
            vtr_processos[i].vsc = rand() % (maior_chegada - menor_chegada + 1) + menor_chegada;
        }
    }

    for (i = 0; i < quant; i++) {
        if (i == 0){
            vtr_processos[i].td = (chg_em_zero == 1) ? 0 : vtr_processos[i].vsc;
        }

        else {
            vtr_processos[i].td = vtr_processos[i].vsc + vtr_processos[i - 1].td;
        }
    }

    for (i = 0; i < quant; i++) {
        vtr_processos[i].pid = i + 1;
        vtr_processos[i].bt  = rand() % (maior_bt - menor_bt + 1) + menor_bt;
        vtr_processos[i].p   = rand() % menor_prty + 1;
    }
}

void imprimeTableRef(int quant, Processo vtr_processos[]) {
    int i;
    printf("\n%-5s | %-5s | %-5s | %-5s | %-5s\n",
           "PId", "VSC", "TD", "BT", "P");
    printf("------+-------+-------+-------+------\n");
    for (i = 0; i < quant; i++) {
        printf("%-5d | %-5d | %-5d | %-5d | %-5d\n",
               vtr_processos[i].pid, vtr_processos[i].vsc,
               vtr_processos[i].td,  vtr_processos[i].bt, vtr_processos[i].p);
    }
}

void simular(int quant, Processo vtr_processos[], int algoritmo) {

    const char *nomes[] = {"", "Tabela Referencia", "FIFO", "SJF", "PRTY", "LIFO"};

    int tc[quant];   
    int tf[quant];  
    int tsc[quant];  

    int cpu_pid[quant];
    int cpu_ti[quant]; 
    int cpu_tt[quant];
    int executado[quant];
    int exec_order[quant];  

    memset(executado, 0, quant * sizeof(int));

    int i;
    for (i = 0; i < quant; i++){
        tc[i] = vtr_processos[i].td;
    }

    int current_time = vtr_processos[0].td;
    int exec_count   = 0;

    while (exec_count < quant) {

        int chosen = -1;

        for (i = 0; i < quant; i++) {
            if (executado[i] || vtr_processos[i].td > current_time)
                continue;

            if (chosen == -1) {
                chosen = i;
                continue;
            }

            int pick = 0;
            switch (algoritmo) {
                case 2: 
                    pick = (vtr_processos[i].td < vtr_processos[chosen].td);
                    break;

                case 3: 
                    pick = (vtr_processos[i].bt < vtr_processos[chosen].bt) ||
                           (vtr_processos[i].bt == vtr_processos[chosen].bt &&
                            vtr_processos[i].td  < vtr_processos[chosen].td);
                    break;

                case 4: 
                    pick = (vtr_processos[i].p < vtr_processos[chosen].p) ||
                           (vtr_processos[i].p == vtr_processos[chosen].p &&
                            vtr_processos[i].td < vtr_processos[chosen].td);
                    break;

                case 5: 
                    pick = (vtr_processos[i].td > vtr_processos[chosen].td);
                    break;
            }
            if (pick) chosen = i;
        }

        if (chosen == -1) {
            int next_td = INT_MAX;
            for (i = 0; i < quant; i++)
                if (!executado[i] && vtr_processos[i].td < next_td)
                    next_td = vtr_processos[i].td;
            current_time = next_td;
            continue;
        }

        executado[chosen]          = 1;
        exec_order[exec_count]     = chosen;

        tf[chosen]                 = current_time;
        tsc[chosen]                = tf[chosen] - tc[chosen];

        cpu_pid[exec_count]        = vtr_processos[chosen].pid;
        cpu_ti[exec_count]         = current_time;
        cpu_tt[exec_count]         = current_time + vtr_processos[chosen].bt;
        current_time               = cpu_tt[exec_count];

        exec_count++;
    }

    printf("\n=== %s ===\n", nomes[algoritmo]);

    printf("\nFILA DE APTO\n");
    printf("%-5s | %-5s | %-5s | %-5s\n", "PId", "TC", "TF", "TSC");
    printf("------+-------+-------+------\n");
    for (i = 0; i < quant; i++) {
        int idx = exec_order[i];
        printf("%-5d | %-5d | %-5d | %-5d\n",
               vtr_processos[idx].pid, tc[idx], tf[idx], tsc[idx]);
    }

    printf("\nCPU\n");
    printf("%-5s | %-5s | %-5s\n", "PId", "TI", "TT");
    printf("------+-------+------\n");
    for (i = 0; i < quant; i++) {
        printf("%-5d | %-5d | %-5d\n",
               cpu_pid[i], cpu_ti[i], cpu_tt[i]);
    }
}

int main() {
    srand((unsigned)time(NULL));

    int quant, chg_em_zero;
    int menor_chegada, maior_chegada;
    int menor_bt,  maior_bt;
    int menor_prty;

    lerDados(&quant, &chg_em_zero,&menor_chegada,&maior_chegada,&menor_bt,&maior_bt,&menor_prty);

    Processo vtr_processos[quant];
    gerarProcessos(quant, chg_em_zero,menor_chegada,maior_chegada,menor_bt,maior_bt,menor_prty, vtr_processos);

    int opcao;
    do {
        printf("\nOpcoes => 1-Tabela Referencia 2-FIFO 3-SJF 4-PRTY 5-LIFO 0-Sair: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                imprimeTableRef(quant, vtr_processos);
                break;
            case 2:
            case 3:
            case 4:
            case 5:
                simular(quant, vtr_processos, opcao);
                break;
            case 0:
                printf("Encerrando...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);

    return 0;
}