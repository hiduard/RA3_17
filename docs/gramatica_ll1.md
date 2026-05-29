# Gramatica LL(1)

## Simbolo inicial

`programa`

## Producoes

Notacao EBNF: **nao-terminais em minusculas**, **TERMINAIS EM MAIUSCULAS**.

- `programa -> abre_start lista_prog fecha_end`
- `abre_start -> LPAREN_CMD START RPAREN`
- `fecha_end -> LPAREN_END END RPAREN`
- `lista_prog -> comando lista_prog`
- `lista_prog -> epsilon`
- `lista_if -> comando lista_if`
- `lista_if -> epsilon`
- `lista_while -> comando lista_while`
- `lista_while -> epsilon`
- `comando -> LPAREN_CMD interior`
- `interior -> NUMBER apos_num`
- `interior -> MEMORY apos_mem`
- `interior -> BOOL_LIT apos_bool`
- `interior -> LPAREN_CMD sub apos_sub`
- `apos_num -> RES RPAREN`
- `apos_num -> NUMBER resto_num`
- `apos_num -> MEMORY resto_mem_grava`
- `apos_num -> LPAREN_CMD sub resto_sub`
- `apos_mem -> RPAREN`
- `apos_mem -> NUMBER resto_num`
- `apos_mem -> MEMORY resto_mem_grava`
- `apos_mem -> LPAREN_CMD sub resto_sub`
- `apos_mem -> IF RPAREN lista_if fim_if`
- `apos_mem -> WHILE RPAREN lista_while abre_endwhile`
- `apos_sub -> RPAREN`
- `apos_sub -> NUMBER resto_num`
- `apos_sub -> MEMORY resto_mem_grava`
- `apos_sub -> LPAREN_CMD sub resto_sub`
- `apos_sub -> IF RPAREN lista_if fim_if`
- `apos_sub -> WHILE RPAREN lista_while abre_endwhile`
- `apos_bool -> MEMORY RPAREN`
- `apos_bool -> RPAREN`
- `apos_bool -> LPAREN_CMD sub resto_sub`
- `apos_bool -> IF RPAREN lista_if fim_if`
- `apos_bool -> WHILE RPAREN lista_while abre_endwhile`
- `apos_bool_sub -> MEMORY RPAREN`
- `apos_bool_sub -> RPAREN`
- `apos_bool_sub -> LPAREN_CMD sub resto_sub_sub`
- `resto_num -> OPERATOR RPAREN`
- `resto_num -> REL_OP cauda_rel`
- `resto_mem_grava -> RPAREN`
- `resto_mem_grava -> OPERATOR RPAREN`
- `resto_mem_grava -> REL_OP cauda_rel`
- `resto_sub -> OPERATOR RPAREN`
- `resto_sub -> REL_OP cauda_rel`
- `cauda_rel -> RPAREN`
- `cauda_rel -> IF RPAREN lista_if fim_if`
- `cauda_rel -> WHILE RPAREN lista_while abre_endwhile`
- `fim_if -> abre_else lista_if abre_endif`
- `fim_if -> abre_endif`
- `abre_else -> LPAREN_ELSE ELSE RPAREN`
- `abre_endif -> LPAREN_ENDIF ENDIF RPAREN`
- `abre_endwhile -> LPAREN_ENDWHILE ENDWHILE RPAREN`
- `sub -> NUMBER apos_num_sub`
- `sub -> MEMORY apos_mem_sub`
- `sub -> BOOL_LIT apos_bool_sub`
- `sub -> LPAREN_CMD sub apos_sub_sub`
- `apos_num_sub -> RES RPAREN`
- `apos_num_sub -> NUMBER resto_num_sub`
- `apos_num_sub -> MEMORY resto_mem_grava_sub`
- `apos_num_sub -> LPAREN_CMD sub resto_sub_sub`
- `apos_mem_sub -> RPAREN`
- `apos_mem_sub -> NUMBER resto_num_sub`
- `apos_mem_sub -> MEMORY resto_mem_grava_sub`
- `apos_mem_sub -> LPAREN_CMD sub resto_sub_sub`
- `apos_sub_sub -> RPAREN`
- `apos_sub_sub -> NUMBER resto_num_sub`
- `apos_sub_sub -> MEMORY resto_mem_grava_sub`
- `apos_sub_sub -> LPAREN_CMD sub resto_sub_sub`
- `resto_num_sub -> OPERATOR RPAREN`
- `resto_num_sub -> REL_OP RPAREN`
- `resto_mem_grava_sub -> RPAREN`
- `resto_mem_grava_sub -> OPERATOR RPAREN`
- `resto_mem_grava_sub -> REL_OP RPAREN`
- `resto_sub_sub -> OPERATOR RPAREN`
- `resto_sub_sub -> REL_OP RPAREN`

