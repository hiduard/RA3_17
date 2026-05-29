# Integrantes do grupo (ordem alfabética):
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

PROMOCAO_LPAREN = {
    END: "LPAREN_END",
    ELSE: "LPAREN_ELSE",
    ENDIF: "LPAREN_ENDIF",
    ENDWHILE: "LPAREN_ENDWHILE",
}

def achatarTokens(tokens_por_linha):
    fluxo = []
    linhas = []
    fontes = {}

    for numero_linha, fonte, tokens in tokens_por_linha:
        fontes[numero_linha] = fonte
        for tok in tokens:
            fluxo.append(tok)
            linhas.append(numero_linha)

    return fluxo, linhas, fontes


def extrairErrosLexicos(fluxo, linhas, fontes):
    erros = []
    novo_fluxo = []
    novas_linhas = []

    for i, (tipo, valor) in enumerate(fluxo):
        if tipo == INVALID:
            linha = linhas[i]
            fonte = fontes.get(linha, "")
            erros.append(f"Linha {linha}: token lexico invalido '{valor}' em: {fonte}")
        else:
            novo_fluxo.append((tipo, valor))
            novas_linhas.append(linhas[i])

    return erros, novo_fluxo, novas_linhas


def promoverLParens(fluxo):
    promovido = []
    n = len(fluxo)

    for i in range(n):
        tipo, valor = fluxo[i]

        if tipo != LPAREN:
            promovido.append((tipo, valor))
            continue

        if i + 1 < n:
            proximo_tipo = fluxo[i + 1][0]
            classe = PROMOCAO_LPAREN.get(proximo_tipo, "LPAREN_CMD")
        else:
            classe = "LPAREN_CMD"

        promovido.append((classe, valor))

    return promovido


