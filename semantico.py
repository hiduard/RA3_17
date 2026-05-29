# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

# =============================================================================
# semantico.py
# Fase 3 - Analisador Semantico
#
# Responsabilidades:
#   - construirTabelaSimbolos(arvore): percorre a arvore e registra variaveis,
#     tipos inferidos, linha de definicao e linha de ultimo uso.
#   - verificarTipos(arvore, tabela): valida tipos usando regras do calculo
#     de sequentes definidas neste modulo.
#
# Tipos suportados: "int", "real", "bool"
#
# Regras de inferencia (calculo de sequentes):
#
#   AXIOMAS:
#     NUMBER (sem ponto decimal) : int
#     NUMBER (com ponto decimal) : real
#     BOOL_LIT ("TRUE")  : bool
#     BOOL_LIT ("FALSE") : bool
#
#   OPERADORES ARITMETICOS (+ - * | ^):
#     E1 : real   E2 : real
#     ─────────────────────   op in {+, -, *, |}
#     E1 op E2 : real
#
#     E1 : int   E2 : int
#     ────────────────────   op in {+, -, *}
#     E1 op E2 : int
#
#     E1 : int   E2 : int
#     ────────────────────   op in {/, %}
#     E1 op E2 : int
#
#     E1 : real   E2 : int
#     ─────────────────────   op == ^
#     E1 ^ E2 : real
#
#     E1 : int   E2 : int
#     ─────────────────────   op == ^
#     E1 ^ E2 : int
#
#   OPERADORES RELACIONAIS (> < >= <= == !=):
#     E1 : T   E2 : T     T in {int, real}
#     ──────────────────────────────────────
#     E1 rop E2 : bool
#
#   CONDICIONAL:
#     E1 : bool   E2 : T   E3 : T
#     ─────────────────────────────
#     if E1 then E2 else E3 : T
#
#   LACO:
#     E1 : bool
#     ──────────
#     while E1 do bloco : ok
#
#   GRAVAR MEMORIA:
#     E : T
#     ──────────────────
#     (E MEM) : T        (define MEM com tipo T)
#
#   CARREGAR MEMORIA:
#     MEM : T   (declarada no contexto)
#     ────────────────────────────────
#     (MEM) : T
#
# =============================================================================

import json
import os


# ---------------------------------------------------------------------------
# Helpers de tipo
# ---------------------------------------------------------------------------

def _eh_real(valor_str):
    """Retorna True se o literal numerico e real (contem ponto)."""
    return "." in valor_str


def _tipo_literal(valor_str):
    """Infere o tipo de um literal numerico."""
    if _eh_real(valor_str):
        return "real"
    return "int"


def _tipos_compativeis(t1, t2):
    """
    Verifica se dois tipos sao compativeis para operacoes aritmeticas/relacionais.
    int e real sao compativeis entre si (promovem para real).
    """
    numericos = {"int", "real"}
    if t1 in numericos and t2 in numericos:
        return True
    return t1 == t2


def _promover(t1, t2):
    """
    Retorna o tipo resultante da promocao entre dois tipos numericos.
    int + real -> real; int + int -> int; real + real -> real.
    """
    if t1 == "real" or t2 == "real":
        return "real"
    return "int"


# ---------------------------------------------------------------------------
# construirTabelaSimbolos
# ---------------------------------------------------------------------------

