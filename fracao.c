#include <stdio.h>

int main() {
    int num1;
    int den1;
    int num2;
    int den2;
    int resto1;
    int resto2;
    int quociente1;
    int quociente2;
    float resultado1;
    float resultado2;
    int novo_num;
    int novo_den;
    int quociente_final;

    printf("Numerador da primeira fracao: ");
    scanf("%d",&num1);
    printf("\n Denominador da primeira fracao: ");
    scanf("%d",&den1);
    printf("\n Numerador da segunda fracao: ");
    scanf("%d",&num2);
    printf("\n Denominador da segunda fracao: ");
    scanf("%d",&den2);

    printf("\nDividendo da fracao 1: %d", num1);
    printf("\nDivisor da fracao 1: %d", den1);
    printf("\nDividendo da fracao 2: %d", num2);
    printf("\nDivisor da fracao 2: %d", den2);

    resto1 = num1 % den1;
    resto2 = num2 % den2;

    printf("\nResto da divisao da fracao 1: %d", resto1);
    printf("\nResto da divisao da fracao 2: %d", resto2);

    quociente1 = num1 / den1;
    quociente2 = num2 / den2;

    printf("\nQuociente da divisao da fracao 1: %d", quociente1);
    printf("\nQuociente da divisao da fracao 2: %d", quociente2);

    resultado1 = (float) num1 / den1;
    resultado2 = (float) num2 / den2;

    printf("\nResultado da divisao da fracao 1: %.2f", resultado1);
    printf("\nResultado da divisao da fracao 2: %.2f", resultado2);

    novo_num = num1 * den2;
    novo_den = den1 * num2;
    quociente_final = novo_num / novo_den;

    printf("\nResultado da divisao da fracao 1 pela fracao 2: %d", quociente_final);

    if(resultado1 > resultado2){
        printf("\nNumerador da primeira fracao: %d", num1);
        printf("\nDenominador da primeira fracao: %d", den1);
        printf("\nResultado da primeira fracao eh maior: %.2f", resultado1);
    }else if(resultado2 > resultado1){
        printf("\nNumerador da segunda fracao: %d", num2);
        printf("\nDenominador da segunda fracao: %d", den2);
        printf("\nResultado da segunda fracao eh maior: %.2f", resultado2);
    }else{
        printf("\nResultados com o mesmo valor: %.2f", resultado1);
    }
    return 0;
}