## FIRST

- `FIRST(abre_else) = { LPAREN_ELSE }`
- `FIRST(abre_endif) = { LPAREN_ENDIF }`
- `FIRST(abre_endwhile) = { LPAREN_ENDWHILE }`
- `FIRST(abre_start) = { LPAREN_CMD }`
- `FIRST(apos_bool) = { IF, LPAREN_CMD, MEMORY, RPAREN, WHILE }`
- `FIRST(apos_bool_sub) = { LPAREN_CMD, MEMORY, RPAREN }`
- `FIRST(apos_mem) = { IF, LPAREN_CMD, MEMORY, NUMBER, RPAREN, WHILE }`
- `FIRST(apos_mem_sub) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(apos_num) = { LPAREN_CMD, MEMORY, NUMBER, RES }`
- `FIRST(apos_num_sub) = { LPAREN_CMD, MEMORY, NUMBER, RES }`
- `FIRST(apos_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, RPAREN, WHILE }`
- `FIRST(apos_sub_sub) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(cauda_rel) = { IF, RPAREN, WHILE }`
- `FIRST(comando) = { LPAREN_CMD }`
- `FIRST(fecha_end) = { LPAREN_END }`
- `FIRST(fim_if) = { LPAREN_ELSE, LPAREN_ENDIF }`
- `FIRST(interior) = { BOOL_LIT, LPAREN_CMD, MEMORY, NUMBER }`
- `FIRST(lista_if) = { LPAREN_CMD, epsilon }`
- `FIRST(lista_prog) = { LPAREN_CMD, epsilon }`
- `FIRST(lista_while) = { LPAREN_CMD, epsilon }`
- `FIRST(programa) = { LPAREN_CMD }`
- `FIRST(resto_mem_grava) = { OPERATOR, REL_OP, RPAREN }`
- `FIRST(resto_mem_grava_sub) = { OPERATOR, REL_OP, RPAREN }`
- `FIRST(resto_num) = { OPERATOR, REL_OP }`
- `FIRST(resto_num_sub) = { OPERATOR, REL_OP }`
- `FIRST(resto_sub) = { OPERATOR, REL_OP }`
- `FIRST(resto_sub_sub) = { OPERATOR, REL_OP }`
- `FIRST(sub) = { BOOL_LIT, LPAREN_CMD, MEMORY, NUMBER }`

## FOLLOW

- `FOLLOW(abre_else) = { LPAREN_CMD, LPAREN_ENDIF }`
- `FOLLOW(abre_endif) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(abre_endwhile) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(abre_start) = { LPAREN_CMD, LPAREN_END }`
- `FOLLOW(apos_bool) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_bool_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(apos_mem) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_mem_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(apos_num) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_num_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(apos_sub) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_sub_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(cauda_rel) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(comando) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(fecha_end) = { $ }`
- `FOLLOW(fim_if) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(interior) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(lista_if) = { LPAREN_ELSE, LPAREN_ENDIF }`
- `FOLLOW(lista_prog) = { LPAREN_END }`
- `FOLLOW(lista_while) = { LPAREN_ENDWHILE }`
- `FOLLOW(programa) = { $ }`
- `FOLLOW(resto_mem_grava) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_mem_grava_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(resto_num) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_num_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(resto_sub) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_sub_sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`
- `FOLLOW(sub) = { IF, LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN, WHILE }`

## Tabela LL(1)

### abre_else

- `[abre_else, LPAREN_ELSE] -> LPAREN_ELSE ELSE RPAREN`

### abre_endif

- `[abre_endif, LPAREN_ENDIF] -> LPAREN_ENDIF ENDIF RPAREN`

### abre_endwhile