def construirTabelaSimbolos(arvore):
    """
    Percorre a arvore sintatica e constroi a tabela de simbolos.

    Retorna um dict:
      {
        "NOME_VAR": {
          "tipo": "int" | "real" | "bool" | "desconhecido",
          "linha_definicao": int,
          "linha_ultimo_uso": int,
        },
        ...
      }

    A inferencia de tipo e feita de forma simples nesta etapa:
    - gravar_memoria: o tipo e inferido do valor atribuido (se for literal).
    - carregar_memoria: registra uso.
    - Tipos complexos (expressoes) ficam como "desconhecido" nesta etapa;
      verificarTipos() vai resolver o tipo correto depois.
    """
    tabela = {}

    def _inferir_tipo_simples(no):
        """Infere tipo apenas para literais e carregamentos simples."""
        tipo_no = no["tipo"]
        if tipo_no == "numero":
            return _tipo_literal(no["valor"])
        if tipo_no == "bool_literal":
            return "bool"
        if tipo_no == "carregar_memoria":
            entrada = tabela.get(no["nome"])
            if entrada:
                return entrada["tipo"]
        if tipo_no == "relacional":
            return "bool"
        if tipo_no == "binaria":
            op = no.get("operador", "")
            t_esq = _inferir_tipo_simples(no["esquerda"])
            t_dir = _inferir_tipo_simples(no["direita"])
            if op == "|":
                return "real"
            if op in ("/", "%"):
                return "int"
            if op == "^":
                return t_esq if t_esq != "desconhecido" else "real"
            return _promover(t_esq, t_dir)
        return "desconhecido"

    def _registrar_definicao(nome, tipo, linha):
        if nome not in tabela:
            tabela[nome] = {
                "tipo": tipo,
                "linha_definicao": linha,
                "linha_ultimo_uso": linha,
            }
        else:
            # Redefinicao: atualiza tipo se o anterior era desconhecido
            if tabela[nome]["tipo"] == "desconhecido" and tipo != "desconhecido":
                tabela[nome]["tipo"] = tipo
            tabela[nome]["linha_ultimo_uso"] = linha
            
    def _registrar_uso(nome, linha):
        if nome in tabela:
            tabela[nome]["linha_ultimo_uso"] = linha

    def _visitar_expressao(no, linha):
        tipo_no = no["tipo"]

        if tipo_no == "numero":
            return

        if tipo_no == "carregar_memoria":
            _registrar_uso(no["nome"], linha)
            return

        if tipo_no == "carregar_resultado":
            return

        if tipo_no == "gravar_memoria":
            _visitar_expressao(no["valor"], linha)
            tipo_inferido = _inferir_tipo_simples(no["valor"])
            _registrar_definicao(no["nome"], tipo_inferido, linha)
            return

        if tipo_no in ("binaria", "relacional"):
            _visitar_expressao(no["esquerda"], linha)
            _visitar_expressao(no["direita"], linha)
            return

    def _visitar_comando(cmd):
        tipo_cmd = cmd["tipo"]

        if tipo_cmd == "expressao":
            _visitar_expressao(cmd["estrutura"], cmd["linha"])
            return

        if tipo_cmd == "if":
            _visitar_expressao(cmd["condicao"], cmd.get("linha", 0))
            for item in cmd["bloco_then"]:
                _visitar_comando(item)
            if cmd["bloco_else"] is not None:
                for item in cmd["bloco_else"]:
                    _visitar_comando(item)
            return

        if tipo_cmd == "while":
            _visitar_expressao(cmd["condicao"], cmd.get("linha", 0))
            for item in cmd["bloco"]:
                _visitar_comando(item)
            return

    for cmd in arvore["comandos"]:
        _visitar_comando(cmd)

    return tabela


# ---------------------------------------------------------------------------
# verificarTipos
# ---------------------------------------------------------------------------

