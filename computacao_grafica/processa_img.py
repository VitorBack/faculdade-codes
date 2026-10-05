from pathlib import Path

import numpy as np
from PIL import Image


# A matriz será sempre gravada ao lado deste programa.
ARQUIVO_MATRIZ = Path(__file__).with_name("matriz_imagem.npy")
ARQUIVO_TEXTO = Path(__file__).with_name("matriz_imagem.txt")
ARQUIVO_MEDIANA = Path(__file__).with_name("imagem_mediana.png")


def gravar_matriz_em_txt(matriz):
    """Grava a matriz em texto para que seus pixels possam ser consultados."""
    altura, largura, canais = matriz.shape

    with ARQUIVO_TEXTO.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"Resolução: {largura} x {altura} pixels\n")
        arquivo.write(f"Canais: {canais} (R, G, B)\n\n")

        for linha in matriz:
            pixels = (f"[{vermelho}, {verde}, {azul}]" for vermelho, verde, azul in linha)
            arquivo.write(" ".join(pixels) + "\n")


def salvar_e_exibir_matriz(matriz, arquivo_imagem=None):
    """Atualiza a matriz, exibe o resultado e, se solicitado, salva a imagem."""
    try:
        imagem = Image.fromarray(matriz)
        if arquivo_imagem is not None:
            imagem.save(arquivo_imagem)

        np.save(ARQUIVO_MATRIZ, matriz)
        gravar_matriz_em_txt(matriz)
        imagem.show()

        print(f"Resolução: {imagem.width} x {imagem.height} pixels")
        print(f"Matriz gravada em: {ARQUIVO_MATRIZ}")
        print(f"Matriz em texto gravada em: {ARQUIVO_TEXTO}")
        if arquivo_imagem is not None:
            print(f"Imagem gravada em: {arquivo_imagem}")
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

    altura, largura, canais = matriz.shape
    # A rotação troca a altura pela largura. zeros apenas cria a matriz vazia.
    matriz_rotacionada = np.zeros((largura, altura, canais), dtype=matriz.dtype)

    for linha in range(altura):
        for coluna in range(largura):
            if sentido == "direita":
                nova_linha = coluna
                nova_coluna = altura - 1 - linha
            else:
                nova_linha = largura - 1 - coluna
                nova_coluna = linha

            # Copia o pixel RGB para a posição calculada.
            matriz_rotacionada[nova_linha, nova_coluna] = matriz[linha, coluna]

    salvar_e_exibir_matriz(matriz_rotacionada)


def espelhar_imagem(sentido):
    matriz = carregar_matriz()
    if matriz is None:
        return

    altura, largura, canais = matriz.shape
    matriz_espelhada = np.zeros((altura, largura, canais), dtype=matriz.dtype)

    for linha in range(altura):
        for coluna in range(largura):
            if sentido == "vertical":
                # A primeira linha vai para a última, a segunda para a penúltima...
                nova_linha = altura - 1 - linha
                nova_coluna = coluna
            else:
                # A primeira coluna vai para a última, a segunda para a penúltima...
                nova_linha = linha
                nova_coluna = largura - 1 - coluna

            matriz_espelhada[nova_linha, nova_coluna] = matriz[linha, coluna]

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


def aplicar_mediana():
    """Aplica a mediana por canal RGB com o tamanho de máscara escolhido."""
    matriz = carregar_matriz()
    if matriz is None:
        return

    tamanhos_permitidos = (3, 5, 7, 9, 15, 21)
    print("Máscaras disponíveis: " + ", ".join(
        f"{tamanho}x{tamanho}" for tamanho in tamanhos_permitidos
    ))
    try:
        tamanho = int(input("Informe o tamanho da máscara (3, 5, 7, 9, 15 ou 21): "))
    except ValueError:
        print("Informe um número inteiro para o tamanho da máscara.")
        return

    if tamanho not in tamanhos_permitidos:
        print("Tamanho inválido. Escolha um dos tamanhos disponíveis.")
        return

    altura, largura = matriz.shape[:2]
    raio = tamanho // 2
    # Repete os pixels das bordas para completar as janelas em toda a imagem.
    matriz_com_borda = np.pad(matriz, ((raio, raio), (raio, raio), (0, 0)), mode="edge")
    matriz_mediana = np.empty_like(matriz)

    for linha in range(altura):
        for coluna in range(largura):
            janela = matriz_com_borda[
                linha:linha + tamanho, coluna:coluna + tamanho
            ]
            # Lê sempre a imagem de entrada, sem reutilizar pixels já filtrados.
            matriz_mediana[linha, coluna] = np.median(janela, axis=(0, 1))

    salvar_e_exibir_matriz(matriz_mediana, ARQUIVO_MEDIANA)


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
        print("8 - Aplicar filtro de mediana (escolher tamanho da máscara)")
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
        elif opcao == "8":
            aplicar_mediana()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
