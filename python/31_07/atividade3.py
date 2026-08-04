x = [12, 7, 45, 3, 28, 91, 16, 54, 8, 33]

primeiros = x[0:3].copy()
ultimos = x[-3:].copy()
pares = x[::2]
impares = x[1::2]
invertido = x[::-1]
sempontas = x[1:-1]

print(primeiros)
print(ultimos)
print(pares)
print(impares)
print(invertido)
print(sempontas)