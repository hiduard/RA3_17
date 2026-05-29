# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA3 17

def gerarRotuloConstante(valor):
    rotulo = valor.replace("-", "NEG_").replace(".", "_")
    return f"CONST_{rotulo}"


def normalizarLiteralDouble(valor):
    if "." not in valor:
        return valor + ".0"
    return valor


def novoRotulo(ctx, prefixo, linha):
    ctx["contador_rotulos"] += 1
    return f"{prefixo}_{linha}_{ctx['contador_rotulos']}"

def gerarCodigoDoubleParaInt(reg_double, reg_single, reg_int):
    return [
        f"    vcvt.s32.f64 {reg_single}, {reg_double}",
        f"    vmov {reg_int}, {reg_single}",
    ]


def gerarCodigoIntParaDouble(reg_int, reg_single, reg_double):
    return [
        f"    vmov {reg_single}, {reg_int}",
        f"    vcvt.f64.s32 {reg_double}, {reg_single}",
    ]

def coletarConstantesExpressao(no, constantes):
    tipo = no["tipo"]

    if tipo == "numero":
        constantes.add(normalizarLiteralDouble(no["valor"]))
        return

    if tipo in ("carregar_memoria", "carregar_resultado"):
        return

    if tipo == "gravar_memoria":
        coletarConstantesExpressao(no["valor"], constantes)
        return

    if tipo in ("binaria", "relacional"):
        coletarConstantesExpressao(no["esquerda"], constantes)
        coletarConstantesExpressao(no["direita"], constantes)
        return


def coletarMemoriasExpressao(no, memorias):
    tipo = no["tipo"]

    if tipo == "carregar_memoria":
        memorias.add(no["nome"])
        return

    if tipo == "gravar_memoria":
        memorias.add(no["nome"])
        coletarMemoriasExpressao(no["valor"], memorias)
        return

    if tipo in ("binaria", "relacional"):
        coletarMemoriasExpressao(no["esquerda"], memorias)
        coletarMemoriasExpressao(no["direita"], memorias)
        return

    if tipo in ("numero", "carregar_resultado"):
        return


def coletarComando(comando, constantes, memorias):
    tipo = comando["tipo"]

    if tipo == "expressao":
        coletarConstantesExpressao(comando["estrutura"], constantes)
        coletarMemoriasExpressao(comando["estrutura"], memorias)
        return

    if tipo == "if":
        coletarConstantesExpressao(comando["condicao"], constantes)
        coletarMemoriasExpressao(comando["condicao"], memorias)
        for item in comando["bloco_then"]:
            coletarComando(item, constantes, memorias)
        if comando["bloco_else"] is not None:
            for item in comando["bloco_else"]:
                coletarComando(item, constantes, memorias)
        return

    if tipo == "while":
        coletarConstantesExpressao(comando["condicao"], constantes)
        coletarMemoriasExpressao(comando["condicao"], memorias)
        for item in comando["bloco"]:
            coletarComando(item, constantes, memorias)
        return


def coletarPrograma(arvore, constantes, memorias):
    for comando in arvore["comandos"]:
        coletarComando(comando, constantes, memorias)

def gerarSecaoDados(arvore):
    linhas = [".data", ".align 3"]

    constantes = {"0.0", "1.0"}
    memorias = set()

    coletarPrograma(arvore, constantes, memorias)

    for valor in sorted(constantes):
        rotulo = gerarRotuloConstante(valor)
        literal = normalizarLiteralDouble(valor)
        linhas.append(f"{rotulo}: .double {literal}")

    for nome in sorted(memorias):
        linhas.append(f"MEM_{nome}: .double 0.0")

    for numero_linha in range(1, arvore["linha_fim"] + 1):
        linhas.append(f"RESULTADO_{numero_linha}: .double 0.0")

    return linhas

