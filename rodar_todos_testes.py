# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17

import subprocess
import sys
import os

ARQUIVOS_VALIDOS = [
    ("teste1.txt", "operacoes basicas com inteiros e reais"),
    ("teste2.txt", "aninhamento profundo e promocao de tipos"),
    ("teste3.txt", "tipos mistos, escopos e memorias"),
]

ARQUIVOS_ERROS_SEMANTICOS = [
    ("teste_semantico_invalido.txt", "divisao inteira com real, resto com real, variavel nao declarada, expoente real"),
]

ARQUIVOS_INVALIDOS = [
    ("teste_sintatico_invalido.txt",  "erro sintatico"),
    ("teste_lexico_invalido.txt",     "erro lexico"),
    ("teste_comentario_invalido.txt", "comentario nao fechado"),
]

LARGURA = 70

def rodar(arquivo):
    resultado = subprocess.run(
        [sys.executable, "AnalisadorSemantico.py", arquivo],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    saida = resultado.stdout
    aceito          = "ACEITO: True"                  in saida
    semantico_ok    = "SEMANTICO: OK"                 in saida
    semantico_erros = "SEMANTICO: ERROS ENCONTRADOS"  in saida
    return aceito, semantico_ok, semantico_erros, saida

def _sep(titulo=""):
    if titulo:
        lado = (LARGURA - len(titulo) - 2) // 2
        print("-" * lado + f" {titulo} " + "-" * lado)
    else:
        print("-" * LARGURA)

def main():
    total = 0
    sucessos = 0

    _sep()
    print("  Suite de Testes — Analisador Semantico  |  Grupo RA2 17")
    _sep()

    print()
    _sep("VALIDOS  (esperado: ACEITO=True + SEMANTICO=OK)")
    print()

    for arquivo, descricao in ARQUIVOS_VALIDOS:
        total += 1
        if not os.path.isfile(arquivo):
            print(f"  [AUSENTE] {arquivo}")
            continue
        aceito, sem_ok, _, _ = rodar(arquivo)
        ok = aceito and sem_ok
        status = "PASSOU" if ok else "FALHOU"
        print(f"  [{status:6s}]  {arquivo}")
        print(f"            {descricao}")
        if not ok:
            print(f"            ACEITO={aceito}  SEMANTICO_OK={sem_ok}")
        if ok:
            sucessos += 1
        print()

    _sep("ERROS SEMANTICOS  (esperado: ACEITO=False + SEMANTICO=ERROS)")
    print()

    for arquivo, descricao in ARQUIVOS_ERROS_SEMANTICOS:
        total += 1
        if not os.path.isfile(arquivo):
            print(f"  [AUSENTE] {arquivo}")
            continue
        aceito, _, sem_erros, _ = rodar(arquivo)
        ok = (not aceito) and sem_erros
        status = "PASSOU" if ok else "FALHOU"
        print(f"  [{status:6s}]  {arquivo}")
        print(f"            {descricao}")
        if not ok:
            print(f"            ACEITO={aceito}  SEMANTICO_ERROS={sem_erros}")
        if ok:
            sucessos += 1
        print()

    _sep("INVALIDOS  (esperado: ACEITO=False)")
    print()

    for arquivo, motivo in ARQUIVOS_INVALIDOS:
        total += 1
        if not os.path.isfile(arquivo):
            print(f"  [AUSENTE] {arquivo}")
            continue
        aceito, _, _, _ = rodar(arquivo)
        ok = not aceito
        status = "PASSOU" if ok else "FALHOU"
        print(f"  [{status:6s}]  {arquivo}")
        print(f"            motivo esperado: {motivo}")
        if not ok:
            print(f"            ACEITO={aceito}  (esperava False)")
        if ok:
            sucessos += 1
        print()

    _sep()
    print(f"  Resultado final: {sucessos}/{total} testes com o resultado esperado.")
    _sep()

    if sucessos == total:
        print("  Todos os testes passaram!")
    else:
        print(f"  {total - sucessos} teste(s) falharam. Verifique os detalhes acima.")

if __name__ == "__main__":
    main()