# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

EPSILON = "epsilon"
EOF = "$"

TERMINAIS = {
    "LPAREN_CMD",
    "LPAREN_END",
    "LPAREN_ELSE",
    "LPAREN_ENDIF",
    "LPAREN_ENDWHILE",
    "RPAREN",
    "NUMBER",
    "MEMORY",
    "BOOL_LIT",        
    "OPERATOR",
    "REL_OP",
    "RES",
    "START",
    "END",
    "IF",
    "ELSE",
    "ENDIF",
    "WHILE",
    "ENDWHILE",
    EOF,
}

def construirGramatica():
    producoes = {
        "programa": [
            ["abre_start", "lista_prog", "fecha_end"],
        ],
        "abre_start": [
            ["LPAREN_CMD", "START", "RPAREN"],
        ],
        "fecha_end": [
            ["LPAREN_END", "END", "RPAREN"],
        ],

        "lista_prog": [
            ["comando", "lista_prog"],
            [EPSILON],
        ],
        "lista_if": [
            ["comando", "lista_if"],
            [EPSILON],
        ],
        "lista_while": [
            ["comando", "lista_while"],
            [EPSILON],
        ],

        "comando": [
            ["LPAREN_CMD", "interior"],
        ],

        "interior": [
            ["NUMBER",   "apos_num"],
            ["MEMORY",   "apos_mem"],
            ["BOOL_LIT", "apos_bool"],
            ["LPAREN_CMD", "sub", "apos_sub"],
        ],

        "apos_num": [
            ["RES", "RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN_CMD", "sub", "resto_sub"],
        ],
        
        "apos_mem": [
            ["RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN_CMD", "sub", "resto_sub"],
            ["IF", "RPAREN", "lista_if", "fim_if"],
            ["WHILE", "RPAREN", "lista_while", "abre_endwhile"],
        ],

        "apos_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN_CMD", "sub", "resto_sub"],
            ["IF", "RPAREN", "lista_if", "fim_if"],
            ["WHILE", "RPAREN", "lista_while", "abre_endwhile"],
        ],

        "apos_bool": [
            ["MEMORY", "RPAREN"],
            ["RPAREN"],
            ["LPAREN_CMD", "sub", "resto_sub"],
            ["IF", "RPAREN", "lista_if", "fim_if"],
            ["WHILE", "RPAREN", "lista_while", "abre_endwhile"],
        ],

        "apos_bool_sub": [
            ["MEMORY", "RPAREN"],
            ["RPAREN"],
            ["LPAREN_CMD", "sub", "resto_sub_sub"],
        ],
        
        "resto_num": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],
        "resto_mem_grava": [
            ["RPAREN"],
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],
        "resto_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],

        "cauda_rel": [
            ["RPAREN"],
            ["IF", "RPAREN", "lista_if", "fim_if"],
            ["WHILE", "RPAREN", "lista_while", "abre_endwhile"],
        ],

        "fim_if": [
            ["abre_else", "lista_if", "abre_endif"],
            ["abre_endif"],
        ],

        "abre_else": [
            ["LPAREN_ELSE", "ELSE", "RPAREN"],
        ],
        "abre_endif": [
            ["LPAREN_ENDIF", "ENDIF", "RPAREN"],
        ],
        "abre_endwhile": [
            ["LPAREN_ENDWHILE", "ENDWHILE", "RPAREN"],
        ],

        "sub": [
            ["NUMBER",   "apos_num_sub"],
            ["MEMORY",   "apos_mem_sub"],
            ["BOOL_LIT", "apos_bool_sub"],
            ["LPAREN_CMD", "sub", "apos_sub_sub"],
        ],

        "apos_num_sub": [
            ["RES", "RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN_CMD", "sub", "resto_sub_sub"],
        ],
        "apos_mem_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN_CMD", "sub", "resto_sub_sub"],
        ],
        "apos_sub_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN_CMD", "sub", "resto_sub_sub"],
        ],

        "resto_num_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
        "resto_mem_grava_sub": [
            ["RPAREN"],
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
        "resto_sub_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
    }

    nao_terminais = set(producoes.keys())
    first = calcularFirst(producoes, nao_terminais)
    follow = calcularFollow(producoes, nao_terminais, first, "programa")
    tabela, conflitos = construirTabelaLL1(
        producoes, nao_terminais, TERMINAIS, first, follow
    )


    return {
        "simbolo_inicial": "programa",
        "producoes": producoes,
        "nao_terminais": nao_terminais,
        "terminais": TERMINAIS,
        "first": first,
        "follow": follow,
        "tabela": tabela,
        "conflitos": conflitos,

    }