def gerarCodigoNumero(no):
    valor = normalizarLiteralDouble(no["valor"])
    rotulo = gerarRotuloConstante(valor)
    return [
        f"    ldr r0, ={rotulo}",
        "    vldr d0, [r0]",
    ]


def gerarCodigoCarregarMemoria(no):
    nome = no["nome"]
    return [
        f"    ldr r0, =MEM_{nome}",
        "    vldr d0, [r0]",
    ]


def gerarInstrucaoOperador(operador):
    if operador == "+":
        return "    vadd.f64 d0, d1, d0"
    if operador == "-":
        return "    vsub.f64 d0, d1, d0"
    if operador == "*":
        return "    vmul.f64 d0, d1, d0"
    if operador == "|":
        return "    vdiv.f64 d0, d1, d0"
    return None

def gerarCodigoDivisaoInteira(esquerda, direita, linha_atual, ctx):

    lbl_divzero = novoRotulo(ctx, "DIVZERO", linha_atual)
    lbl_loop    = novoRotulo(ctx, "DIV_LOOP", linha_atual)
    lbl_fim     = novoRotulo(ctx, "DIVINT_FIM", linha_atual)
    lbl_neg     = novoRotulo(ctx, "DIVINT_NEG", linha_atual)
    lbl_end     = novoRotulo(ctx, "DIVINT_END", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")
    linhas.extend(direita)
    linhas.append("    vpop {d1}")

    linhas.extend(gerarCodigoDoubleParaInt("d1", "s2", "r4"))
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r5"))

    linhas.append("    cmp r5, #0")
    linhas.append(f"    beq {lbl_divzero}")

    linhas.append("    eor r7, r4, r5")

    linhas.append("    cmp r4, #0")
    linhas.append("    rsblt r4, r4, #0")
    linhas.append("    cmp r5, #0")
    linhas.append("    rsblt r5, r5, #0")

    linhas.append("    mov r6, #0")
    linhas.append(f"{lbl_loop}:")
    linhas.append("    cmp r4, r5")
    linhas.append(f"    blt {lbl_fim}")
    linhas.append("    sub r4, r4, r5")
    linhas.append("    add r6, r6, #1")
    linhas.append(f"    b {lbl_loop}")

    linhas.append(f"{lbl_divzero}:")
    linhas.append("    mov r6, #0")
    linhas.append(f"    b {lbl_end}")

    linhas.append(f"{lbl_fim}:")
    linhas.append("    cmp r7, #0")
    linhas.append(f"    bge {lbl_end}")
    linhas.append(f"    b {lbl_neg}")
    linhas.append(f"{lbl_neg}:")
    linhas.append("    rsb r6, r6, #0")

    linhas.append(f"{lbl_end}:")
    linhas.extend(gerarCodigoIntParaDouble("r6", "s0", "d0"))
    return linhas

def gerarCodigoRestoInteiro(esquerda, direita, linha_atual, ctx):
    lbl_divzero = novoRotulo(ctx, "RESTO_DIVZERO", linha_atual)
    lbl_loop    = novoRotulo(ctx, "RESTO_LOOP", linha_atual)
    lbl_fim     = novoRotulo(ctx, "RESTO_FIM", linha_atual)
    lbl_neg     = novoRotulo(ctx, "RESTO_NEG", linha_atual)
    lbl_end     = novoRotulo(ctx, "RESTO_END", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")
    linhas.extend(direita)
    linhas.append("    vpop {d1}")

    linhas.extend(gerarCodigoDoubleParaInt("d1", "s2", "r4"))
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r5"))

    linhas.append("    cmp r5, #0")
    linhas.append(f"    beq {lbl_divzero}")

    linhas.append("    mov r7, r4")

    linhas.append("    cmp r4, #0")
    linhas.append("    rsblt r4, r4, #0")
    linhas.append("    cmp r5, #0")
    linhas.append("    rsblt r5, r5, #0")

    linhas.append(f"{lbl_loop}:")
    linhas.append("    cmp r4, r5")
    linhas.append(f"    blt {lbl_fim}")
    linhas.append("    sub r4, r4, r5")
    linhas.append(f"    b {lbl_loop}")

    linhas.append(f"{lbl_divzero}:")
    linhas.append("    mov r4, #0")
    linhas.append(f"    b {lbl_end}")

    linhas.append(f"{lbl_fim}:")
    linhas.append("    cmp r7, #0")
    linhas.append(f"    bge {lbl_end}")
    linhas.append(f"    b {lbl_neg}")
    linhas.append(f"{lbl_neg}:")
    linhas.append("    rsb r4, r4, #0")

    linhas.append(f"{lbl_end}:")
    linhas.extend(gerarCodigoIntParaDouble("r4", "s0", "d0"))
    return linhas

def gerarCodigoPotencia(esquerda, direita, linha_atual, ctx):
    lbl_loop = novoRotulo(ctx, "POT_LOOP", linha_atual)
    lbl_fim  = novoRotulo(ctx, "POT_FIM", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")         

    linhas.extend(direita)
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r4"))  

    linhas.append("    vpop {d2}")           
    linhas.append("    ldr r0, =CONST_1_0")
    linhas.append("    vldr d0, [r0]")       

    linhas.append("    cmp r4, #0")
    linhas.append(f"    ble {lbl_fim}")       

    linhas.append(f"{lbl_loop}:")
    linhas.append("    vmul.f64 d0, d0, d2")
    linhas.append("    subs r4, r4, #1")
    linhas.append(f"    bne {lbl_loop}")

    linhas.append(f"{lbl_fim}:")
    return linhas

def gerarCodigoRelacionalComoBoolean(no, linha_atual, ctx):
    lbl_true = novoRotulo(ctx, "REL_TRUE", linha_atual)
    lbl_fim  = novoRotulo(ctx, "REL_FIM", linha_atual)

    linhas = []
    linhas.extend(gerarCodigoNo(no["esquerda"], linha_atual, ctx))
    linhas.append("    vpush {d0}")
    linhas.extend(gerarCodigoNo(no["direita"], linha_atual, ctx))
    linhas.append("    vpop {d1}")
    linhas.append("    vcmp.f64 d1, d0")
    linhas.append("    vmrs APSR_nzcv, fpscr")

    operador = no["operador"]

    if operador == "==":
        linhas.append(f"    beq {lbl_true}")
    elif operador == "!=":
        linhas.append(f"    bne {lbl_true}")
    elif operador == ">":
        linhas.append(f"    bgt {lbl_true}")
    elif operador == "<":
        linhas.append(f"    blt {lbl_true}")
    elif operador == ">=":
        linhas.append(f"    bge {lbl_true}")
    elif operador == "<=":
        linhas.append(f"    ble {lbl_true}")
    else:
        raise ValueError(f"Operador relacional nao suportado: {operador}")

    linhas.append("    ldr r0, =CONST_0_0")
    linhas.append("    vldr d0, [r0]")
    linhas.append(f"    b {lbl_fim}")

    linhas.append(f"{lbl_true}:")
    linhas.append("    ldr r0, =CONST_1_0")
    linhas.append("    vldr d0, [r0]")

    linhas.append(f"{lbl_fim}:")
    return linhas



def gerarCodigoCondicao(no, label_false, linha_atual, ctx):
    linhas = []

    # Condicao direta: variavel bool ou literal bool (sem operador relacional)
    if no["tipo"] in ("carregar_memoria", "bool_literal"):
        linhas.extend(gerarCodigoNo(no, linha_atual, ctx))
        linhas.append("    ldr r1, =CONST_0_0")
        linhas.append("    vldr d1, [r1]")
        linhas.append("    vcmp.f64 d0, d1")
        linhas.append("    vmrs APSR_nzcv, fpscr")
        linhas.append(f"    beq {label_false}")
        return linhas

    linhas.extend(gerarCodigoNo(no["esquerda"], linha_atual, ctx))
    linhas.append("    vpush {d0}")
    linhas.extend(gerarCodigoNo(no["direita"], linha_atual, ctx))
    linhas.append("    vpop {d1}")
    linhas.append("    vcmp.f64 d1, d0")
    linhas.append("    vmrs APSR_nzcv, fpscr")

    operador = no["operador"]

    # Branch para false: inverte a condicao
    if operador == "==":
        linhas.append(f"    bne {label_false}")
    elif operador == "!=":
        linhas.append(f"    beq {label_false}")
    elif operador == ">":
        linhas.append(f"    ble {label_false}")
    elif operador == "<":
        linhas.append(f"    bge {label_false}")
    elif operador == ">=":
        linhas.append(f"    blt {label_false}")
    elif operador == "<=":
        linhas.append(f"    bgt {label_false}")
    else:
        raise ValueError(f"Operador relacional nao suportado: {operador}")

    return linhas


def gerarCodigoBoolLiteral(no):
    linhas = []
    if no["valor"] == "TRUE":
        linhas.append("    ldr r0, =CONST_1_0")
    else:
        linhas.append("    ldr r0, =CONST_0_0")
    linhas.append("    vldr d0, [r0]")
    return linhas


def gerarCodigoNo(no, linha_atual, ctx):
    tipo = no["tipo"]

    if tipo == "numero":
        return gerarCodigoNumero(no)

    if tipo == "bool_literal":          
        return gerarCodigoBoolLiteral(no)

    if tipo == "carregar_memoria":
        return gerarCodigoCarregarMemoria(no)

    if tipo == "gravar_memoria":
        linhas = []
        linhas.extend(gerarCodigoNo(no["valor"], linha_atual, ctx))
        linhas.append(f"    ldr r0, =MEM_{no['nome']}")
        linhas.append("    vstr d0, [r0]")
        return linhas

    if tipo == "carregar_resultado":
        deslocamento = int(no["indice"])

        if "linha_resultado" in no:
            linha_destino = int(no["linha_resultado"])
        else:
            if deslocamento == 0:
                raise ValueError(
                    f"RES 0 invalido na linha {linha_atual}: "
                    "nao e possivel referenciar o resultado da linha atual"
                )

            linha_destino = linha_atual - deslocamento

            if linha_destino < 1:
                raise ValueError(
                    f"RES {deslocamento} invalido na linha {linha_atual}: "
                    f"aponta para linha {linha_destino}, que nao existe"
                )

        return [
            f"    ldr r0, =RESULTADO_{linha_destino}",
            "    vldr d0, [r0]",
        ]
    
    if tipo == "relacional":
        return gerarCodigoRelacionalComoBoolean(no, linha_atual, ctx)
    
    if tipo == "binaria":
        operador = no["operador"]

        if operador in ["+", "-", "*", "|"]:
            instrucao = gerarInstrucaoOperador(operador)
            linhas = []
            linhas.extend(gerarCodigoNo(no["esquerda"], linha_atual, ctx))
            linhas.append("    vpush {d0}")
            linhas.extend(gerarCodigoNo(no["direita"], linha_atual, ctx))
            linhas.append("    vpop {d1}")
            linhas.append(instrucao)
            return linhas
        
        if operador == "/":
            return gerarCodigoDivisaoInteira(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )

        if operador == "%":
            return gerarCodigoRestoInteiro(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )
        
        if operador == "^":
            return gerarCodigoPotencia(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )
        raise ValueError(f"Operador binario ainda nao implementado: {operador}")
    raise ValueError(f"No nao suportado ainda: {tipo}")


def gerarCodigoComando(comando, ctx):
    linhas = []
    tipo = comando["tipo"]

    if tipo == "expressao":
        linhas.append("")
        linhas.append(f"    @ Linha {comando['linha']}")
        linhas.append(f"    @ Fonte: {comando['fonte']}")

        codigo = gerarCodigoNo(comando["estrutura"], comando["linha"], ctx)
        linhas.extend(codigo)
        linhas.append(f"    ldr r0, =RESULTADO_{comando['linha']}")
        linhas.append("    vstr d0, [r0]")
        return linhas
    if tipo == "if":
        lbl_else = novoRotulo(ctx, "IF_ELSE", comando["linha"])
        lbl_fim = novoRotulo(ctx, "IF_FIM", comando["linha"])

        linhas.append("")
        linhas.append(f"    @ IF linha {comando['linha']}")
        linhas.append(f"    @ Fonte: {comando['fonte']}")

        if comando["bloco_else"] is None:
            linhas.extend(
                gerarCodigoCondicao(comando["condicao"], lbl_fim, comando["linha"], ctx)
            )

            for item in comando["bloco_then"]:
                linhas.extend(gerarCodigoComando(item, ctx))

            linhas.append(f"{lbl_fim}:")
            return linhas
        linhas.extend(
            gerarCodigoCondicao(comando["condicao"], lbl_else, comando["linha"], ctx)
        )

        for item in comando["bloco_then"]:

            linhas.extend(gerarCodigoComando(item, ctx))
        linhas.append(f"    b {lbl_fim}")
        linhas.append(f"{lbl_else}:")

        for item in comando["bloco_else"]:
            linhas.extend(gerarCodigoComando(item, ctx))

        linhas.append(f"{lbl_fim}:")
        return linhas
    
    if tipo == "while":
        lbl_inicio = novoRotulo(ctx, "WHILE_INICIO", comando["linha"])
        lbl_fim = novoRotulo(ctx, "WHILE_FIM", comando["linha"])

        linhas.append("")
        linhas.append(f"    @ WHILE linha {comando['linha']}")
        linhas.append(f"    @ Fonte: {comando['fonte']}")
        linhas.append(f"{lbl_inicio}:")

        linhas.extend(
            gerarCodigoCondicao(comando["condicao"], lbl_fim, comando["linha"], ctx)
        )

        for item in comando["bloco"]:
            linhas.extend(gerarCodigoComando(item, ctx))

        linhas.append(f"    b {lbl_inicio}") 
        linhas.append(f"{lbl_fim}:")
        return linhas

    raise ValueError(f"Comando nao suportado ainda: {tipo}")


def gerarStringsUART(memorias):
    linhas = []
    linhas.append("@ Strings para impressao no JTAG UART")
    for nome in sorted(memorias):
        linhas.append(f'STR_{nome}: .asciz "{nome}="')
    linhas.append('STR_NL: .asciz "\\n"')
    linhas.append('STR_PONTO: .asciz "."')
    linhas.append('STR_MENOS: .asciz "-"')
    linhas.append("PRINT_BUF: .space 12")
    return linhas


def gerarBlocoImpressaoUART(memorias):
    linhas = []
    linhas.append("")
    linhas.append("@ ============================================================")
    linhas.append("@ Impressao dos resultados no JTAG UART")
    linhas.append("@ ============================================================")
    for nome in sorted(memorias):
        linhas.append(f"    @ Imprime {nome}")
        linhas.append(f"    ldr r1, =STR_{nome}")
        linhas.append("    bl print_str")
        linhas.append(f"    ldr r0, =MEM_{nome}")
        linhas.append("    vldr d0, [r0]")
        linhas.append("    bl print_double")
        linhas.append("    ldr r1, =STR_NL")
        linhas.append("    bl print_str")
    return linhas


SUBROTINAS_UART = """
@ ============================================================
@ Subrotinas de impressao no JTAG UART (0xFF201000)
@ Polling correto: verifica espaco na FIFO de escrita antes
@ ============================================================

@ print_char: imprime caractere em r2 (espera FIFO ter espaco)
print_char:
    push {r0, r3, lr}
    ldr r0, =0xFF201000
pc_wait:
    ldr r3, [r0, #4]
    lsr r3, r3, #16
    cmp r3, #0
    beq pc_wait
    str r2, [r0]
    pop {r0, r3, lr}
    bx lr

@ print_str: imprime string em r1
print_str:
    push {r2, lr}
ps_loop:
    ldrb r2, [r1], #1
    cmp r2, #0
    beq ps_ret
    bl print_char
    b ps_loop
ps_ret:
    pop {r2, lr}
    bx lr

@ print_int: imprime inteiro em r1
print_int:
    push {r4, r5, r6, r7, lr}
    mov r4, r1
    ldr r6, =PRINT_BUF
    add r6, r6, #11
    mov r7, #0
    strb r7, [r6]
    cmp r4, #0
    bge pi_conv
    ldr r1, =STR_MENOS
    bl print_str
    rsb r4, r4, #0
pi_conv:
    sub r6, r6, #1
    mov r7, r4
    mov r4, #0
pi_d10:
    cmp r7, #10
    blt pi_d10d
    sub r7, r7, #10
    add r4, r4, #1
    b pi_d10
pi_d10d:
    add r7, r7, #48
    strb r7, [r6]
    cmp r4, #0
    bne pi_conv
pi_imp:
    ldrb r2, [r6], #1
    cmp r2, #0
    beq pi_fim
    bl print_char
    b pi_imp
pi_fim:
    pop {r4, r5, r6, r7, lr}
    bx lr

@ print_double: imprime double em d0 com 2 casas decimais
print_double:
    push {r4, r5, lr}
    vmov r4, r5, d0
    tst r5, #0x80000000
    beq pd_pos
    ldr r1, =STR_MENOS
    bl print_str
    vneg.f64 d0, d0
pd_pos:
    vcvt.s32.f64 s0, d0
    vmov r1, s0
    bl print_int
    ldr r1, =STR_PONTO
    bl print_str
    vcvt.f64.s32 d1, s0
    vsub.f64 d0, d0, d1
    ldr r4, =CONST_10_0
    vldr d2, [r4]
    vmul.f64 d0, d0, d2
    vmul.f64 d0, d0, d2
    vcvt.s32.f64 s0, d0
    vmov r1, s0
    cmp r1, #10
    bge pd_2d
    mov r2, #48
    bl print_char
pd_2d:
    bl print_int
    pop {r4, r5, lr}
    bx lr
"""


def gerarAssembly(arvore):
    ctx = {"contador_rotulos": 0}

    constantes = {"0.0", "1.0", "10.0"}
    memorias = set()
    coletarPrograma(arvore, constantes, memorias)

    # secao .data
    linhas = [".data", ".align 3"]
    for valor in sorted(constantes):
        rotulo = gerarRotuloConstante(valor)
        literal = normalizarLiteralDouble(valor)
        linhas.append(f"{rotulo}: .double {literal}")
    for nome in sorted(memorias):
        linhas.append(f"MEM_{nome}: .double 0.0")
    for numero_linha in range(1, arvore["linha_fim"] + 1):
        linhas.append(f"RESULTADO_{numero_linha}: .double 0.0")
    linhas.append("")
    linhas.extend(gerarStringsUART(memorias))

    linhas.append("")
    linhas.append(".text")
    linhas.append(".global _start")
    linhas.append("_start:")

    for comando in arvore["comandos"]:
        linhas.extend(gerarCodigoComando(comando, ctx))

    linhas.extend(gerarBlocoImpressaoUART(memorias))

    linhas.append("")
    linhas.append("    b fim")
    linhas.append(SUBROTINAS_UART)
    linhas.append("")
    linhas.append("fim:")
    linhas.append("    b fim")

    return "\n".join(linhas)