def verificarTipos(arvore, tabela_simbolos):
    """
    Percorre a arvore e verifica os tipos de todas as expressoes usando
    as regras do calculo de sequentes documentadas neste modulo.

    Retorna um dict:
      {
        "valido": True | False,
        "erros": [ "mensagem de erro", ... ],
        "arvore_atribuida": arvore com campo "tipo_inferido" em cada no,
      }

    A arvore_atribuida e uma copia profunda da arvore original com o campo
    "tipo_inferido" adicionado a cada no de expressao.
    """
    import copy
    erros = []
    arvore_atribuida = copy.deepcopy(arvore)

    # Contexto de tipos das variaveis (sincronizado com tabela_simbolos)
    contexto = {}

    # Resultados ja produzidos por comandos de expressao.
    # Chave: linha do comando; valor: tipo inferido do resultado.
    tipos_resultado_por_linha = {}
    historico_resultados = []

    def _erro(msg, linha):
        erros.append(f"Linha {linha}: {msg}")

    def _tipar_expressao(no, linha):
        """
        Aplica as regras de sequentes ao no e retorna o tipo inferido.
        Tambem adiciona o campo "tipo_inferido" ao no (in-place).
        """
        tipo_no = no["tipo"]

        # --- AXIOMA: literal numerico ---
        if tipo_no == "numero":
            t = _tipo_literal(no["valor"])
            no["tipo_inferido"] = t
            return t
        
        if tipo_no == "bool_literal":
            no["tipo_inferido"] = "bool"
            return "bool"
        
        # --- AXIOMA: carregar memoria ---
        if tipo_no == "carregar_memoria":
            nome = no["nome"]
            if nome not in contexto:
                _erro(
                    f"variavel '{nome}' usada antes de ser definida",
                    linha,
                )
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"
            t = contexto[nome]
            no["tipo_inferido"] = t
            return t

        # --- carregar resultado (N RES) ---
        if tipo_no == "carregar_resultado":
            try:
                indice = int(no["indice"])
            except (ValueError, TypeError):
                _erro(f"RES exige indice inteiro, recebeu '{no['indice']}'", linha)
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"

            if indice <= 0:
                _erro(f"RES {indice} invalido: deve referenciar resultado anterior", linha)
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"

            linha_destino = linha - indice

            if linha_destino in tipos_resultado_por_linha:
                t = tipos_resultado_por_linha[linha_destino]
                no["linha_resultado"] = linha_destino
                no["tipo_inferido"] = t
                return t

            if indice <= len(historico_resultados):
                linha_destino, t = historico_resultados[-indice]
                no["linha_resultado"] = linha_destino
                no["tipo_inferido"] = t
                return t

            _erro(
                f"RES {indice} invalido: nao existe resultado anterior suficiente",
                linha,
            )
            no["tipo_inferido"] = "desconhecido"
            return "desconhecido"

        # --- gravar memoria ---
        if tipo_no == "gravar_memoria":
            nome = no["nome"]
            t_val = _tipar_expressao(no["valor"], linha)
            no["tipo_inferido"] = t_val

            if nome in contexto and contexto[nome] != "desconhecido":
                t_anterior = contexto[nome]

                if t_val == "desconhecido":
                    _erro(
                        f"variavel '{nome}' recebe valor de tipo desconhecido",
                        linha,
                    )
                elif t_anterior != t_val:
                    _erro(
                        f"variavel '{nome}' foi definida como {t_anterior} "
                        f"mas recebe valor do tipo {t_val}",
                        linha,
                    )
            else:
                contexto[nome] = t_val
                if nome in tabela_simbolos:
                    tabela_simbolos[nome]["tipo"] = t_val

            return t_val

        # --- operacao binaria aritmetica ---
        if tipo_no == "binaria":
            op = no["operador"]
            t_esq = _tipar_expressao(no["esquerda"], linha)
            t_dir = _tipar_expressao(no["direita"], linha)

            # NOVO: se um operando já é desconhecido, o erro raiz (ex: variável
            # não definida) já foi reportado. Propaga sem emitir erro derivado.
            if t_esq == "desconhecido" or t_dir == "desconhecido":
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"
            
            # Divisao inteira e resto: exigem int em ambos os lados
            if op in ("/", "%"):
                if t_esq != "int":
                    _erro(
                        f"operador '{op}' exige int no operando esquerdo, "
                        f"recebeu {t_esq}",
                        linha,
                    )
                if t_dir != "int":
                    _erro(
                        f"operador '{op}' exige int no operando direito, "
                        f"recebeu {t_dir}",
                        linha,
                    )
                no["tipo_inferido"] = "int"
                return "int"

            # Potenciacao: base qualquer numerica, expoente int
            if op == "^":
                if t_esq == "bool":
                    _erro(
                        f"operador '^' nao aceita bool como base",
                        linha,
                    )
                if t_dir != "int":
                    _erro(
                        f"operador '^' exige int como expoente, recebeu {t_dir}",
                        linha,
                    )
                t_res = t_esq if t_esq != "desconhecido" else "real"
                no["tipo_inferido"] = t_res
                return t_res

            # Divisao real: aceita operandos numericos e sempre retorna real
            if op == "|":
                if t_esq == "bool" or t_dir == "bool":
                    _erro(
                        f"operador '|' nao aceita operandos do tipo bool",
                        linha,
                    )
                    no["tipo_inferido"] = "desconhecido"
                    return "desconhecido"

                no["tipo_inferido"] = "real"
                return "real"

            # Demais operadores aritmeticos: + - *
            if t_esq == "bool" or t_dir == "bool":
                _erro(
                    f"operador '{op}' nao aceita operandos do tipo bool",
                    linha,
                )
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"

            if not _tipos_compativeis(t_esq, t_dir):
                _erro(
                    f"tipos incompativeis para operador '{op}': "
                    f"{t_esq} e {t_dir}",
                    linha,
                )
                no["tipo_inferido"] = "desconhecido"
                return "desconhecido"

            t_res = _promover(t_esq, t_dir)
            no["tipo_inferido"] = t_res
            return t_res

        # --- operacao relacional ---
        if tipo_no == "relacional":
            op = no["operador"]
            t_esq = _tipar_expressao(no["esquerda"], linha)
            t_dir = _tipar_expressao(no["direita"], linha)

            # NOVO: propaga desconhecido sem erro derivado
            if t_esq == "desconhecido" or t_dir == "desconhecido":
                no["tipo_inferido"] = "bool"
                return "bool"

            if t_esq == "bool" or t_dir == "bool":
                _erro(
                    f"operador relacional '{op}' nao aceita operandos bool",
                    linha,
                )
            elif not _tipos_compativeis(t_esq, t_dir):
                _erro(
                    f"tipos incompativeis para operador relacional '{op}': "
                    f"{t_esq} e {t_dir}",
                    linha,
                )

            no["tipo_inferido"] = "bool"
            return "bool"

        # Tipo desconhecido (nao deveria chegar aqui)
        no["tipo_inferido"] = "desconhecido"
        return "desconhecido"

    def _verificar_comando(cmd):
        tipo_cmd = cmd["tipo"]

        if tipo_cmd == "expressao":
            t = _tipar_expressao(cmd["estrutura"], cmd["linha"])

            if t != "desconhecido":
                tipos_resultado_por_linha[cmd["linha"]] = t
                historico_resultados.append((cmd["linha"], t))

            return

        if tipo_cmd == "if":
            linha = cmd.get("linha", 0)
            t_cond = _tipar_expressao(cmd["condicao"], linha)
            if t_cond != "bool":
                _erro(
                    f"condicao do IF deve ser bool, recebeu {t_cond}",
                    linha,
                )
            for item in cmd["bloco_then"]:
                _verificar_comando(item)
            if cmd["bloco_else"] is not None:
                for item in cmd["bloco_else"]:
                    _verificar_comando(item)
            return

        if tipo_cmd == "while":
            linha = cmd.get("linha", 0)
            t_cond = _tipar_expressao(cmd["condicao"], linha)
            if t_cond != "bool":
                _erro(
                    f"condicao do WHILE deve ser bool, recebeu {t_cond}",
                    linha,
                )
            for item in cmd["bloco"]:
                _verificar_comando(item)
            return

    for cmd in arvore_atribuida["comandos"]:
        _verificar_comando(cmd)

    return {
        "valido": len(erros) == 0,
        "erros": erros,
        "arvore_atribuida": arvore_atribuida,
    }