- `[abre_endwhile, LPAREN_ENDWHILE] -> LPAREN_ENDWHILE ENDWHILE RPAREN`

### abre_start

- `[abre_start, LPAREN_CMD] -> LPAREN_CMD START RPAREN`

### apos_bool

- `[apos_bool, IF] -> IF RPAREN lista_if fim_if`
- `[apos_bool, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_bool, MEMORY] -> MEMORY RPAREN`
- `[apos_bool, RPAREN] -> RPAREN`
- `[apos_bool, WHILE] -> WHILE RPAREN lista_while abre_endwhile`

### apos_bool_sub

- `[apos_bool_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_bool_sub, MEMORY] -> MEMORY RPAREN`
- `[apos_bool_sub, RPAREN] -> RPAREN`

### apos_mem

- `[apos_mem, IF] -> IF RPAREN lista_if fim_if`
- `[apos_mem, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_mem, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_mem, NUMBER] -> NUMBER resto_num`
- `[apos_mem, RPAREN] -> RPAREN`
- `[apos_mem, WHILE] -> WHILE RPAREN lista_while abre_endwhile`

### apos_mem_sub

- `[apos_mem_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_mem_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_mem_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_mem_sub, RPAREN] -> RPAREN`

### apos_num

- `[apos_num, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_num, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_num, NUMBER] -> NUMBER resto_num`
- `[apos_num, RES] -> RES RPAREN`

### apos_num_sub

- `[apos_num_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_num_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_num_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_num_sub, RES] -> RES RPAREN`

### apos_sub

- `[apos_sub, IF] -> IF RPAREN lista_if fim_if`
- `[apos_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_sub, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_sub, NUMBER] -> NUMBER resto_num`
- `[apos_sub, RPAREN] -> RPAREN`
- `[apos_sub, WHILE] -> WHILE RPAREN lista_while abre_endwhile`

### apos_sub_sub

- `[apos_sub_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_sub_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_sub_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_sub_sub, RPAREN] -> RPAREN`

### cauda_rel

- `[cauda_rel, IF] -> IF RPAREN lista_if fim_if`
- `[cauda_rel, RPAREN] -> RPAREN`
- `[cauda_rel, WHILE] -> WHILE RPAREN lista_while abre_endwhile`

### comando

- `[comando, LPAREN_CMD] -> LPAREN_CMD interior`

### fecha_end

- `[fecha_end, LPAREN_END] -> LPAREN_END END RPAREN`

### fim_if

- `[fim_if, LPAREN_ELSE] -> abre_else lista_if abre_endif`
- `[fim_if, LPAREN_ENDIF] -> abre_endif`

### interior

- `[interior, BOOL_LIT] -> BOOL_LIT apos_bool`
- `[interior, LPAREN_CMD] -> LPAREN_CMD sub apos_sub`
- `[interior, MEMORY] -> MEMORY apos_mem`
- `[interior, NUMBER] -> NUMBER apos_num`

### lista_if

- `[lista_if, LPAREN_CMD] -> comando lista_if`
- `[lista_if, LPAREN_ELSE] -> epsilon`
- `[lista_if, LPAREN_ENDIF] -> epsilon`

### lista_prog

- `[lista_prog, LPAREN_CMD] -> comando lista_prog`
- `[lista_prog, LPAREN_END] -> epsilon`

### lista_while

- `[lista_while, LPAREN_CMD] -> comando lista_while`
- `[lista_while, LPAREN_ENDWHILE] -> epsilon`

### programa

- `[programa, LPAREN_CMD] -> abre_start lista_prog fecha_end`

### resto_mem_grava

- `[resto_mem_grava, OPERATOR] -> OPERATOR RPAREN`
- `[resto_mem_grava, REL_OP] -> REL_OP cauda_rel`
- `[resto_mem_grava, RPAREN] -> RPAREN`

### resto_mem_grava_sub

- `[resto_mem_grava_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_mem_grava_sub, REL_OP] -> REL_OP RPAREN`
- `[resto_mem_grava_sub, RPAREN] -> RPAREN`

### resto_num

- `[resto_num, OPERATOR] -> OPERATOR RPAREN`
- `[resto_num, REL_OP] -> REL_OP cauda_rel`

