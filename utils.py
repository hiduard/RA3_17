# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 8


def lerTokens(caminho_arquivo):
    resultado = []
    numero_linha = None
    linha_original = ""
    tokens = []

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha:
                if numero_linha is not None:
                    resultado.append((numero_linha, linha_original, tokens))
                    numero_linha = None
                    linha_original = ""
                    tokens = []
                continue

            if linha.startswith("Linha "):
                partes = linha.split(":", 1)
                numero_linha = int(partes[0].replace("Linha", "").strip())
                linha_original = partes[1].strip()
            else:
                conteudo = linha.strip()[1:-1]
                tipo, valor = conteudo.split(",", 1)
                tokens.append((tipo.strip(), valor.strip()))

    if numero_linha is not None:
        resultado.append((numero_linha, linha_original, tokens))

    return resultado


def salvarTokens(resultado_por_linha, caminho_saida):
    import os
    pasta = os.path.dirname(caminho_saida)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        for numero_linha, linha_original, tokens in resultado_por_linha:
            arquivo.write(f"Linha {numero_linha}: {linha_original}\n")
            for tipo, valor in tokens:
                arquivo.write(f"({tipo}, {valor})\n")
            arquivo.write("\n")