# ---------------------------------------------------------------------------
# Salvar artefatos da Fase 3
# ---------------------------------------------------------------------------

def salvarTabelaSimbolos(tabela, caminho):
    """Salva a tabela de simbolos em JSON."""
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(tabela, f, indent=2, ensure_ascii=False)


def salvarRelatorioErrosSemanticos(erros, caminho):
    """Salva o relatorio de erros semanticos em texto."""
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        if erros:
            f.write(f"Erros semanticos encontrados: {len(erros)}\n\n")
            for e in erros:
                f.write(f"  {e}\n")
        else:
            f.write("Nenhum erro semantico encontrado.\n")


def _arvore_atribuida_para_texto(arvore_atribuida):
    """Renderiza a arvore atribuida em texto, com o tipo inferido [tipo] em cada no."""
    linhas = []

    def _no(no, prefixo=""):
        tipo = no["tipo"]
        if tipo == "programa":
            linhas.append(f"{prefixo}programa [{no['linha_inicio']}..{no['linha_fim']}]")
            for cmd in no["comandos"]:
                _no(cmd, prefixo + "  ")
        elif tipo == "expressao":
            linhas.append(f"{prefixo}expressao [linha {no['linha']}]")
            _expr(no["estrutura"], prefixo + "  ")
        elif tipo == "if":
            linhas.append(f"{prefixo}if [linha {no.get('linha', '?')}]")
            linhas.append(f"{prefixo}  condicao:")
            _expr(no["condicao"], prefixo + "    ")
            linhas.append(f"{prefixo}  then:")
            for item in no["bloco_then"]:
                _no(item, prefixo + "    ")
            if no["bloco_else"] is not None:
                linhas.append(f"{prefixo}  else:")
                for item in no["bloco_else"]:
                    _no(item, prefixo + "    ")
        elif tipo == "while":
            linhas.append(f"{prefixo}while [linha {no.get('linha', '?')}]")
            linhas.append(f"{prefixo}  condicao:")
            _expr(no["condicao"], prefixo + "    ")
            linhas.append(f"{prefixo}  bloco:")
            for item in no["bloco"]:
                _no(item, prefixo + "    ")
        else:
            linhas.append(f"{prefixo}{tipo}")

    def _expr(no, prefixo):
        tipo = no["tipo"]
        tipo_inf = no.get("tipo_inferido", "")
        sufixo = f"  [{tipo_inf}]" if tipo_inf else ""
        if tipo == "numero":
            linhas.append(f"{prefixo}numero({no['valor']}){sufixo}")
        elif tipo == "carregar_memoria":
            linhas.append(f"{prefixo}memoria({no['nome']}){sufixo}")
        elif tipo == "carregar_resultado":
            linhas.append(f"{prefixo}res({no['indice']}){sufixo}")
        elif tipo == "gravar_memoria":
            linhas.append(f"{prefixo}gravar_memoria({no['nome']}){sufixo}")
            _expr(no["valor"], prefixo + "  ")
        elif tipo == "binaria":
            linhas.append(f"{prefixo}binaria({no['operador']}){sufixo}")
            _expr(no["esquerda"], prefixo + "  ")
            _expr(no["direita"], prefixo + "  ")
        elif tipo == "relacional":
            linhas.append(f"{prefixo}relacional({no['operador']}){sufixo}")
            _expr(no["esquerda"], prefixo + "  ")
            _expr(no["direita"], prefixo + "  ")
        else:
            linhas.append(f"{prefixo}{tipo}{sufixo}")

    _no(arvore_atribuida)
    return "\n".join(linhas)


