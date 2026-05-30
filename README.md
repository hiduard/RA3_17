# Fase 3 — Analisador Semântico

## Informações Institucionais

- **Instituição**: PUCPR — Pontifícia Universidade Católica do Paraná
- **Ano / Semestre**: 2026 — 1º Semestre
- **Disciplina**: Linguagens Formais e Compiladores
- **Professor**: Frank Coelho de Alcantara
- **Grupo (Canvas)**: RA3 8
- **Linguagem de implementação**: Python 3

### Integrantes (ordem alfabética)

| Nome | GitHub |
|------|--------|
| Eduardo Hideo Itinoseke Ogassawara | hiduard |
| Gabriel Barbosa Fernandes de Oliveira | GabrielBarbosaFernandes |

---

## Como Executar

Nenhuma biblioteca externa é necessária. Apenas Python 3.8 ou superior.

### Executar o analisador

```bash
python AnalisadorSemantico.py <arquivo_de_entrada>
```

Exemplos:

```bash
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste3.txt
python AnalisadorSemantico.py teste_semantico_invalido.txt
python AnalisadorSemantico.py teste_sintatico_invalido.txt
python AnalisadorSemantico.py teste_lexico_invalido.txt
python AnalisadorSemantico.py teste_comentario_invalido.txt
```

### Executar a suíte completa de testes

```bash
python rodar_todos_testes.py
```

### Saída esperada no terminal

```
============================================================
  AnalisadorSemantico — Grupo RA3 8
  Arquivo: teste1.txt
============================================================
================= ETAPA 1: ANALISE LEXICA =================
  [OK]  N tokens reconhecidos em N linha(s)
  [OK]  Nenhum erro lexico encontrado
================= ETAPA 2: GRAMATICA LL(1) =================
  [OK]  28 nao-terminais, 74 producoes
  [OK]  Gramatica LL(1) sem conflitos
================== ETAPA 3: PARSING LL(1) ==================
  [OK]  N derivacoes aplicadas — programa sintaticamente valido
================ ETAPA 4: ARVORE SINTATICA ================
  [OK]  Arvore gerada com N comando(s) no nivel raiz
================ ETAPA 5: ANALISE SEMANTICA ================
  [OK]  Tabela de simbolos: N variavel(is) encontrada(s)
ACEITO: True
SEMANTICO: OK
============ ETAPA 6: GERACAO DE ASSEMBLY ARMv7 ============
  [OK]  Assembly gerado: N linhas -> output/programa.s
```

### Como depurar

```bash
cat output/arvore.txt
cat output/tokens_saida.txt
cat output/tabela_simbolos.json
cat output/erros_semanticos.txt
cat output/arvore_atribuida.txt
cat docs/tabela_simbolos.md
cat docs/arvore_atribuida.md
cat docs/gramatica_aumentada.md
cat docs/regras_sequentes.md
```

### Como validar o Assembly no CPUlator

1. Execute `python AnalisadorSemantico.py teste1.txt`
2. Acesse: https://cpulator.01xz.net/?sys=arm-de1soc
3. Copie o conteúdo de `output/programa.s` e cole no editor
4. Clique em **Compile and Load** (F5) e depois **Continue**

---

## Descrição da Linguagem

Todo programa começa com `(START)` e termina com `(END)`. As expressões seguem a **notação polonesa reversa (RPN)** no formato `(A B op)`.

### Operadores Aritméticos

| Operador | Operação | Tipos exigidos | Tipo resultado |
|----------|----------|----------------|----------------|
| `+` | Adição | int+int ou real+real ou int+real | int ou real |
| `-` | Subtração | int+int ou real+real ou int+real | int ou real |
| `*` | Multiplicação | int+int ou real+real ou int+real | int ou real |
| `\|` | Divisão real | numérico+numérico | real |
| `/` | Divisão inteira | **int+int** obrigatório | int |
| `%` | Resto | **int+int** obrigatório | int |
| `^` | Potenciação | base numérica, **expoente int** | mesmo da base |

### Operadores Relacionais

| Operador | Operação |
|----------|----------|
| `>` | Maior que |
| `<` | Menor que |
| `>=` | Maior ou igual |
| `<=` | Menor ou igual |
| `==` | Igual |
| `!=` | Diferente |

