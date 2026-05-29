# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17

import sys
import json
import os

import arvore
from gramatica import construirGramatica
from parser_ll1 import parsear
from arvore import gerarArvore, arvoreParaTexto, salvarArvoreJSON, salvarArvoreTexto
from assembly import gerarAssembly
from utils import lerTokens, salvarTokens
from leitor import lerArquivo
from lexico import parseExpressao
from semantico import (
    construirTabelaSimbolos,
    verificarTipos,
    gerarArvoreAtribuida,
    salvarTabelaSimbolos,
    salvarTabelaSimbolosMarkdown,
    salvarRelatorioErrosSemanticos,
    salvarArvoreAtribuida,
    salvarArvoreAtribuidaMarkdown,
    salvarGramaticaAumentadaMarkdown,
    salvarRegrasSequentes,
)

LARGURA = 60

def _separador(titulo=""):
    if titulo:
        lado = (LARGURA - len(titulo) - 2) // 2
        print("=" * lado + f" {titulo} " + "=" * lado)
    else:
        print("=" * LARGURA)

def _ok(msg):
    print(f"  [OK]  {msg}")

def _erro(msg):
    print(f"  [!!]  {msg}")

def _info(msg):
    print(f"        {msg}")

def garantir_pasta(caminho):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

def salvar_gramatica_markdown(gramatica, caminho):
    garantir_pasta(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("# Gramatica LL(1)\n\n")
        arquivo.write("## Simbolo inicial\n\n")
        arquivo.write(f"`{gramatica['simbolo_inicial']}`\n\n")
        arquivo.write("## Producoes\n\n")
        arquivo.write("Notacao EBNF: **nao-terminais em minusculas**, **TERMINAIS EM MAIUSCULAS**.\n\n")
        for A, regras in gramatica["producoes"].items():
            for regra in regras:
                lado_direito = " ".join(regra)
                arquivo.write(f"- `{A} -> {lado_direito}`\n")
        arquivo.write("\n")
        arquivo.write("## FIRST\n\n")
        for nt in sorted(gramatica["first"]):
            conteudo = ", ".join(sorted(gramatica["first"][nt]))
            arquivo.write(f"- `FIRST({nt}) = {{ {conteudo} }}`\n")
        arquivo.write("\n")
        arquivo.write("## FOLLOW\n\n")
        for nt in sorted(gramatica["follow"]):
            conteudo = ", ".join(sorted(gramatica["follow"][nt]))
            arquivo.write(f"- `FOLLOW({nt}) = {{ {conteudo} }}`\n")
        arquivo.write("\n")
        arquivo.write("## Tabela LL(1)\n\n")
        for nt in sorted(gramatica["tabela"]):
            arquivo.write(f"### {nt}\n\n")
            for terminal, regra in sorted(gramatica["tabela"][nt].items()):
                lado_direito = " ".join(regra)
                arquivo.write(f"- `[{nt}, {terminal}] -> {lado_direito}`\n")
            arquivo.write("\n")
        arquivo.write("## Conflitos\n\n")
        if gramatica["conflitos"]:
            for conflito in gramatica["conflitos"]:
                A, terminal, antiga, nova = conflito
                arquivo.write(f"- Conflito em `{A}, {terminal}`: `{antiga}` x `{nova}`\n")
        else:
            arquivo.write("Sem conflitos LL(1).\n")

def salvar_gramatica_com_arvore(gramatica, arvore, caminho):
    salvar_gramatica_markdown(gramatica, caminho)
    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write("\n---\n\n")
        arquivo.write("## Arvore Sintatica (ultimo teste)\n\n")
        arquivo.write("```\n")
        arquivo.write(arvoreParaTexto(arvore))
        arquivo.write("\n```\n")

def salvar_resultado_parser(resultado, caminho):
    garantir_pasta(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"ACEITO: {resultado['aceito']}\n\n")
        if resultado.get("erros_lexicos"):
            arquivo.write("ERROS LEXICOS:\n")
            for e in resultado["erros_lexicos"]:
                arquivo.write(f"  {e}\n")
            return
        if resultado["erro"]:
            arquivo.write(f"ERRO SINTATICO: {resultado['erro']}\n\n")
            if resultado["derivacoes"]:
                arquivo.write("DERIVACOES APLICADAS ATE O ERRO:\n")
                for derivacao in resultado["derivacoes"]:
                    arquivo.write(json.dumps(derivacao, ensure_ascii=False))
                    arquivo.write("\n")
            return
        arquivo.write("DERIVACOES:\n")
        for derivacao in resultado["derivacoes"]:
            arquivo.write(json.dumps(derivacao, ensure_ascii=False))
            arquivo.write("\n")

def salvar_assembly(codigo, caminho):
    garantir_pasta(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)

def bloquear_assembly(motivo):
    garantir_pasta("output/programa.s")
    with open("output/programa.s", "w", encoding="utf-8") as f:
        f.write(f"@ Assembly nao gerado: {motivo}.\n")

def carregar_entrada(nome_arquivo):
    if nome_arquivo.endswith(".tok") or nome_arquivo.endswith(".tokens"):
        return lerTokens(nome_arquivo)
    
    linhas = lerArquivo(nome_arquivo)
    if linhas and linhas[0][1] == "ERRO_COMENTARIO_NAO_FECHADO":
        linha_err = linhas[0][0]
        return [(linha_err, "ERRO_COMENTARIO_NAO_FECHADO",
                [("INVALID", "COMENTARIO_NAO_FECHADO")])]

    tokens_por_linha = []
    for numero_linha, linha in linhas:
        tokens = parseExpressao(linha)
        tokens_por_linha.append((numero_linha, linha, tokens))
    return tokens_por_linha

def prepararEntradaSemantica(nome_arquivo):
    """
    Carrega o programa-fonte, remove comentarios e prepara
    os tokens para o analisador sintatico e semantico.
    Entrada: nome do arquivo de teste.
    Saida: vetor de tokens sem comentarios.
    """
    return carregar_entrada(nome_arquivo)

def main():
    if len(sys.argv) != 2:
        print("Uso: python AnalisadorSemantico.py <arquivo_de_entrada>")
        print("Exemplo: python AnalisadorSemantico.py teste1.txt")
        return

    nome_arquivo = sys.argv[1]

    if not os.path.isfile(nome_arquivo):
        print(f"Erro: arquivo '{nome_arquivo}' nao encontrado.")
        return

    _separador()
    print(f"  AnalisadorSemantico — Grupo RA2 17")
    print(f"  Arquivo: {nome_arquivo}")
    _separador()

    # Etapa 1: analise lexica
    _separador("ETAPA 1: ANALISE LEXICA")
    tokens_por_linha = prepararEntradaSemantica(nome_arquivo)
    total_tokens = sum(len(t) for _, _, t in tokens_por_linha)
    total_linhas = len(tokens_por_linha)
    _ok(f"{total_tokens} tokens reconhecidos em {total_linhas} linha(s)")

    erros_lex = []
    for nl, linha, toks in tokens_por_linha:
        for tok in toks:
            if tok[0] in ("INVALID", "UNTERMINATED_COMMENT"):
                erros_lex.append(f"Linha {nl}: token invalido '{tok[1]}'")

    if erros_lex:
        for e in erros_lex:
            _erro(e)
        salvarTokens(tokens_por_linha, "output/tokens_saida.txt")
        bloquear_assembly("programa possui erros lexicos")
        _separador()
        print("ACEITO: False")
        return

    _ok("Nenhum erro lexico encontrado")

    _separador("ETAPA 2: GRAMATICA LL(1)")
    gramatica = construirGramatica()
    nao_terminais = len(gramatica["producoes"])
    total_prod = sum(len(r) for r in gramatica["producoes"].values())
    _ok(f"{nao_terminais} nao-terminais, {total_prod} producoes")
    if gramatica["conflitos"]:
        _erro(f"{len(gramatica['conflitos'])} conflito(s) LL(1) detectado(s)!")
    else:
        _ok("Gramatica LL(1) sem conflitos")

    _separador("ETAPA 3: PARSING LL(1)")
    resultado = parsear(tokens_por_linha, gramatica["tabela"])
    salvarTokens(tokens_por_linha, "output/tokens_saida.txt")
    salvar_resultado_parser(resultado, "output/parser_resultado.txt")

    if not resultado["aceito"]:
        if resultado.get("erros_lexicos"):
            for e in resultado["erros_lexicos"]:
                _erro(f"LEXICO: {e}")
        else:
            _erro(f"SINTATICO: {resultado['erro']}")
            bloquear_assembly("programa possui erros sintaticos")
        salvar_gramatica_markdown(gramatica, "docs/gramatica_ll1.md")
        salvarGramaticaAumentadaMarkdown("docs/gramatica_aumentada.md")
        _separador()
        print("ACEITO: False")
        return

    _ok(f"{len(resultado['derivacoes'])} derivacoes aplicadas — programa sintaticamente valido")

    _separador("ETAPA 4: ARVORE SINTATICA")
    try:
        arvore = gerarArvore(resultado)
    except ValueError as e:
        _erro(f"Erro ao obter arvore: {e}")
        bloquear_assembly("nao foi possivel gerar a arvore sintatica")
        _separador()
        print("ACEITO: False")
        return

    n_comandos = len(arvore["comandos"])
    _ok(f"Arvore gerada com {n_comandos} comando(s) no nivel raiz")
    salvarArvoreJSON(arvore, "output/arvore.json")
    salvarArvoreTexto(arvore, "output/arvore.txt")
    _ok("output/arvore.json  |  output/arvore.txt")

    _separador("ETAPA 5: ANALISE SEMANTICA")
    salvarRegrasSequentes("docs/regras_sequentes.md")
    salvarGramaticaAumentadaMarkdown("docs/gramatica_aumentada.md")

    tabela_simbolos = construirTabelaSimbolos(arvore)
    resultado_semantico = verificarTipos(arvore, tabela_simbolos)
    arvore_atribuida = resultado_semantico["arvore_atribuida"]

    salvarTabelaSimbolos(tabela_simbolos, "output/tabela_simbolos.json")
    salvarTabelaSimbolosMarkdown(tabela_simbolos, "docs/tabela_simbolos.md")

    n_vars = len(tabela_simbolos)
    _ok(f"Tabela de simbolos: {n_vars} variavel(is) encontrada(s)")
    if tabela_simbolos:
        for nome, info in sorted(tabela_simbolos.items()):
            _info(f"  {nome:12s}  tipo={info['tipo']:12s}  def=linha {info['linha_definicao']}  uso=linha {info['linha_ultimo_uso']}")

    salvarRelatorioErrosSemanticos(resultado_semantico["erros"], "output/erros_semanticos.txt")
    salvarArvoreAtribuida(arvore_atribuida, "output/arvore_atribuida.json", "output/arvore_atribuida.txt")
    salvarArvoreAtribuidaMarkdown(arvore_atribuida, "docs/arvore_atribuida.md")

    print()
    print(f"ACEITO: {resultado_semantico['valido']}")
    print(f"SEMANTICO: {'OK' if resultado_semantico['valido'] else 'ERROS ENCONTRADOS'}")
    
    if not resultado_semantico["valido"]:
        print()
        _erro(f"{len(resultado_semantico['erros'])} erro(s) semantico(s) encontrado(s):")
        for e in resultado_semantico["erros"]:
            _info(f"  {e}")

        salvar_gramatica_com_arvore(gramatica, arvore, "docs/gramatica_ll1.md")

        with open("output/programa.s", "w", encoding="utf-8") as f:
            f.write("@ Assembly nao gerado: programa possui erros semanticos.\n")

        print()
        _separador("ARQUIVOS GERADOS (sem Assembly — erros semanticos)")
        _info("output/tokens_saida.txt")
        _info("output/parser_resultado.txt")
        _info("output/arvore.json / arvore.txt")
        _info("output/tabela_simbolos.json")
        _info("output/erros_semanticos.txt")
        _info("output/arvore_atribuida.json / arvore_atribuida.txt")
        _info("output/programa.s (marcado como nao gerado)")
        _info("docs/gramatica_ll1.md / gramatica_aumentada.md")
        _info("docs/regras_sequentes.md / tabela_simbolos.md / arvore_atribuida.md")
        _separador()

        return

    _ok("Nenhum erro semantico — tipos consistentes")

    _separador("ETAPA 6: GERACAO DE ASSEMBLY ARMv7")
    try:
        codigo = gerarAssembly(arvore_atribuida)
    except ValueError as e:
        _erro(f"Erro na geracao de Assembly: {e}")
        salvar_gramatica_com_arvore(gramatica, arvore, "docs/gramatica_ll1.md")
        _separador()
        return

    salvar_assembly(codigo, "output/programa.s")
    salvar_gramatica_com_arvore(gramatica, arvore, "docs/gramatica_ll1.md")
    linhas_asm = len(codigo.splitlines())
    _ok(f"Assembly gerado: {linhas_asm} linhas -> output/programa.s")

    print()
    _separador("ARVORE SINTATICA")
    print(arvoreParaTexto(arvore))

    print()
    _separador("ARQUIVOS GERADOS")
    _info("output/tokens_saida.txt")
    _info("output/parser_resultado.txt")
    _info("output/arvore.json / arvore.txt")
    _info("output/tabela_simbolos.json")
    _info("output/erros_semanticos.txt")
    _info("output/arvore_atribuida.json / arvore_atribuida.txt")
    _info("output/programa.s")
    _info("docs/gramatica_ll1.md / gramatica_aumentada.md")
    _info("docs/regras_sequentes.md / tabela_simbolos.md / arvore_atribuida.md")
    _separador()

if __name__ == "__main__":
    main()