# Sistema de Regras de Tipos — Calculo de Sequentes

Este documento descreve as regras semanticas usadas pelo analisador semantico da Fase 3.

A linguagem utiliza tipagem estatica e forte. O tipo de uma variavel e inferido na primeira definicao e nao pode ser alterado posteriormente.

A promocao `int -> real` e permitida em expressoes aritmeticas compativeis, mas nao e permitida para redefinir o tipo de uma variavel ja registrada na tabela de simbolos.

## Julgamentos de Tipo

Um julgamento de tipo tem a forma:

```
G |- e : T
```

onde:

- `G` e o contexto semantico, isto e, a tabela de simbolos;
- `e` e uma expressao ou comando;
- `T` e o tipo inferido ou verificado;
- `T` pertence a {int, real, bool}.

## Axiomas

```
────────────────────────────────────────────────
NUMBER sem ponto decimal : int

────────────────────────────────────────────────
NUMBER com ponto decimal : real

────────────────────────────────────────────────
BOOL_LIT("TRUE") : bool

────────────────────────────────────────────────
BOOL_LIT("FALSE") : bool
```

> Literais booleanos sao reconhecidos pelo lexico como tokens `BOOL_LIT`, com valores `TRUE` ou `FALSE`.

## Operadores Aritmeticos

### Soma, Subtracao e Multiplicacao

```
G |- E1 : int
G |- E2 : int
op pertence a {+, -, *}
────────────────────────────────────────────────
G |- (E1 E2 op) : int

G |- E1 : real
G |- E2 : real
op pertence a {+, -, *}
────────────────────────────────────────────────
G |- (E1 E2 op) : real

G |- E1 : int
G |- E2 : real
op pertence a {+, -, *}
────────────────────────────────────────────────
G |- (E1 E2 op) : real

G |- E1 : real
G |- E2 : int
op pertence a {+, -, *}
────────────────────────────────────────────────
G |- (E1 E2 op) : real
```

### Divisao Real

```
G |- E1 : T1
G |- E2 : T2
T1 pertence a {int, real}
T2 pertence a {int, real}
────────────────────────────────────────────────
G |- (E1 E2 |) : real
```

### Divisao Inteira e Resto

```
G |- E1 : int
G |- E2 : int
op pertence a {/, %}
────────────────────────────────────────────────
G |- (E1 E2 op) : int

G |- E1 : T1
G |- E2 : T2
op pertence a {/, %}
T1 != int ou T2 != int
────────────────────────────────────────────────
erro_semantico: operador exige operandos inteiros
```

### Potenciacao

```
G |- E1 : int
G |- E2 : int
────────────────────────────────────────────────
G |- (E1 E2 ^) : int

G |- E1 : real
G |- E2 : int
────────────────────────────────────────────────
G |- (E1 E2 ^) : real

G |- E1 : T1
G |- E2 : T2
T2 != int
────────────────────────────────────────────────
erro_semantico: operador ^ exige expoente inteiro
```

> Operacoes entre `int` e `real` podem promover o resultado para `real` dentro da expressao. Essa promocao nao altera o tipo previamente registrado de uma variavel.

## Operadores Relacionais

```
G |- E1 : T1
G |- E2 : T2
T1 pertence a {int, real}
T2 pertence a {int, real}
rop pertence a {>, <, >=, <=, ==, !=}
────────────────────────────────────────────────
G |- (E1 E2 rop) : bool

G |- E1 : T1
G |- E2 : T2
T1 = bool ou T2 = bool
────────────────────────────────────────────────
erro_semantico: operador relacional exige operandos numericos
```

## Definicao e Redefinicao de Variaveis

### Primeira definicao

Se a variavel ainda nao existe no contexto, ela recebe o tipo da expressao atribuida.

```
G |- E : T
X nao pertence a dom(G)
────────────────────────────────────────────────
G |- (E X) : T
G' = G unido {X : T}
```

### Redefinicao valida