class ParserLL1:
    def __init__(self, fluxo_promovido, linhas, fontes, tabela):
        self.tokens = fluxo_promovido
        self.linhas = linhas     
        self.fontes = fontes      
        self.tabela = tabela
        self.i = 0
        self.derivacoes = []

    def lookahead(self):
        if self.i >= len(self.tokens):
            return "$"
        return self.tokens[self.i][0]

    def linhaAtual(self):
        if self.i >= len(self.linhas):
            return self.linhas[-1] if self.linhas else 0
        return self.linhas[self.i]

    def fonteAtual(self):
        return self.fontes.get(self.linhaAtual(), "")

    def erro(self, mensagem):
        linha = self.linhaAtual()
        fonte = self.fonteAtual()
        la = self.lookahead()
        raise ValueError(
            f"Erro sintatico na linha {linha} (lookahead={la}): {mensagem}"
            f" — trecho: {fonte}"
        )

    def consumir(self, esperado):
        if self.lookahead() != esperado:
            self.erro(f"esperava '{esperado}', encontrei '{self.lookahead()}'")
        valor = self.tokens[self.i][1]
        self.i += 1
        return valor

    def registrarDerivacao(self, nao_terminal, regra):
        self.derivacoes.append({
            "nao_terminal": nao_terminal,
            "lookahead": self.lookahead(),
            "regra": list(regra),
        })

    def escolherProducao(self, nao_terminal):
        la = self.lookahead()
        regra = self.tabela.get(nao_terminal, {}).get(la)
        if regra is None:
            self.erro(
                f"sem producao LL(1) para nao-terminal '{nao_terminal}' "
                f"com lookahead '{la}'"
            )
        self.registrarDerivacao(nao_terminal, regra)
        return regra

    def parse_programa(self):
        self.escolherProducao("programa")
        self.parse_abre_start()
        comandos = self.parse_lista("lista_prog")
        linha_fim = self.parse_fecha_end()
        linha_inicio = 1 if not self.linhas else self.linhas[0]
        return {
            "tipo": "programa",
            "linha_inicio": linha_inicio,
            "linha_fim": linha_fim,
            "comandos": comandos,
        }

    def parse_abre_start(self):
        self.escolherProducao("abre_start")
        self.consumir("LPAREN_CMD")
        self.consumir(START)
        self.consumir(RPAREN)

    def parse_fecha_end(self):
        self.escolherProducao("fecha_end")
        linha = self.linhaAtual()
        self.consumir("LPAREN_END")
        self.consumir(END)
        self.consumir(RPAREN)
        return linha

    def parse_lista(self, nome_nt):
        comandos = []
        while True:
            regra = self.escolherProducao(nome_nt)
            if regra == ["epsilon"]:
                return comandos
            comandos.append(self.parse_comando())

    def parse_comando(self):
        self.escolherProducao("comando")
        linha = self.linhaAtual()
        fonte = self.fonteAtual()
        self.consumir("LPAREN_CMD")
        no = self.parse_interior()
        if no["tipo"] in ("if", "while"):
            no["linha"] = linha
            no["fonte"] = fonte
            return no
        return {
            "tipo": "expressao",
            "linha": linha,
            "fonte": fonte,
            "estrutura": no,
        }

    def parse_interior(self):
        regra = self.escolherProducao("interior")
        if regra[0] == NUMBER:
            valor = self.consumir(NUMBER)
            return self.parse_apos_num({"tipo": "numero", "valor": valor})
        if regra[0] == MEMORY:
            nome = self.consumir(MEMORY)
            return self.parse_apos_mem(nome)
        if regra[0] == BOOL_LIT:
            valor = self.consumir(BOOL_LIT)
            return self.parse_apos_bool({"tipo": "bool_literal", "valor": valor})
        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            sub_expr = self.parse_sub()
            return self.parse_apos_sub(sub_expr)
        self.erro("interior: regra desconhecida")

    def parse_apos_num(self, no_num):
        regra = self.escolherProducao("apos_num")

        if regra[0] == RES:
            self.consumir(RES)
            self.consumir(RPAREN)
            return {"tipo": "carregar_resultado", "indice": no_num["valor"]}

        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num(no_num, no_b)

        if regra[0] == MEMORY:
            nome_mem = self.consumir(MEMORY)
            return self.parse_resto_mem_grava(no_num, nome_mem)

        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub = self.parse_sub()
            return self.parse_resto_sub(no_num, no_sub)

        self.erro("apos_num: regra desconhecida")

    def parse_apos_mem(self, nome_mem):
        regra = self.escolherProducao("apos_mem")

        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return {"tipo": "carregar_memoria", "nome": nome_mem}

        no_mem = {"tipo": "carregar_memoria", "nome": nome_mem}

        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num(no_mem, no_b)

        if regra[0] == MEMORY:
            nome2 = self.consumir(MEMORY)
            return self.parse_resto_mem_grava(no_mem, nome2)

        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub = self.parse_sub()
            return self.parse_resto_sub(no_mem, no_sub)
        
        if regra[0] == IF:
            self.consumir(IF)
            self.consumir(RPAREN)
            bloco_then = self.parse_lista("lista_if")
            fim = self.parse_fim_if()
            return {
                "tipo": "if",
                "condicao": no_mem,
                "bloco_then": bloco_then,
                "bloco_else": fim["bloco_else"],
            }

        if regra[0] == WHILE:
            self.consumir(WHILE)
            self.consumir(RPAREN)
            bloco = self.parse_lista("lista_while")
            self.parse_abre_endwhile()
            return {
                "tipo": "while",
                "condicao": no_mem,
                "bloco": bloco,
            }

        self.erro("apos_mem: regra desconhecida")

    def parse_apos_sub(self, no_sub):
        regra = self.escolherProducao("apos_sub")

        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return no_sub

        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num(no_sub, no_b)

        if regra[0] == MEMORY:
            nome2 = self.consumir(MEMORY)
            return self.parse_resto_mem_grava(no_sub, nome2)

        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub2 = self.parse_sub()
            return self.parse_resto_sub(no_sub, no_sub2)
        
        if regra[0] == IF:
            self.consumir(IF)
            self.consumir(RPAREN)
            bloco_then = self.parse_lista("lista_if")
            fim = self.parse_fim_if()
            return {
                "tipo": "if",
                "condicao": no_sub,
                "bloco_then": bloco_then,
                "bloco_else": fim["bloco_else"],
            }

        if regra[0] == WHILE:
            self.consumir(WHILE)
            self.consumir(RPAREN)
            bloco = self.parse_lista("lista_while")
            self.parse_abre_endwhile()
            return {
                "tipo": "while",
                "condicao": no_sub,
                "bloco": bloco,
            }

        self.erro("apos_sub: regra desconhecida")

    def parse_resto_num(self, esq, dir_):
        regra = self.escolherProducao("resto_num")
        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op, "esquerda": esq, "direita": dir_}
        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            return self.parse_cauda_rel(esq, dir_, op)
        self.erro("resto_num: regra desconhecida")

    def parse_resto_mem_grava(self, valor_ou_exp, nome_mem):
        regra = self.escolherProducao("resto_mem_grava")
        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return {"tipo": "gravar_memoria", "nome": nome_mem, "valor": valor_ou_exp}

        no_mem = {"tipo": "carregar_memoria", "nome": nome_mem}

        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op,
                    "esquerda": valor_ou_exp, "direita": no_mem}

        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            return self.parse_cauda_rel(valor_ou_exp, no_mem, op)

        self.erro("resto_mem_grava: regra desconhecida")

    def parse_resto_sub(self, esq, dir_):
        regra = self.escolherProducao("resto_sub")
        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op, "esquerda": esq, "direita": dir_}
        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            return self.parse_cauda_rel(esq, dir_, op)
        self.erro("resto_sub: regra desconhecida")

    def parse_cauda_rel(self, esq, dir_, op_rel):
        no_rel = {"tipo": "relacional", "operador": op_rel,
                  "esquerda": esq, "direita": dir_}

        regra = self.escolherProducao("cauda_rel")

        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return no_rel

        if regra[0] == IF:
            self.consumir(IF)
            self.consumir(RPAREN)
            bloco_then = self.parse_lista("lista_if")
            fim = self.parse_fim_if()
            return {
                "tipo": "if",
                "condicao": no_rel,
                "bloco_then": bloco_then,
                "bloco_else": fim["bloco_else"],
            }

        if regra[0] == WHILE:
            self.consumir(WHILE)
            self.consumir(RPAREN)
            bloco = self.parse_lista("lista_while")
            self.parse_abre_endwhile()
            return {
                "tipo": "while",
                "condicao": no_rel,
                "bloco": bloco,
            }

        self.erro("cauda_rel: regra desconhecida")

    def parse_fim_if(self):
        regra = self.escolherProducao("fim_if")
        if regra[0] == "abre_else":
            self.parse_abre_else()
            bloco_else = self.parse_lista("lista_if")
            self.parse_abre_endif()
            return {"bloco_else": bloco_else}
        if regra[0] == "abre_endif":
            self.parse_abre_endif()
            return {"bloco_else": None}
        self.erro("fim_if: regra desconhecida")

    def parse_abre_else(self):
        self.escolherProducao("abre_else")
        self.consumir("LPAREN_ELSE")
        self.consumir(ELSE)
        self.consumir(RPAREN)

    def parse_abre_endif(self):
        self.escolherProducao("abre_endif")
        self.consumir("LPAREN_ENDIF")
        self.consumir(ENDIF)
        self.consumir(RPAREN)

    def parse_abre_endwhile(self):
        self.escolherProducao("abre_endwhile")
        self.consumir("LPAREN_ENDWHILE")
        self.consumir(ENDWHILE)
        self.consumir(RPAREN)

    def parse_sub(self):
        regra = self.escolherProducao("sub")
        if regra[0] == NUMBER:
            valor = self.consumir(NUMBER)
            return self.parse_apos_num_sub({"tipo": "numero", "valor": valor})
        if regra[0] == MEMORY:
            nome = self.consumir(MEMORY)
            return self.parse_apos_mem_sub(nome)
        if regra[0] == BOOL_LIT:
            valor = self.consumir(BOOL_LIT)
            return self.parse_apos_bool_sub({"tipo": "bool_literal", "valor": valor})
        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub_interno = self.parse_sub()
            return self.parse_apos_sub_sub(no_sub_interno)
        self.erro("sub: regra desconhecida")

    def parse_apos_bool(self, no_bool):
        regra = self.escolherProducao("apos_bool")
        if regra[0] == MEMORY:
            nome = self.consumir(MEMORY)
            self.consumir(RPAREN)
            return {"tipo": "gravar_memoria", "nome": nome, "valor": no_bool}
        if regra[0] == "LPAREN_CMD":        
            self.consumir("LPAREN_CMD")
            no_sub = self.parse_sub()
            return self.parse_resto_sub(no_bool, no_sub)
        if regra[0] == IF:
            self.consumir(IF)
            self.consumir(RPAREN)
            bloco_then = self.parse_lista("lista_if")
            fim = self.parse_fim_if()
            return {
                "tipo": "if",
                "condicao": no_bool,
                "bloco_then": bloco_then,
                "bloco_else": fim["bloco_else"],
            }

        if regra[0] == WHILE:
            self.consumir(WHILE)
            self.consumir(RPAREN)
            bloco = self.parse_lista("lista_while")
            self.parse_abre_endwhile()
            return {
                "tipo": "while",
                "condicao": no_bool,
                "bloco": bloco,
            }
        self.consumir(RPAREN)
        return no_bool

    def parse_apos_bool_sub(self, no_bool):
        regra = self.escolherProducao("apos_bool_sub")

        if regra[0] == MEMORY:
            nome = self.consumir(MEMORY)
            self.consumir(RPAREN)
            return {
                "tipo": "gravar_memoria",
                "nome": nome,
                "valor": no_bool
            }

        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub = self.parse_sub()
            return self.parse_resto_sub_sub(no_bool, no_sub)

        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return no_bool

        self.erro("apos_bool_sub: regra desconhecida")

    def parse_apos_num_sub(self, no_num):
        regra = self.escolherProducao("apos_num_sub")
        if regra[0] == RES:
            self.consumir(RES)
            self.consumir(RPAREN)
            return {"tipo": "carregar_resultado", "indice": no_num["valor"]}
        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num_sub(no_num, no_b)
        if regra[0] == MEMORY:
            nome2 = self.consumir(MEMORY)
            return self.parse_resto_mem_grava_sub(no_num, nome2)
        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub_i = self.parse_sub()
            return self.parse_resto_sub_sub(no_num, no_sub_i)
        self.erro("apos_num_sub: regra desconhecida")

    def parse_apos_mem_sub(self, nome_mem):
        regra = self.escolherProducao("apos_mem_sub")
        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return {"tipo": "carregar_memoria", "nome": nome_mem}
        no_mem = {"tipo": "carregar_memoria", "nome": nome_mem}
        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num_sub(no_mem, no_b)
        if regra[0] == MEMORY:
            nome2 = self.consumir(MEMORY)
            return self.parse_resto_mem_grava_sub(no_mem, nome2)
        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub_i = self.parse_sub()
            return self.parse_resto_sub_sub(no_mem, no_sub_i)
        self.erro("apos_mem_sub: regra desconhecida")

    def parse_apos_sub_sub(self, no_sub):
        regra = self.escolherProducao("apos_sub_sub")
        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return no_sub
        if regra[0] == NUMBER:
            valor_b = self.consumir(NUMBER)
            no_b = {"tipo": "numero", "valor": valor_b}
            return self.parse_resto_num_sub(no_sub, no_b)
        if regra[0] == MEMORY:
            nome2 = self.consumir(MEMORY)
            return self.parse_resto_mem_grava_sub(no_sub, nome2)
        if regra[0] == "LPAREN_CMD":
            self.consumir("LPAREN_CMD")
            no_sub_i = self.parse_sub()
            return self.parse_resto_sub_sub(no_sub, no_sub_i)
        self.erro("apos_sub_sub: regra desconhecida")

    def parse_resto_num_sub(self, esq, dir_):
        regra = self.escolherProducao("resto_num_sub")
        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op, "esquerda": esq, "direita": dir_}
        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            self.consumir(RPAREN)
            return {"tipo": "relacional", "operador": op,
                    "esquerda": esq, "direita": dir_}
        self.erro("resto_num_sub: regra desconhecida")

    def parse_resto_mem_grava_sub(self, valor_ou_exp, nome_mem):
        regra = self.escolherProducao("resto_mem_grava_sub")
        if regra[0] == RPAREN:
            self.consumir(RPAREN)
            return {"tipo": "gravar_memoria", "nome": nome_mem, "valor": valor_ou_exp}
        no_mem = {"tipo": "carregar_memoria", "nome": nome_mem}
        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op,
                    "esquerda": valor_ou_exp, "direita": no_mem}
        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            self.consumir(RPAREN)
            return {"tipo": "relacional", "operador": op,
                    "esquerda": valor_ou_exp, "direita": no_mem}
        self.erro("resto_mem_grava_sub: regra desconhecida")

    def parse_resto_sub_sub(self, esq, dir_):
        regra = self.escolherProducao("resto_sub_sub")
        if regra[0] == OPERATOR:
            op = self.consumir(OPERATOR)
            self.consumir(RPAREN)
            return {"tipo": "binaria", "operador": op, "esquerda": esq, "direita": dir_}
        if regra[0] == REL_OP:
            op = self.consumir(REL_OP)
            self.consumir(RPAREN)
            return {"tipo": "relacional", "operador": op,
                    "esquerda": esq, "direita": dir_}
        self.erro("resto_sub_sub: regra desconhecida")


def parsear(tokens_por_linha, tabela_ll1):
    # 1. Achatamento
    fluxo, linhas, fontes = achatarTokens(tokens_por_linha)

    # 2. Filtragem de erros lexicos
    erros_lexicos, fluxo, linhas = extrairErrosLexicos(fluxo, linhas, fontes)
    if erros_lexicos:
        return {
            "aceito": False,
            "arvore": None,
            "derivacoes": [],
            "erro": None,
            "erros_lexicos": erros_lexicos,
        }

    # 3. Promocao de LPAREN
    fluxo_promovido = promoverLParens(fluxo)

    # 4. Parsing
    parser = ParserLL1(fluxo_promovido, linhas, fontes, tabela_ll1)
    try:
        arvore = parser.parse_programa()
        if parser.lookahead() != "$":
            parser.erro("sobraram tokens apos o (END)")
        return {
            "aceito": True,
            "arvore": arvore,
            "derivacoes": parser.derivacoes,
            "erro": None,
            "erros_lexicos": [],
        }
    except ValueError as e:
        return {
            "aceito": False,
            "arvore": None,
            "derivacoes": parser.derivacoes,
            "erro": str(e),
            "erros_lexicos": [],
        }
