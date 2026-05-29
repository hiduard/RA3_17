# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17


def lerArquivo(nomeArquivo):
    with open(nomeArquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Pre-processa comentarios *{ ... }* antes de fatiar em linhas.
    # Preserva quebras de linha para manter a numeracao correta.
    chars_limpos = []
    i = 0
    dentro_comentario = False
    linha_abertura = 1
    linha_atual = 1

    while i < len(conteudo):
        if not dentro_comentario:
            if conteudo[i] == '*' and i + 1 < len(conteudo) and conteudo[i+1] == '{':
                dentro_comentario = True
                linha_abertura = linha_atual
                i += 2
            else:
                if conteudo[i] == '\n':
                    linha_atual += 1
                chars_limpos.append(conteudo[i])
                i += 1
        else:
            if conteudo[i] == '}' and i + 1 < len(conteudo) and conteudo[i+1] == '*':
                dentro_comentario = False
                i += 2
            else:
                if conteudo[i] == '\n':
                    linha_atual += 1
                    chars_limpos.append('\n')  # preserva numeracao
                i += 1

    if dentro_comentario:
        return [(linha_abertura, "ERRO_COMENTARIO_NAO_FECHADO")]

    resultado = []
    for numero, linha in enumerate("".join(chars_limpos).splitlines(), start=1):
        conteudo_linha = linha.strip()
        if conteudo_linha:
            resultado.append((numero, conteudo_linha))
    return resultado