Operadores relacionais sempre produzem tipo `bool`.

### Comandos Especiais

| Sintaxe | Significado |
|---------|-------------|
| `(N RES)` | Carrega o resultado anterior indicado por N; N deve ser inteiro positivo e deve existir resultado anterior suficiente |
| `(V MEM)` | Grava o valor V na memória MEM (define a variável) |
| `(MEM)` | Carrega o valor armazenado em MEM |

### Comentários

| Sintaxe | Posição permitida |
|---------|-------------------|
| `*{ texto }*` | Linha inteira, fim de linha de código, ou entre expressões |

Comentários são reconhecidos pelo léxico e descartados — não geram tokens.

### Estruturas de Controle

**Condicional:**
```
(A B > IF)
  (comando_verdadeiro)
(ELSE)
  (comando_falso)
(ENDIF)
```
O bloco `(ELSE)` é opcional.

**Repetição:**
```
(A B < WHILE)
  (corpo_do_laco)
(ENDWHILE)
```

---

## Tipos Suportados

| Tipo | Descrição | Como é determinado |
|------|-----------|-------------------|
| `int` | Inteiro | Literal sem ponto decimal |
| `real` | Real de dupla precisão (IEEE 754) | Literal com ponto decimal |
| `bool` | Lógico | Resultado de operação relacional |

### Regras de Definição e Uso de Variáveis

- Uma variável só pode ser **usada** após ser **definida** com `(V MEM)`
- O tipo é determinado **na primeira definição** e permanece fixo durante todo o programa
- Redefinir uma variável com valor de tipo diferente do tipo original é erro semântico
- A promoção `int -> real` é permitida apenas dentro de expressões aritméticas, não na redefinição de variáveis
- Redefinir com `bool` ou redefinir uma variável `bool` com valor numérico também é erro semântico
- Memórias têm **escopo de arquivo** — cada arquivo `.txt` é um escopo independente
- `RES` é palavra reservada e não pode ser nome de variável

### Promoção de Tipos

A promoção de tipos ocorre somente durante a avaliação de expressões. Ela não altera o tipo previamente registrado de uma variável na tabela de símbolos.

```
int  op  int   →  int
int  op  real  →  real
real op  int   →  real
real op  real  →  real
T    rop T     →  bool   (T em {int, real})
bool não pode ser operando de operações aritméticas
```

### Redefinição de Variáveis

A linguagem adota tipagem estática e forte. Depois que uma variável é definida, seu tipo não pode ser alterado.

Exemplo válido:

```txt
(START)
(5 X)
(10 X)
(X)
(END)
```

Exemplo inválido:

```txt
(START)
(5 X)
(3.14 X)
(X)
(END)
```

Nesse caso, `X` foi definida inicialmente como `int` e depois recebeu um valor `real`, gerando erro semântico.

---

## Exemplos de Programas

### Programa semanticamente válido

```
(START)
*{ exemplo valido }*
(10 X)
(1.5 Y)
(((X) (Y) +) SOMA)
((X) 0 > WHILE)
(((X) 1 -) X)
((X) 5 == IF)
(99 FLAG)
(ELSE)
(0 FLAG)
(ENDIF)
(ENDWHILE)
(SOMA)
(END)
```

### Programa semanticamente inválido

```
(START)
*{ erro: divisao inteira com real }*
(10 A)
(3.5 B)
((A) (B) /)
*{ erro: variavel nao declarada }*
(NAODECLARADA)
(END)
```

Saída esperada:
```
ACEITO: False
SEMANTICO: ERROS ENCONTRADOS
  Linha 5: operador '/' exige int no operando direito, recebeu real
  Linha 7: variavel 'NAODECLARADA' usada antes de ser definida
```

---

## Arquivos de Teste

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `teste1.txt` | Válido | Operações básicas com inteiros e reais |
| `teste2.txt` | Válido | Aninhamento e promoção de tipos |
| `teste3.txt` | Válido | Tipos mistos, escopos e memórias |
| `teste_semantico_invalido.txt` | Erros semânticos | Divisão inteira com real, resto com real, variável não declarada, expoente real |
| `teste_sintatico_invalido.txt` | Erro sintático | Estrutura de controle mal formada |
| `teste_lexico_invalido.txt` | Erro léxico | Token inválido |
| `teste_comentario_invalido.txt` | Erro léxico | Comentário não fechado |