def calcularFirst(producoes, nao_terminais):
    first = {nt: set() for nt in nao_terminais}

    mudou = True
    while mudou:
        mudou = False
        for A, regras in producoes.items():
            for regra in regras:
                first_seq = calcularFirstDaSequencia(regra, first, nao_terminais)
                tamanho_antes = len(first[A])
                first[A].update(first_seq)
                if len(first[A]) != tamanho_antes:
                    mudou = True

    return first

def calcularFirstDaSequencia(sequencia, first, nao_terminais):
    if not sequencia:
        return {EPSILON}

    resultado = set()

    for simbolo in sequencia:
        if simbolo == EPSILON:
            resultado.add(EPSILON)
            return resultado

        if simbolo not in nao_terminais:
            resultado.add(simbolo)  
            return resultado

        resultado.update(first[simbolo] - {EPSILON})

        if EPSILON not in first[simbolo]:
            return resultado

    resultado.add(EPSILON)
    return resultado

def calcularFollow(producoes, nao_terminais, first, simbolo_inicial):
    follow = {nt: set() for nt in nao_terminais}
    follow[simbolo_inicial].add(EOF)

    mudou = True
    while mudou:
        mudou = False
        for A, regras in producoes.items():
            for regra in regras:
                for i, B in enumerate(regra):
                    if B not in nao_terminais:
                        continue

                    beta = regra[i + 1:]
                    first_beta = calcularFirstDaSequencia(beta, first, nao_terminais)

                    tamanho_antes = len(follow[B])
                    follow[B].update(first_beta - {EPSILON})

                    if EPSILON in first_beta or len(beta) == 0:
                        follow[B].update(follow[A])

                    if len(follow[B]) != tamanho_antes:
                        mudou = True

    return follow

def construirTabelaLL1(producoes, nao_terminais, terminais, first, follow):
    tabela = {nt: {} for nt in nao_terminais}
    conflitos = []

    for A, regras in producoes.items():
        for regra in regras:
            first_regra = calcularFirstDaSequencia(regra, first, nao_terminais)

            for terminal in first_regra - {EPSILON}:
                if terminal in tabela[A]:
                    conflitos.append((A, terminal, tabela[A][terminal], regra))
                else:
                    tabela[A][terminal] = regra

            if EPSILON in first_regra:
                for terminal in follow[A]:
                    if terminal in tabela[A]:
                        conflitos.append((A, terminal, tabela[A][terminal], regra))
                    else:
                        tabela[A][terminal] = regra

    return tabela, conflitos

def formatarRegra(A, regra):
    return f"{A} -> {' '.join(regra)}"

def exibirGramatica(gramatica):
    print("SIMBOLO INICIAL:")
    print(gramatica["simbolo_inicial"])
    print()

    print("PRODUCOES:")
    for A, regras in gramatica["producoes"].items():
        for regra in regras:
            print(formatarRegra(A, regra))
    print()

    print("FIRST:")
    for nt in sorted(gramatica["first"]):
        print(f"FIRST({nt}) = {sorted(gramatica['first'][nt])}")
    print()

    print("FOLLOW:")
    for nt in sorted(gramatica["follow"]):
        print(f"FOLLOW({nt}) = {sorted(gramatica['follow'][nt])}")
    print()

    print("TABELA LL(1):")
    for nt in sorted(gramatica["tabela"]):
        print(f"{nt}:")
        for terminal, regra in sorted(gramatica["tabela"][nt].items()):
            print(f"  {terminal} -> {' '.join(regra)}")
        print()

    if gramatica["conflitos"]:
        print("CONFLITOS:")
        for conflito in gramatica["conflitos"]:
            A, terminal, antiga, nova = conflito
            print(f"{A}, {terminal}: {antiga} X {nova}")
    else:
        print("SEM CONFLITOS LL(1)")