### resto_num_sub

- `[resto_num_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_num_sub, REL_OP] -> REL_OP RPAREN`

### resto_sub

- `[resto_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_sub, REL_OP] -> REL_OP cauda_rel`

### resto_sub_sub

- `[resto_sub_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_sub_sub, REL_OP] -> REL_OP RPAREN`

### sub

- `[sub, BOOL_LIT] -> BOOL_LIT apos_bool_sub`
- `[sub, LPAREN_CMD] -> LPAREN_CMD sub apos_sub_sub`
- `[sub, MEMORY] -> MEMORY apos_mem_sub`
- `[sub, NUMBER] -> NUMBER apos_num_sub`

## Conflitos

Sem conflitos LL(1).

---

## Arvore Sintatica (ultimo teste)

```
programa [1..63]
  expressao [linha 3]
    gravar_memoria(X)
      numero(10)
  expressao [linha 4]
    gravar_memoria(Y)
      numero(3)
  expressao [linha 5]
    gravar_memoria(Z)
      numero(2.5)
  expressao [linha 7]
    gravar_memoria(SOMA)
      binaria(+)
        memoria(X)
        memoria(Y)
  expressao [linha 8]
    gravar_memoria(DIF)
      binaria(-)
        memoria(X)
        memoria(Y)
  expressao [linha 9]
    gravar_memoria(PROD)
      binaria(*)
        memoria(X)
        memoria(Y)
  expressao [linha 10]
    gravar_memoria(DIVINT)
      binaria(/)
        memoria(X)
        memoria(Y)
  expressao [linha 11]
    gravar_memoria(RESTO)
      binaria(%)
        memoria(X)
        memoria(Y)
  expressao [linha 13]
    gravar_memoria(ZSOMA)
      binaria(+)
        memoria(Z)
        numero(1.0)
  expressao [linha 14]
    gravar_memoria(ZDIV)
      binaria(|)
        memoria(Z)
        numero(2.0)
  expressao [linha 16]
    gravar_memoria(POT)
      binaria(^)
        memoria(X)
        memoria(Y)
  expressao [linha 18]
    gravar_memoria(MIX)
      binaria(+)
        memoria(X)
        memoria(Z)
  if [linha 20]
    condicao:
      relacional(>)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 21]
        gravar_memoria(RGT)
          numero(1)
    else:
      expressao [linha 23]
        gravar_memoria(RGT)
          numero(0)
  if [linha 25]
    condicao:
      relacional(<)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 26]
        gravar_memoria(RLT)
          numero(1)
    else:
      expressao [linha 28]
        gravar_memoria(RLT)
          numero(0)
  if [linha 30]
    condicao:
      relacional(>=)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 31]
        gravar_memoria(RGE)
          numero(1)
    else:
      expressao [linha 33]
        gravar_memoria(RGE)
          numero(0)
  if [linha 35]
    condicao:
      relacional(<=)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 36]
        gravar_memoria(RLE)
          numero(1)
    else:
      expressao [linha 38]
        gravar_memoria(RLE)
          numero(0)
  if [linha 40]
    condicao:
      relacional(==)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 41]
        gravar_memoria(REQ)
          numero(1)
    else:
      expressao [linha 43]
        gravar_memoria(REQ)
          numero(0)
  if [linha 45]
    condicao:
      relacional(!=)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 46]
        gravar_memoria(RNE)
          numero(1)
    else:
      expressao [linha 48]
        gravar_memoria(RNE)
          numero(0)
  while [linha 51]
    condicao:
      relacional(>)
        memoria(Y)
        numero(0)
    bloco:
      expressao [linha 52]
        gravar_memoria(Y)
          binaria(-)
            memoria(Y)
            numero(1)
  expressao [linha 55]
    res(1)
  expressao [linha 56]
    gravar_memoria(ULTIMO)
      res(1)
  expressao [linha 57]
    memoria(SOMA)
  expressao [linha 59]
    gravar_memoria(LIGADO)
      bool_literal(TRUE)
  expressao [linha 60]
    gravar_memoria(DESLIGADO)
      bool_literal(FALSE)
  expressao [linha 61]
    memoria(LIGADO)
  expressao [linha 62]
    memoria(DESLIGADO)
```