---

## Artefatos Gerados

### Pasta `output/`

| Arquivo | Conteúdo |
|---------|----------|
| `tokens_saida.txt` | Tokens gerados pela análise léxica |
| `parser_resultado.txt` | Resultado do parser com derivações LL(1) |
| `arvore.json` | Árvore sintática em JSON |
| `arvore.txt` | Árvore sintática em texto indentado |
| `tabela_simbolos.json` | Tabela de símbolos em JSON |
| `erros_semanticos.txt` | Erros semânticos encontrados |
| `arvore_atribuida.json` | Árvore atribuída com tipos em JSON |
| `arvore_atribuida.txt` | Árvore atribuída em texto |
| `programa.s` | Código Assembly ARMv7 (só se sem erros semânticos) |

### Pasta `docs/`

| Arquivo | Conteúdo |
|---------|----------|
| `gramatica_ll1.md` | Gramática LL(1) completa |
| `gramatica_aumentada.md` | Gramática atribuída em EBNF |
| `regras_sequentes.md` | Sistema de regras de tipos em cálculo de sequentes |
| `tabela_simbolos.md` | Tabela de símbolos em Markdown |
| `arvore_atribuida.md` | Árvore atribuída em Markdown |

---

## Estrutura do Repositório

```
.
├── AnalisadorSemantico.py         # Ponto de entrada
├── main.py                        # Lógica principal
├── tokens.py                      # Constantes de tipos de tokens
├── lexico.py                      # Analisador léxico (AFD, sem regex)
├── leitor.py                      # Leitura de arquivo por linha
├── utils.py                       # lerTokens / salvarTokens
├── gramatica.py                   # Gramática LL(1)
├── parser_ll1.py                  # Parser descendente recursivo LL(1)
├── arvore.py                      # Serialização da árvore sintática
├── assembly.py                    # Gerador de código ARMv7
├── semantico.py                   # Analisador semântico
├── rodar_todos_testes.py          # Suite de testes
├── teste1.txt                     # Válido
├── teste2.txt                     # Válido
├── teste3.txt                     # Válido
├── teste_semantico_invalido.txt   # Erros semânticos
├── teste_sintatico_invalido.txt   # Erro sintático
├── teste_lexico_invalido.txt      # Erro léxico
├── teste_comentario_invalido.txt  # Comentário não fechado
├── docs/
│   ├── gramatica_ll1.md
│   ├── gramatica_aumentada.md
│   ├── regras_sequentes.md
│   ├── tabela_simbolos.md
│   └── arvore_atribuida.md
└── output/
    ├── tokens_saida.txt
    ├── parser_resultado.txt
    ├── arvore.json
    ├── arvore.txt
    ├── tabela_simbolos.json
    ├── erros_semanticos.txt
    ├── arvore_atribuida.json
    ├── arvore_atribuida.txt
    └── programa.s
```

---

## Última Execução

Os artefatos presentes nas pastas `output/` e `docs/` foram gerados pela execução de:

```bash
python AnalisadorSemantico.py teste1.txt
```

Este arquivo cobre todos os recursos da linguagem: operações aritméticas, relacionais, estruturas de controle, comandos especiais e comentários.

---

## Decisões de Projeto

### Fatoração léxica de LPAREN

Para manter gramática LL(1) pura, o token `(` é classificado em 5 subtipos:

| Classe | Contexto |
|--------|----------|
| `LPAREN_CMD` | Inicia comando ou expressão |
| `LPAREN_END` | Antes de `END` |
| `LPAREN_ELSE` | Antes de `ELSE` |
| `LPAREN_ENDIF` | Antes de `ENDIF` |
| `LPAREN_ENDWHILE` | Antes de `ENDWHILE` |

### Comentários

Reconhecidos pelo léxico no estado `estadoComentario` — consumidos e descartados antes de gerar tokens. Podem aparecer em qualquer posição.

### Ponto flutuante no Assembly

Todos os valores são `double` (IEEE 754 64 bits) com registradores VFP do ARMv7 (`d0`–`d2`). Divisão inteira e resto convertem via `vcvt`.

### Potenciação

Implementada por loop de multiplicação. Expoente ≤ 0 produz 1.0.