Se a variavel ja existe no contexto, a nova atribuicao so e valida quando o tipo da nova expressao e igual ao tipo ja registrado.

```
G(X) = T
G |- E : T
────────────────────────────────────────────────
G |- (E X) : T
```

### Redefinicao invalida

Se a variavel ja existe com tipo `T1` e recebe uma expressao de tipo `T2`, com `T1 != T2`, ocorre erro semantico.

```
G(X) = T1
G |- E : T2
T1 != T2
────────────────────────────────────────────────
erro_semantico: redefinicao incompativel de tipo
```

Exemplo invalido:

```txt
(START)
(5 X)
(3.14 X)
(END)
```

Nesse caso, `X` foi definida como `int` e depois recebeu um valor `real`.

## Carregar Memoria

Uma variavel so pode ser usada depois de ter sido definida.

```
G(X) = T
────────────────────────────────────────────────
G |- (X) : T

X nao pertence a dom(G)
────────────────────────────────────────────────
erro_semantico: variavel usada antes de ser definida
```

## Carregar Resultado — RES

O comando `(N RES)` referencia um resultado anterior. O indice `N` deve ser inteiro positivo e deve existir resultado anterior suficiente.

### RES valido

```
N : int
N > 0
existe resultado anterior na posicao N
resultado_N : T
────────────────────────────────────────────────
G |- (N RES) : T
```

### RES invalido por indice zero ou negativo

```
N : int
N <= 0
────────────────────────────────────────────────
erro_semantico: RES deve referenciar resultado anterior
```

### RES invalido por falta de resultado anterior

```
N : int
N > 0
nao existe resultado anterior suficiente
────────────────────────────────────────────────
erro_semantico: referencia invalida a resultado anterior
```

> O tipo de `(N RES)` e o tipo do resultado anterior referenciado. Portanto, ele nao deve permanecer como `desconhecido` quando a referencia e valida.

## Condicional — IF

A condicao de um `IF` deve ser uma expressao logica, isto e, do tipo `bool`.

```
G |- C : bool
G |- bloco_then : ok
G |- bloco_else : ok
────────────────────────────────────────────────
G |- if C then bloco_then else bloco_else : ok

G |- C : T
T != bool
────────────────────────────────────────────────
erro_semantico: condicao de IF deve ser bool
```

## Laco — WHILE

A condicao de um `WHILE` deve ser uma expressao logica, isto e, do tipo `bool`.

```
G |- C : bool
G |- bloco : ok
────────────────────────────────────────────────
G |- while C do bloco : ok

G |- C : T
T != bool
────────────────────────────────────────────────
erro_semantico: condicao de WHILE deve ser bool
```

## Expressoes Aninhadas

Expressoes aninhadas sao tipadas de dentro para fora. O tipo inferido de uma subexpressao e usado como tipo de operando da expressao externa.

Exemplo:

```
G |- 10 : int
G |- 3 : int
────────────────────────────────────────────────
G |- (10 3 +) : int

G |- (10 3 +) : int
G |- 2.5 : real
────────────────────────────────────────────────
G |- ((10 3 +) 2.5 *) : real
```

## Regras de Erro

O analisador semantico deve rejeitar o programa quando encontrar pelo menos um erro semantico.

Sao erros semanticos:

- usar variavel antes de definicao;
- redefinir variavel com tipo diferente do tipo original;
- usar `bool` em operacao aritmetica;
- usar `/` ou `%` com operandos nao inteiros;
- usar `^` com expoente nao inteiro;
- usar condicao de `IF` diferente de `bool`; 
- usar condicao de `WHILE` diferente de `bool`; 
- usar `(0 RES)`;
- usar `(N RES)` quando nao existe resultado anterior suficiente.

Quando ha erro semantico, o resultado final deve ser:

```txt
ACEITO: False
SEMANTICO: ERROS ENCONTRADOS
```

E o Assembly nao deve ser gerado para a execucao invalida.
