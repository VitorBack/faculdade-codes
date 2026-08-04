notas = [8.5, 4.0, 6.2, 9.1, 2.7]

for aluno, nota in enumerate(notas):
    if(nota >= 7):
        print(f"Aluno {aluno}: Aprovado")
    elif (nota <= 5):
        print(f"Aluno {aluno}: Reprovado")
    else:
        print(f"Aluno {aluno}: Exame")
