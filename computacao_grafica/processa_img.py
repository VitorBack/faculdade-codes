from pathlib import Path

import numpy as np
from PIL import Image


# A matriz será sempre gravada ao lado deste programa.
ARQUIVO_MATRIZ = Path(__file__).with_name("matriz_imagem.npy")


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

        imagem.show()
        matriz = np.array(imagem)
        np.save(ARQUIVO_MATRIZ, matriz)

        print("Imagem exibida com sucesso.")
        print(f"Resolução: {imagem.width} x {imagem.height} pixels")
        print(f"Matriz gravada em: {ARQUIVO_MATRIZ}")
    except OSError:
        print("Não foi possível abrir esse arquivo como imagem.")


def ler_matriz_e_visualizar_imagem():
    """Lê a matriz gravada anteriormente e exibe a imagem reconstruída."""
    if not ARQUIVO_MATRIZ.is_file():
        print("Nenhuma matriz foi gravada ainda. Escolha primeiro a opção 1.")
        return

    try:
        matriz = np.load(ARQUIVO_MATRIZ, allow_pickle=False)
        imagem = Image.fromarray(matriz)
        imagem.show()
        print("Imagem reconstruída e exibida com sucesso.")
    except (ValueError, TypeError, OSError):
        print("Não foi possível reconstruir a imagem a partir da matriz gravada.")


def main():
    while True:
        print("\n--- Processamento de Imagens ---")
        print("1 - Ler e visualizar uma imagem; gravar sua matriz")
        print("2 - Ler a matriz gravada e visualizar a imagem")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            ler_imagem_e_gravar_matriz()
        elif opcao == "2":
            ler_matriz_e_visualizar_imagem()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
