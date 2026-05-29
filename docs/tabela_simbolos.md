# Tabela de Simbolos

Gerada pelo Analisador Semantico — Fase 3.

| Variavel | Tipo | Linha de Definicao | Linha de Ultimo Uso |
|----------|------|-------------------|---------------------|
| `DESLIGADO` | `bool` | 60 | 62 |
| `DIF` | `int` | 8 | 8 |
| `DIVINT` | `int` | 10 | 10 |
| `LIGADO` | `bool` | 59 | 61 |
| `MIX` | `real` | 18 | 18 |
| `POT` | `int` | 16 | 16 |
| `PROD` | `int` | 9 | 9 |
| `REQ` | `int` | 41 | 43 |
| `RESTO` | `int` | 11 | 11 |
| `RGE` | `int` | 31 | 33 |
| `RGT` | `int` | 21 | 23 |
| `RLE` | `int` | 36 | 38 |
| `RLT` | `int` | 26 | 28 |
| `RNE` | `int` | 46 | 48 |
| `SOMA` | `int` | 7 | 57 |
| `ULTIMO` | `int` | 56 | 56 |
| `X` | `int` | 3 | 45 |
| `Y` | `int` | 4 | 52 |
| `Z` | `real` | 5 | 18 |
| `ZDIV` | `real` | 14 | 14 |
| `ZSOMA` | `real` | 13 | 13 |

## Notas

- **Tipo `int`**: variavel definida com literal inteiro (sem ponto decimal).
- **Tipo `real`**: variavel definida com literal real (com ponto decimal) ou promovida por operacao int+real.
- **Tipo `bool`**: variavel definida como resultado de operacao relacional.
- **Tipo `desconhecido`**: tipo nao pode ser inferido estaticamente.
- **Linha de Definicao**: primeira linha em que `(V MEM)` foi executado para esta variavel.
- **Linha de Ultimo Uso**: ultima linha em que a variavel foi lida `(MEM)` ou redefinida.
