# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17

from tokens import (
    LPAREN,
    RPAREN,
    NUMBER,
    MEMORY,
    OPERATOR,
    REL_OP,
    RES,
    START,
    END,
    IF,
    ELSE,
    ENDIF,
    WHILE,
    ENDWHILE,
    BOOL_LIT,
    INVALID,
)

KEYWORDS = {
    "RES": RES,
    "START": START,
    "END": END,
    "IF": IF,
    "ELSE": ELSE,
    "ENDIF": ENDIF,
    "WHILE": WHILE,
    "ENDWHILE": ENDWHILE,
    "TRUE": BOOL_LIT,
    "FALSE": BOOL_LIT,
}


def eh_digito(c):
    return "0" <= c <= "9"


def eh_letra_maiuscula(c):
    return "A" <= c <= "Z"


def adicionarToken(tokens, tipo, valor):
    tokens.append((tipo, valor))


def estadoNumero(linha, i, tokens):
    inicio = i
    tem_ponto = False
    digitos_antes = 0
    digitos_depois = 0

    while i < len(linha):
        c = linha[i]

        if eh_digito(c):
            if tem_ponto:
                digitos_depois += 1
            else:
                digitos_antes += 1
            i += 1

        elif c == ".":
            if tem_ponto:
                while i < len(linha) and linha[i] not in " ()\t":
                    i += 1
                adicionarToken(tokens, INVALID, linha[inicio:i])
                return i

            tem_ponto = True
            i += 1

        else:
            break

    lexema = linha[inicio:i]

    if tem_ponto:
        if digitos_antes == 0 or digitos_depois == 0:
            adicionarToken(tokens, INVALID, lexema)
        else:
            adicionarToken(tokens, NUMBER, lexema)
    else:
        if digitos_antes == 0:
            adicionarToken(tokens, INVALID, lexema)
        else:
            adicionarToken(tokens, NUMBER, lexema)

    return i


def estadoPalavra(linha, i, tokens):
    inicio = i

    if not eh_letra_maiuscula(linha[i]):
        adicionarToken(tokens, INVALID, linha[i])
        return i + 1

    i += 1

    while i < len(linha) and eh_letra_maiuscula(linha[i]):
        i += 1

    lexema = linha[inicio:i]

    if lexema in KEYWORDS:
        adicionarToken(tokens, KEYWORDS[lexema], lexema)
    else:
        adicionarToken(tokens, MEMORY, lexema)

    return i


def estadoBarra(linha, i, tokens):
    if i + 1 < len(linha) and linha[i + 1] == "/":
        adicionarToken(tokens, INVALID, "//")
        return i + 2

    adicionarToken(tokens, OPERATOR, "/")
    return i + 1


def estadoPipe(linha, i, tokens):
    adicionarToken(tokens, OPERATOR, "|")
    return i + 1


def estadoOperador(linha, i, tokens):
    adicionarToken(tokens, OPERATOR, linha[i])
    return i + 1


def estadoRelacional(linha, i, tokens):
    c = linha[i]

    if c == "=":
        if i + 1 < len(linha) and linha[i + 1] == "=":
            adicionarToken(tokens, REL_OP, "==")
            return i + 2
        adicionarToken(tokens, INVALID, "=")
        return i + 1

    if c == "!":
        if i + 1 < len(linha) and linha[i + 1] == "=":
            adicionarToken(tokens, REL_OP, "!=")
            return i + 2
        adicionarToken(tokens, INVALID, "!")
        return i + 1

    if c == "<":
        if i + 1 < len(linha) and linha[i + 1] == "=":
            adicionarToken(tokens, REL_OP, "<=")
            return i + 2
        adicionarToken(tokens, REL_OP, "<")
        return i + 1

    if c == ">":
        if i + 1 < len(linha) and linha[i + 1] == "=":
            adicionarToken(tokens, REL_OP, ">=")
            return i + 2
        adicionarToken(tokens, REL_OP, ">")
        return i + 1

    adicionarToken(tokens, INVALID, c)
    return i + 1


def estadoParenteses(linha, i, tokens):
    if linha[i] == "(":
        adicionarToken(tokens, LPAREN, "(")
    else:
        adicionarToken(tokens, RPAREN, ")")
    return i + 1


def estadoComentario(linha, i, tokens):
    # Ao entrar aqui, linha[i] == '*' e linha[i+1] == '{'.
    # Comentarios sao consumidos e descartados (nao geram token).
    # Se nao encontrar '}*' ate o fim da linha, marca como invalido.
    i += 2  # consome '*{'

    while i < len(linha):
        if linha[i] == "}" and i + 1 < len(linha) and linha[i + 1] == "*":
            return i + 2  # consome '}*' e segue
        i += 1

    # Nao fechou na mesma linha: erro lexico
    adicionarToken(tokens, INVALID, "COMENTARIO_NAO_FECHADO")
    return i


def estadoInvalido(linha, i, tokens):
    inicio = i

    while i < len(linha) and linha[i] not in " ()\t":
        i += 1

    adicionarToken(tokens, INVALID, linha[inicio:i])
    return i

def estadoInicial(linha, i, tokens):
    c = linha[i]

    if c in " \t":
        return i + 1

    if c == "(" or c == ")":
        return estadoParenteses(linha, i, tokens)

    if eh_digito(c):
        return estadoNumero(linha, i, tokens)

    if eh_letra_maiuscula(c):
        return estadoPalavra(linha, i, tokens)

    if c == "/":
        return estadoBarra(linha, i, tokens)

    if c == "|":
        return estadoPipe(linha, i, tokens)

    if c == "*" and i + 1 < len(linha) and linha[i + 1] == "{":
        return estadoComentario(linha, i, tokens)

    if c in "+-*%^":
        return estadoOperador(linha, i, tokens)

    if c in "<>!=":
        return estadoRelacional(linha, i, tokens)
    
    return estadoInvalido(linha, i, tokens)


def validarParenteses(tokens):
    saldo = 0

    for tipo, valor in tokens:
        if tipo == LPAREN:
            saldo += 1
        elif tipo == RPAREN:
            saldo -= 1

        if saldo < 0:
            return False

    return saldo == 0


def parseExpressao(linha):
    tokens = []
    i = 0

    while i < len(linha):
        i = estadoInicial(linha, i, tokens)

    if not validarParenteses(tokens):
        adicionarToken(tokens, INVALID, "PARENTESES_DESBALANCEADOS")

    return tokens