def salvarArvoreAtribuida(arvore_atribuida, caminho_json, caminho_txt):
    """Salva a arvore atribuida em JSON e em texto (com tipos)."""
    from arvore import noParaDict

    os.makedirs(os.path.dirname(caminho_json) or ".", exist_ok=True)
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(noParaDict(arvore_atribuida), f, indent=2, ensure_ascii=False)

    os.makedirs(os.path.dirname(caminho_txt) or ".", exist_ok=True)
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(_arvore_atribuida_para_texto(arvore_atribuida))   # <- mudou aqui


def salvarRegrasSequentes(caminho):
    """
    Salva o sistema de regras de tipos em calculo de sequentes
    em formato Markdown, conforme exigido pela Fase 3.
    """
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)

    linhas = [
        "# Sistema de Regras de Tipos — Calculo de Sequentes",
        "",
        "Este documento descreve as regras semanticas usadas pelo analisador semantico da Fase 3.",
        "",
        "A linguagem utiliza tipagem estatica e forte. O tipo de uma variavel e inferido na primeira definicao e nao pode ser alterado posteriormente.",
        "",
        "A promocao `int -> real` e permitida em expressoes aritmeticas compativeis, mas nao e permitida para redefinir o tipo de uma variavel ja registrada na tabela de simbolos.",
        "",
        "## Julgamentos de Tipo",
        "",
        "Um julgamento de tipo tem a forma:",
        "",
        "```",
        "G |- e : T",
        "```",
        "",
        "onde:",
        "",
        "- `G` e o contexto semantico, isto e, a tabela de simbolos;",
        "- `e` e uma expressao ou comando;",
        "- `T` e o tipo inferido ou verificado;",
        "- `T` pertence a {int, real, bool}.",
        "",
        "## Axiomas",
        "",
        "```",
        "────────────────────────────────────────────────",
        "NUMBER sem ponto decimal : int",
        "",
        "────────────────────────────────────────────────",
        "NUMBER com ponto decimal : real",
        "",
        "────────────────────────────────────────────────",
        'BOOL_LIT(\"TRUE\") : bool',
        "",
        "────────────────────────────────────────────────",
        'BOOL_LIT(\"FALSE\") : bool',
        "```",
        "",
        "> Literais booleanos sao reconhecidos pelo lexico como tokens `BOOL_LIT`, com valores `TRUE` ou `FALSE`.",
        "",
        "## Operadores Aritmeticos",
        "",
        "### Soma, Subtracao e Multiplicacao",
        "",
        "```",
        "G |- E1 : int",
        "G |- E2 : int",
        "op pertence a {+, -, *}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 op) : int",
        "",
        "G |- E1 : real",
        "G |- E2 : real",
        "op pertence a {+, -, *}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 op) : real",
        "",
        "G |- E1 : int",
        "G |- E2 : real",
        "op pertence a {+, -, *}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 op) : real",
        "",
        "G |- E1 : real",
        "G |- E2 : int",
        "op pertence a {+, -, *}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 op) : real",
        "```",
        "",
        "### Divisao Real",
        "",
        "```",
        "G |- E1 : T1",
        "G |- E2 : T2",
        "T1 pertence a {int, real}",
        "T2 pertence a {int, real}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 |) : real",
        "```",
        "",
        "### Divisao Inteira e Resto",
        "",
        "```",
        "G |- E1 : int",
        "G |- E2 : int",
        "op pertence a {/, %}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 op) : int",
        "",
        "G |- E1 : T1",
        "G |- E2 : T2",
        "op pertence a {/, %}",
        "T1 != int ou T2 != int",
        "────────────────────────────────────────────────",
        "erro_semantico: operador exige operandos inteiros",
        "```",
        "",
        "### Potenciacao",
        "",
        "```",
        "G |- E1 : int",
        "G |- E2 : int",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 ^) : int",
        "",
        "G |- E1 : real",
        "G |- E2 : int",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 ^) : real",
        "",
        "G |- E1 : T1",
        "G |- E2 : T2",
        "T2 != int",
        "────────────────────────────────────────────────",
        "erro_semantico: operador ^ exige expoente inteiro",
        "```",
        "",
        "> Operacoes entre `int` e `real` podem promover o resultado para `real` dentro da expressao. Essa promocao nao altera o tipo previamente registrado de uma variavel.",
        "",
        "## Operadores Relacionais",
        "",
        "```",
        "G |- E1 : T1",
        "G |- E2 : T2",
        "T1 pertence a {int, real}",
        "T2 pertence a {int, real}",
        "rop pertence a {>, <, >=, <=, ==, !=}",
        "────────────────────────────────────────────────",
        "G |- (E1 E2 rop) : bool",
        "",
        "G |- E1 : T1",
        "G |- E2 : T2",
        "T1 = bool ou T2 = bool",
        "────────────────────────────────────────────────",
        "erro_semantico: operador relacional exige operandos numericos",
        "```",
        "",
        "## Definicao e Redefinicao de Variaveis",
        "",
        "### Primeira definicao",
        "",
        "Se a variavel ainda nao existe no contexto, ela recebe o tipo da expressao atribuida.",
        "",
        "```",
        "G |- E : T",
        "X nao pertence a dom(G)",
        "────────────────────────────────────────────────",
        "G |- (E X) : T",
        "G' = G unido {X : T}",
        "```",
        "",
        "### Redefinicao valida",
        "",
        "Se a variavel ja existe no contexto, a nova atribuicao so e valida quando o tipo da nova expressao e igual ao tipo ja registrado.",
        "",
        "```",
        "G(X) = T",
        "G |- E : T",
        "────────────────────────────────────────────────",
        "G |- (E X) : T",
        "```",
        "",
        "### Redefinicao invalida",
        "",
        "Se a variavel ja existe com tipo `T1` e recebe uma expressao de tipo `T2`, com `T1 != T2`, ocorre erro semantico.",
        "",
        "```",
        "G(X) = T1",
        "G |- E : T2",
        "T1 != T2",
        "────────────────────────────────────────────────",
        "erro_semantico: redefinicao incompativel de tipo",
        "```",
        "",
        "Exemplo invalido:",
        "",
        "```txt",
        "(START)",
        "(5 X)",
        "(3.14 X)",
        "(END)",
        "```",
        "",
        "Nesse caso, `X` foi definida como `int` e depois recebeu um valor `real`.",
        "",
        "## Carregar Memoria",
        "",
        "Uma variavel so pode ser usada depois de ter sido definida.",
        "",
        "```",
        "G(X) = T",
        "────────────────────────────────────────────────",
        "G |- (X) : T",
        "",
        "X nao pertence a dom(G)",
        "────────────────────────────────────────────────",
        "erro_semantico: variavel usada antes de ser definida",
        "```",
        "",
        "## Carregar Resultado — RES",
        "",
        "O comando `(N RES)` referencia um resultado anterior. O indice `N` deve ser inteiro positivo e deve existir resultado anterior suficiente.",
        "",
        "### RES valido",
        "",
        "```",
        "N : int",
        "N > 0",
        "existe resultado anterior na posicao N",
        "resultado_N : T",
        "────────────────────────────────────────────────",
        "G |- (N RES) : T",
        "```",
        "",
        "### RES invalido por indice zero ou negativo",
        "",
        "```",
        "N : int",
        "N <= 0",
        "────────────────────────────────────────────────",
        "erro_semantico: RES deve referenciar resultado anterior",
        "```",
        "",
        "### RES invalido por falta de resultado anterior",
        "",
        "```",
        "N : int",
        "N > 0",
        "nao existe resultado anterior suficiente",
        "────────────────────────────────────────────────",
        "erro_semantico: referencia invalida a resultado anterior",
        "```",
        "",
        "> O tipo de `(N RES)` e o tipo do resultado anterior referenciado. Portanto, ele nao deve permanecer como `desconhecido` quando a referencia e valida.",
        "",
        "## Condicional — IF",
        "",
        "A condicao de um `IF` deve ser uma expressao logica, isto e, do tipo `bool`.",
        "",
        "```",
        "G |- C : bool",
        "G |- bloco_then : ok",
        "G |- bloco_else : ok",
        "────────────────────────────────────────────────",
        "G |- if C then bloco_then else bloco_else : ok",
        "",
        "G |- C : T",
        "T != bool",
        "────────────────────────────────────────────────",
        "erro_semantico: condicao de IF deve ser bool",
        "```",
        "",
        "## Laco — WHILE",
        "",
        "A condicao de um `WHILE` deve ser uma expressao logica, isto e, do tipo `bool`.",
        "",
        "```",
        "G |- C : bool",
        "G |- bloco : ok",
        "────────────────────────────────────────────────",
        "G |- while C do bloco : ok",
        "",
        "G |- C : T",
        "T != bool",
        "────────────────────────────────────────────────",
        "erro_semantico: condicao de WHILE deve ser bool",
        "```",
        "",
        "## Expressoes Aninhadas",
        "",
        "Expressoes aninhadas sao tipadas de dentro para fora. O tipo inferido de uma subexpressao e usado como tipo de operando da expressao externa.",
        "",
        "Exemplo:",
        "",
        "```",
        "G |- 10 : int",
        "G |- 3 : int",
        "────────────────────────────────────────────────",
        "G |- (10 3 +) : int",
        "",
        "G |- (10 3 +) : int",
        "G |- 2.5 : real",
        "────────────────────────────────────────────────",
        "G |- ((10 3 +) 2.5 *) : real",
        "```",
        "",
        "## Regras de Erro",
        "",
        "O analisador semantico deve rejeitar o programa quando encontrar pelo menos um erro semantico.",
        "",
        "Sao erros semanticos:",
        "",
        "- usar variavel antes de definicao;",
        "- redefinir variavel com tipo diferente do tipo original;",
        "- usar `bool` em operacao aritmetica;",
        "- usar `/` ou `%` com operandos nao inteiros;",
        "- usar `^` com expoente nao inteiro;",
        "- usar condicao de `IF` diferente de `bool`; ",
        "- usar condicao de `WHILE` diferente de `bool`; ",
        "- usar `(0 RES)`;",
        "- usar `(N RES)` quando nao existe resultado anterior suficiente.",
        "",
        "Quando ha erro semantico, o resultado final deve ser:",
        "",
        "```txt",
        "ACEITO: False",
        "SEMANTICO: ERROS ENCONTRADOS",
        "```",
        "",
        "E o Assembly nao deve ser gerado para a execucao invalida.",
    ]

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


