from pathlib import Path

import numpy as np
from PIL import Image


# A matriz será sempre gravada ao lado deste programa.
ARQUIVO_MATRIZ = Path(__file__).with_name("matriz_imagem.npy")
ARQUIVO_TEXTO = Path(__file__).with_name("matriz_imagem.txt")


def gravar_matriz_em_txt(matriz):
    """Grava a matriz em texto para que seus pixels possam ser consultados."""
    altura, largura, canais = matriz.shape

    with ARQUIVO_TEXTO.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"Resolução: {largura} x {altura} pixels\n")
        arquivo.write(f"Canais: {canais} (R, G, B)\n\n")

        for linha in matriz:
            pixels = (f"[{vermelho}, {verde}, {azul}]" for vermelho, verde, azul in linha)
            arquivo.write(" ".join(pixels) + "\n")


def salvar_e_exibir_matriz(matriz):
    """Atualiza os arquivos da matriz e mostra a imagem resultante."""
    try:
        np.save(ARQUIVO_MATRIZ, matriz)
        gravar_matriz_em_txt(matriz)
        imagem = Image.fromarray(matriz)
        imagem.show()

        print(f"Resolução: {imagem.width} x {imagem.height} pixels")
        print(f"Matriz gravada em: {ARQUIVO_MATRIZ}")
        print(f"Matriz em texto gravada em: {ARQUIVO_TEXTO}")
    except (ValueError, TypeError, OSError) as erro:
        print(f"Não foi possível salvar ou exibir a imagem: {erro}")


def ler_imagem_e_gravar_matriz():
    caminho = input("Informe o caminho da imagem: ").strip().strip('"')
    arquivo_imagem = Path(caminho)

    if not arquivo_imagem.is_file():
        print("Imagem não encontrada.")
        return

    try:
        with Image.open(arquivo_imagem) as imagem_original:
            # RGB evita que imagens em paleta sejam salvas apenas como índices de cor.
            imagem = imagem_original.convert("RGB")

        matriz = np.array(imagem)
    except OSError:
        print("Não foi possível abrir esse arquivo como imagem.")
        return

    salvar_e_exibir_matriz(matriz)


def carregar_matriz():
    """Lê a matriz RGB gravada para visualizar ou manipular seus pixels."""
    if not ARQUIVO_MATRIZ.is_file():
        print("Nenhuma matriz foi gravada ainda. Escolha primeiro a opção 1.")
        return None

    try:
        matriz = np.load(ARQUIVO_MATRIZ, allow_pickle=False)
        if matriz.ndim != 3 or matriz.shape[2] != 3 or matriz.size == 0:
            raise ValueError("A matriz deve representar uma imagem RGB não vazia.")
        if matriz.dtype != np.uint8:
            raise ValueError("Os pixels devem usar valores do tipo uint8.")
        return matriz
    except (ValueError, TypeError, OSError) as erro:
        print(f"Não foi possível ler a matriz gravada: {erro}")
        return None


def ler_matriz_e_visualizar_imagem():
    """Lê a matriz gravada anteriormente e exibe a imagem reconstruída."""
    matriz = carregar_matriz()
    if matriz is None:
        return

    try:
        imagem = Image.fromarray(matriz)
        imagem.show()
        print("Imagem reconstruída e exibida com sucesso.")
    except (ValueError, TypeError, OSError):
        print("Não foi possível reconstruir a imagem a partir da matriz gravada.")


def rotacionar_imagem(sentido):
    matriz = carregar_matriz()
    if matriz is None:
        return

    # Cada passo de rot90 gira 90 graus; o valor negativo gira à direita.
    passos = -1 if sentido == "direita" else 1
    matriz_rotacionada = np.rot90(matriz, k=passos)
    salvar_e_exibir_matriz(matriz_rotacionada)


def espelhar_imagem(sentido):
    matriz = carregar_matriz()
    if matriz is None:
        return

    if sentido == "vertical":
        matriz_espelhada = np.flipud(matriz)  # Troca cima e baixo.
    else:
        matriz_espelhada = np.fliplr(matriz)  # Troca esquerda e direita.

    salvar_e_exibir_matriz(matriz_espelhada)


def recortar_imagem():
    matriz = carregar_matriz()
    if matriz is None:
        return

    altura, largura = matriz.shape[:2]
    print(f"Linhas: 0 a {altura - 1}; colunas: 0 a {largura - 1}.")
    print("A linha e a coluna finais também serão incluídas no recorte.")

    try:
        linha_inicial = int(input("Linha inicial: "))
        coluna_inicial = int(input("Coluna inicial: "))
        linha_final = int(input("Linha final: "))
        coluna_final = int(input("Coluna final: "))
    except ValueError:
        print("Informe apenas números inteiros para as linhas e colunas.")
        return

    if not (0 <= linha_inicial <= linha_final < altura
            and 0 <= coluna_inicial <= coluna_final < largura):
        print("Recorte inválido. Respeite os limites e informe o início antes ou igual ao fim.")
        return

    matriz_recortada = matriz[
        linha_inicial:linha_final + 1,
        coluna_inicial:coluna_final + 1
    ]
    salvar_e_exibir_matriz(matriz_recortada)


def main():
    while True:
        print("\n--- Processamento de Imagens ---")
        print("1 - Ler e visualizar uma imagem; gravar sua matriz")
        print("2 - Ler a matriz gravada e visualizar a imagem")
        print("3 - Rotacionar 90° à direita")
        print("4 - Rotacionar 90° à esquerda")
        print("5 - Espelhar verticalmente (cima/baixo)")
        print("6 - Espelhar horizontalmente (esquerda/direita)")
        print("7 - Recortar imagem")
        print("0 - Sair")
        print("As alterações atualizam a matriz gravada em NPY e TXT.")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            ler_imagem_e_gravar_matriz()
        elif opcao == "2":
            ler_matriz_e_visualizar_imagem()
        elif opcao == "3":
            rotacionar_imagem("direita")
        elif opcao == "4":
            rotacionar_imagem("esquerda")
        elif opcao == "5":
            espelhar_imagem("vertical")
        elif opcao == "6":
            espelhar_imagem("horizontal")
        elif opcao == "7":
            recortar_imagem()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
