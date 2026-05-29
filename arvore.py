# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17

import json
import os

def gerarArvore(resultado_parser):
    if not resultado_parser["aceito"]:
        raise ValueError("Nao e possivel gerar arvore de um programa rejeitado")
    return resultado_parser["arvore"]


def noParaDict(no):
    tipo = no["tipo"]
    tipo_inferido = no.get("tipo_inferido")

    if tipo == "numero":
        d = {"tipo": tipo, "valor": no["valor"]}
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d
    
    if tipo == "bool_literal":
        d = {"tipo": tipo, "valor": no["valor"]}
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d
    
    if tipo == "carregar_memoria":
        d = {"tipo": tipo, "nome": no["nome"]}
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "carregar_resultado":
        d = {"tipo": tipo, "indice": no["indice"]}
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "gravar_memoria":
        d = {
            "tipo": tipo,
            "nome": no["nome"],
            "valor": noParaDict(no["valor"]),
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo in ("binaria", "relacional"):
        d = {
            "tipo": tipo,
            "operador": no["operador"],
            "esquerda": noParaDict(no["esquerda"]),
            "direita": noParaDict(no["direita"]),
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "expressao":
        d = {
            "tipo": "expressao",
            "linha": no["linha"],
            "fonte": no["fonte"],
            "estrutura": noParaDict(no["estrutura"]),
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "if":
        d = {
            "tipo": "if",
            "linha": no.get("linha"),
            "fonte": no.get("fonte"),
            "condicao": noParaDict(no["condicao"]),
            "bloco_then": [noParaDict(x) for x in no["bloco_then"]],
            "bloco_else": (
                None if no["bloco_else"] is None
                else [noParaDict(x) for x in no["bloco_else"]]
            ),
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "while":
        d = {
            "tipo": "while",
            "linha": no.get("linha"),
            "fonte": no.get("fonte"),
            "condicao": noParaDict(no["condicao"]),
            "bloco": [noParaDict(x) for x in no["bloco"]],
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    if tipo == "programa":
        d = {
            "tipo": "programa",
            "linha_inicio": no["linha_inicio"],
            "linha_fim": no["linha_fim"],
            "comandos": [noParaDict(x) for x in no["comandos"]],
        }
        if tipo_inferido:
            d["tipo_inferido"] = tipo_inferido
        return d

    raise ValueError(f"Tipo de no desconhecido ao serializar: {tipo}")


def adicionarLinhasExpressao(no, linhas, prefixo):
    tipo = no["tipo"]

    if tipo == "numero":
        linhas.append(f"{prefixo}numero({no['valor']})")
        return

    if tipo == "bool_literal":
        linhas.append(f"{prefixo}bool_literal({no['valor']})")
        return

    if tipo == "carregar_memoria":
        linhas.append(f"{prefixo}memoria({no['nome']})")
        return

    if tipo == "carregar_resultado":
        linhas.append(f"{prefixo}res({no['indice']})")
        return

    if tipo == "gravar_memoria":
        linhas.append(f"{prefixo}gravar_memoria({no['nome']})")
        adicionarLinhasExpressao(no["valor"], linhas, prefixo + "  ")
        return

    if tipo == "binaria":
        linhas.append(f"{prefixo}binaria({no['operador']})")
        adicionarLinhasExpressao(no["esquerda"], linhas, prefixo + "  ")
        adicionarLinhasExpressao(no["direita"], linhas, prefixo + "  ")
        return

    if tipo == "relacional":
        linhas.append(f"{prefixo}relacional({no['operador']})")
        adicionarLinhasExpressao(no["esquerda"], linhas, prefixo + "  ")
        adicionarLinhasExpressao(no["direita"], linhas, prefixo + "  ")
        return

    linhas.append(f"{prefixo}{tipo}")

def arvoreParaTexto(arvore):
    linhas = []

    def visitar(no, prefixo=""):
        tipo = no["tipo"]

        if tipo == "programa":
            linhas.append(
                f"{prefixo}programa [{no['linha_inicio']}..{no['linha_fim']}]"
            )
            for comando in no["comandos"]:
                visitar(comando, prefixo + "  ")
            return

        if tipo == "expressao":
            linhas.append(f"{prefixo}expressao [linha {no['linha']}]")
            adicionarLinhasExpressao(no["estrutura"], linhas, prefixo + "  ")
            return

        if tipo == "if":
            linha = no.get("linha", "?")
            linhas.append(f"{prefixo}if [linha {linha}]")
            linhas.append(f"{prefixo}  condicao:")
            adicionarLinhasExpressao(no["condicao"], linhas, prefixo + "    ")
            linhas.append(f"{prefixo}  then:")
            for item in no["bloco_then"]:
                visitar(item, prefixo + "    ")
            if no["bloco_else"] is not None:
                linhas.append(f"{prefixo}  else:")
                for item in no["bloco_else"]:
                    visitar(item, prefixo + "    ")
            return

        if tipo == "while":
            linha = no.get("linha", "?")
            linhas.append(f"{prefixo}while [linha {linha}]")
            linhas.append(f"{prefixo}  condicao:")
            adicionarLinhasExpressao(no["condicao"], linhas, prefixo + "    ")
            linhas.append(f"{prefixo}  bloco:")
            for item in no["bloco"]:
                visitar(item, prefixo + "    ")
            return

        linhas.append(f"{prefixo}{tipo}")

    visitar(arvore)
    return "\n".join(linhas)

def salvarArvoreJSON(arvore, caminho_saida):
    pasta = os.path.dirname(caminho_saida)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(noParaDict(arvore), arquivo, indent=2, ensure_ascii=False)

def salvarArvoreTexto(arvore, caminho_saida):
    pasta = os.path.dirname(caminho_saida)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(arvoreParaTexto(arvore))