def salvarTabelaSimbolosMarkdown(tabela, caminho):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)

    linhas = [
        "# Tabela de Simbolos",
        "",
        "Gerada pelo Analisador Semantico — Fase 3.",
        "",
        "| Variavel | Tipo | Linha de Definicao | Linha de Ultimo Uso |",
        "|----------|------|-------------------|---------------------|",
    ]

    if tabela:
        for nome in sorted(tabela.keys()):
            info = tabela[nome]
            tipo = info.get("tipo", "desconhecido")
            l_def = info.get("linha_definicao", "-")
            l_uso = info.get("linha_ultimo_uso", "-")
            linhas.append(f"| `{nome}` | `{tipo}` | {l_def} | {l_uso} |")
    else:
        linhas.append("| — | — | — | — |")

    linhas += [
        "",
        "## Notas",
        "",
        "- **Tipo `int`**: variavel definida com literal inteiro (sem ponto decimal).",
        "- **Tipo `real`**: variavel definida com literal real (com ponto decimal) ou promovida por operacao int+real.",
        "- **Tipo `bool`**: variavel definida como resultado de operacao relacional.",
        "- **Tipo `desconhecido`**: tipo nao pode ser inferido estaticamente.",
        "- **Linha de Definicao**: primeira linha em que `(V MEM)` foi executado para esta variavel.",
        "- **Linha de Ultimo Uso**: ultima linha em que a variavel foi lida `(MEM)` ou redefinida.",
    ]

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


