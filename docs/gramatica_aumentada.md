# Gramatica Atribuida — EBNF

Gramatica da linguagem RPN — Grupo RA2 17 (Fases 1-3).

**Convencao EBNF:**
- `nao-terminais` em minusculas
- `TERMINAIS` em maiusculas
- `epsilon` representa vazio

## Simbolo Inicial

`programa`

## Producoes

```ebnf
programa ::= abre_start lista_prog fecha_end
abre_start ::= LPAREN_CMD START RPAREN
fecha_end ::= LPAREN_END END RPAREN
lista_prog ::= comando lista_prog | epsilon
lista_if ::= comando lista_if | epsilon
lista_while ::= comando lista_while | epsilon
comando ::= LPAREN_CMD interior
interior ::= NUMBER apos_num | MEMORY apos_mem | BOOL_LIT apos_bool | LPAREN_CMD sub apos_sub
apos_num ::= RES RPAREN | NUMBER resto_num | MEMORY resto_mem_grava | LPAREN_CMD sub resto_sub
apos_mem ::= RPAREN | NUMBER resto_num | MEMORY resto_mem_grava | LPAREN_CMD sub resto_sub | IF RPAREN lista_if fim_if | WHILE RPAREN lista_while abre_endwhile
apos_sub ::= RPAREN | NUMBER resto_num | MEMORY resto_mem_grava | LPAREN_CMD sub resto_sub | IF RPAREN lista_if fim_if | WHILE RPAREN lista_while abre_endwhile
apos_bool ::= MEMORY RPAREN | RPAREN | LPAREN_CMD sub resto_sub | IF RPAREN lista_if fim_if | WHILE RPAREN lista_while abre_endwhile
apos_bool_sub ::= MEMORY RPAREN | RPAREN | LPAREN_CMD sub resto_sub_sub
resto_num ::= OPERATOR RPAREN | REL_OP cauda_rel
resto_mem_grava ::= RPAREN | OPERATOR RPAREN | REL_OP cauda_rel
resto_sub ::= OPERATOR RPAREN | REL_OP cauda_rel
cauda_rel ::= RPAREN | IF RPAREN lista_if fim_if | WHILE RPAREN lista_while abre_endwhile
fim_if ::= abre_else lista_if abre_endif | abre_endif
abre_else ::= LPAREN_ELSE ELSE RPAREN
abre_endif ::= LPAREN_ENDIF ENDIF RPAREN
abre_endwhile ::= LPAREN_ENDWHILE ENDWHILE RPAREN
sub ::= NUMBER apos_num_sub | MEMORY apos_mem_sub | BOOL_LIT apos_bool_sub | LPAREN_CMD sub apos_sub_sub
apos_num_sub ::= RES RPAREN | NUMBER resto_num_sub | MEMORY resto_mem_grava_sub | LPAREN_CMD sub resto_sub_sub
apos_mem_sub ::= RPAREN | NUMBER resto_num_sub | MEMORY resto_mem_grava_sub | LPAREN_CMD sub resto_sub_sub
apos_sub_sub ::= RPAREN | NUMBER resto_num_sub | MEMORY resto_mem_grava_sub | LPAREN_CMD sub resto_sub_sub
resto_num_sub ::= OPERATOR RPAREN | REL_OP RPAREN
resto_mem_grava_sub ::= RPAREN | OPERATOR RPAREN | REL_OP RPAREN
resto_sub_sub ::= OPERATOR RPAREN | REL_OP RPAREN
```

## Acoes Semanticas

- Literais inteiros recebem tipo `int`.
- Literais reais recebem tipo `real`.
- Literais `TRUE` e `FALSE` recebem tipo `bool`.
- Variaveis sao registradas na primeira atribuicao `(V MEM)`.
- Usos de `(MEM)` exigem variavel previamente definida.
- Operadores `/` e `%` exigem operandos `int`.
- Operador `^` exige expoente `int`.
- Operadores relacionais produzem `bool`.
- Condicoes de `IF` e `WHILE` devem ter tipo `bool`.
- Assembly so e gerado se a analise semantica nao possuir erros.