def salvarArvoreAtribuidaMarkdown(arvore_atribuida, caminho):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)

    linhas_md = [
        "# Arvore Sintatica Atribuida",
        "",
        "Gerada pelo Analisador Semantico — Fase 3.",
        "Cada no de expressao exibe seu tipo inferido entre colchetes `[tipo]`.",
        "",
        "```",
    ]

    def _texto_no_com_tipo(no, prefixo=""):
        tipo = no["tipo"]

        if tipo == "programa":
            linhas_md.append(f"{prefixo}programa [{no['linha_inicio']}..{no['linha_fim']}]")
            for cmd in no["comandos"]:
                _texto_no_com_tipo(cmd, prefixo + "  ")

        elif tipo == "expressao":
            linhas_md.append(f"{prefixo}expressao [linha {no['linha']}]")
            _texto_expr_com_tipo(no["estrutura"], prefixo + "  ")

        elif tipo == "if":
            linhas_md.append(f"{prefixo}if [linha {no.get('linha', '?')}]")
            linhas_md.append(f"{prefixo}  condicao:")
            _texto_expr_com_tipo(no["condicao"], prefixo + "    ")
            linhas_md.append(f"{prefixo}  then:")
            for item in no["bloco_then"]:
                _texto_no_com_tipo(item, prefixo + "    ")
            if no["bloco_else"] is not None:
                linhas_md.append(f"{prefixo}  else:")
                for item in no["bloco_else"]:
                    _texto_no_com_tipo(item, prefixo + "    ")

        elif tipo == "while":
            linhas_md.append(f"{prefixo}while [linha {no.get('linha', '?')}]")
            linhas_md.append(f"{prefixo}  condicao:")
            _texto_expr_com_tipo(no["condicao"], prefixo + "    ")
            linhas_md.append(f"{prefixo}  bloco:")
            for item in no["bloco"]:
                _texto_no_com_tipo(item, prefixo + "    ")

        else:
            linhas_md.append(f"{prefixo}{tipo}")

    def _texto_expr_com_tipo(no, prefixo):
        tipo = no["tipo"]
        tipo_inf = no.get("tipo_inferido", "")
        sufixo = f"  [{tipo_inf}]" if tipo_inf else ""

        if tipo == "numero":
            linhas_md.append(f"{prefixo}numero({no['valor']}){sufixo}")
        elif tipo == "carregar_memoria":
            linhas_md.append(f"{prefixo}memoria({no['nome']}){sufixo}")
        elif tipo == "carregar_resultado":
            linhas_md.append(f"{prefixo}res({no['indice']}){sufixo}")
        elif tipo == "gravar_memoria":
            linhas_md.append(f"{prefixo}gravar_memoria({no['nome']}){sufixo}")
            _texto_expr_com_tipo(no["valor"], prefixo + "  ")
        elif tipo == "binaria":
            linhas_md.append(f"{prefixo}binaria({no['operador']}){sufixo}")
            _texto_expr_com_tipo(no["esquerda"], prefixo + "  ")
            _texto_expr_com_tipo(no["direita"], prefixo + "  ")
        elif tipo == "relacional":
            linhas_md.append(f"{prefixo}relacional({no['operador']}){sufixo}")
            _texto_expr_com_tipo(no["esquerda"], prefixo + "  ")
            _texto_expr_com_tipo(no["direita"], prefixo + "  ")
        else:
            linhas_md.append(f"{prefixo}{tipo}{sufixo}")

    _texto_no_com_tipo(arvore_atribuida)
    linhas_md.append("```")
    linhas_md += [
        "",
        "## Legenda",
        "",
        "- `[int]`  — expressao de tipo inteiro",
        "- `[real]` — expressao de tipo real (ponto flutuante)",
        "- `[bool]` — expressao de tipo logico (resultado de operacao relacional)",
        "- `[desconhecido]` — tipo nao pode ser inferido estaticamente",
    ]

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_md) + "\n")


def salvarGramaticaAumentadaMarkdown(caminho):
    from gramatica import construirGramatica

    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    gramatica = construirGramatica()

    linhas = []
    linhas.append("# Gramatica Atribuida — EBNF")
    linhas.append("")
    linhas.append("Gramatica da linguagem RPN — Grupo RA2 17 (Fases 1-3).")
    linhas.append("")
    linhas.append("**Convencao EBNF:**")
    linhas.append("- `nao-terminais` em minusculas")
    linhas.append("- `TERMINAIS` em maiusculas")
    linhas.append("- `epsilon` representa vazio")
    linhas.append("")
    linhas.append("## Simbolo Inicial")
    linhas.append("")
    linhas.append(f"`{gramatica['simbolo_inicial']}`")
    linhas.append("")
    linhas.append("## Producoes")
    linhas.append("")
    linhas.append("```ebnf")

    for nt, regras in gramatica["producoes"].items():
        alternativas = [" ".join(regra) for regra in regras]
        linhas.append(f"{nt} ::= " + " | ".join(alternativas))

    linhas.append("```")
    linhas.append("")
    linhas.append("## Acoes Semanticas")
    linhas.append("")
    linhas.append("- Literais inteiros recebem tipo `int`.")
    linhas.append("- Literais reais recebem tipo `real`.")
    linhas.append("- Literais `TRUE` e `FALSE` recebem tipo `bool`.")
    linhas.append("- Variaveis sao registradas na primeira atribuicao `(V MEM)`.")
    linhas.append("- Usos de `(MEM)` exigem variavel previamente definida.")
    linhas.append("- Operadores `/` e `%` exigem operandos `int`.")
    linhas.append("- Operador `^` exige expoente `int`.")
    linhas.append("- Operadores relacionais produzem `bool`.")
    linhas.append("- Condicoes de `IF` e `WHILE` devem ter tipo `bool`.")
    linhas.append("- Assembly so e gerado se a analise semantica nao possuir erros.")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

def gerarArvoreAtribuida(arvore, tabela_simbolos, tipos=None):
    """
    Gera a arvore sintatica atribuida a partir da arvore inicial
    e da tabela de simbolos, incorporando os tipos inferidos em
    cada no de expressao.
    Entrada: arvore sintatica inicial, tabela de simbolos e tipos inferidos.
    Saida: arvore sintatica atribuida com campo tipo_inferido em cada no.
    """
    resultado = verificarTipos(arvore, tabela_simbolos)
    return resultado["arvore_atribuida"]