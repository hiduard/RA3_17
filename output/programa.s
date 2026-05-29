.data
.align 3
CONST_0_0: .double 0.0
CONST_1_0: .double 1.0
CONST_10_0: .double 10.0
CONST_2_0: .double 2.0
CONST_2_5: .double 2.5
CONST_3_0: .double 3.0
MEM_DESLIGADO: .double 0.0
MEM_DIF: .double 0.0
MEM_DIVINT: .double 0.0
MEM_LIGADO: .double 0.0
MEM_MIX: .double 0.0
MEM_POT: .double 0.0
MEM_PROD: .double 0.0
MEM_REQ: .double 0.0
MEM_RESTO: .double 0.0
MEM_RGE: .double 0.0
MEM_RGT: .double 0.0
MEM_RLE: .double 0.0
MEM_RLT: .double 0.0
MEM_RNE: .double 0.0
MEM_SOMA: .double 0.0
MEM_ULTIMO: .double 0.0
MEM_X: .double 0.0
MEM_Y: .double 0.0
MEM_Z: .double 0.0
MEM_ZDIV: .double 0.0
MEM_ZSOMA: .double 0.0
RESULTADO_1: .double 0.0
RESULTADO_2: .double 0.0
RESULTADO_3: .double 0.0
RESULTADO_4: .double 0.0
RESULTADO_5: .double 0.0
RESULTADO_6: .double 0.0
RESULTADO_7: .double 0.0
RESULTADO_8: .double 0.0
RESULTADO_9: .double 0.0
RESULTADO_10: .double 0.0
RESULTADO_11: .double 0.0
RESULTADO_12: .double 0.0
RESULTADO_13: .double 0.0
RESULTADO_14: .double 0.0
RESULTADO_15: .double 0.0
RESULTADO_16: .double 0.0
RESULTADO_17: .double 0.0
RESULTADO_18: .double 0.0
RESULTADO_19: .double 0.0
RESULTADO_20: .double 0.0
RESULTADO_21: .double 0.0
RESULTADO_22: .double 0.0
RESULTADO_23: .double 0.0
RESULTADO_24: .double 0.0
RESULTADO_25: .double 0.0
RESULTADO_26: .double 0.0
RESULTADO_27: .double 0.0
RESULTADO_28: .double 0.0
RESULTADO_29: .double 0.0
RESULTADO_30: .double 0.0
RESULTADO_31: .double 0.0
RESULTADO_32: .double 0.0
RESULTADO_33: .double 0.0
RESULTADO_34: .double 0.0
RESULTADO_35: .double 0.0
RESULTADO_36: .double 0.0
RESULTADO_37: .double 0.0
RESULTADO_38: .double 0.0
RESULTADO_39: .double 0.0
RESULTADO_40: .double 0.0
RESULTADO_41: .double 0.0
RESULTADO_42: .double 0.0
RESULTADO_43: .double 0.0
RESULTADO_44: .double 0.0
RESULTADO_45: .double 0.0
RESULTADO_46: .double 0.0
RESULTADO_47: .double 0.0
RESULTADO_48: .double 0.0
RESULTADO_49: .double 0.0
RESULTADO_50: .double 0.0
RESULTADO_51: .double 0.0
RESULTADO_52: .double 0.0
RESULTADO_53: .double 0.0
RESULTADO_54: .double 0.0
RESULTADO_55: .double 0.0
RESULTADO_56: .double 0.0
RESULTADO_57: .double 0.0
RESULTADO_58: .double 0.0
RESULTADO_59: .double 0.0
RESULTADO_60: .double 0.0
RESULTADO_61: .double 0.0
RESULTADO_62: .double 0.0
RESULTADO_63: .double 0.0

@ Strings para impressao no JTAG UART
STR_DESLIGADO: .asciz "DESLIGADO="
STR_DIF: .asciz "DIF="
STR_DIVINT: .asciz "DIVINT="
STR_LIGADO: .asciz "LIGADO="
STR_MIX: .asciz "MIX="
STR_POT: .asciz "POT="
STR_PROD: .asciz "PROD="
STR_REQ: .asciz "REQ="
STR_RESTO: .asciz "RESTO="
STR_RGE: .asciz "RGE="
STR_RGT: .asciz "RGT="
STR_RLE: .asciz "RLE="
STR_RLT: .asciz "RLT="
STR_RNE: .asciz "RNE="
STR_SOMA: .asciz "SOMA="
STR_ULTIMO: .asciz "ULTIMO="
STR_X: .asciz "X="
STR_Y: .asciz "Y="
STR_Z: .asciz "Z="
STR_ZDIV: .asciz "ZDIV="
STR_ZSOMA: .asciz "ZSOMA="
STR_NL: .asciz "\n"
STR_PONTO: .asciz "."
STR_MENOS: .asciz "-"
PRINT_BUF: .space 12

.text
.global _start
_start:

    @ Linha 3
    @ Fonte: (10 X)
    ldr r0, =CONST_10_0
    vldr d0, [r0]
    ldr r0, =MEM_X
    vstr d0, [r0]
    ldr r0, =RESULTADO_3
    vstr d0, [r0]

    @ Linha 4
    @ Fonte: (3 Y)
    ldr r0, =CONST_3_0
    vldr d0, [r0]
    ldr r0, =MEM_Y
    vstr d0, [r0]
    ldr r0, =RESULTADO_4
    vstr d0, [r0]

    @ Linha 5
    @ Fonte: (2.5 Z)
    ldr r0, =CONST_2_5
    vldr d0, [r0]
    ldr r0, =MEM_Z
    vstr d0, [r0]
    ldr r0, =RESULTADO_5
    vstr d0, [r0]

    @ Linha 7
    @ Fonte: (((X) (Y) +) SOMA)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =MEM_SOMA
    vstr d0, [r0]
    ldr r0, =RESULTADO_7
    vstr d0, [r0]

    @ Linha 8
    @ Fonte: (((X) (Y) -) DIF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vsub.f64 d0, d1, d0
    ldr r0, =MEM_DIF
    vstr d0, [r0]
    ldr r0, =RESULTADO_8
    vstr d0, [r0]

    @ Linha 9
    @ Fonte: (((X) (Y) *) PROD)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vmul.f64 d0, d1, d0
    ldr r0, =MEM_PROD
    vstr d0, [r0]
    ldr r0, =RESULTADO_9
    vstr d0, [r0]

    @ Linha 10
    @ Fonte: (((X) (Y) /) DIVINT)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r4, s2
    vcvt.s32.f64 s0, d0
    vmov r5, s0
    cmp r5, #0
    beq DIVZERO_10_1
    eor r7, r4, r5
    cmp r4, #0
    rsblt r4, r4, #0
    cmp r5, #0
    rsblt r5, r5, #0
    mov r6, #0
DIV_LOOP_10_2:
    cmp r4, r5
    blt DIVINT_FIM_10_3
    sub r4, r4, r5
    add r6, r6, #1
    b DIV_LOOP_10_2
DIVZERO_10_1:
    mov r6, #0
    b DIVINT_END_10_5
DIVINT_FIM_10_3:
    cmp r7, #0
    bge DIVINT_END_10_5
    b DIVINT_NEG_10_4
DIVINT_NEG_10_4:
    rsb r6, r6, #0
DIVINT_END_10_5:
    vmov s0, r6
    vcvt.f64.s32 d0, s0
    ldr r0, =MEM_DIVINT
    vstr d0, [r0]
    ldr r0, =RESULTADO_10
    vstr d0, [r0]

    @ Linha 11
    @ Fonte: (((X) (Y) %) RESTO)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r4, s2
    vcvt.s32.f64 s0, d0
    vmov r5, s0
    cmp r5, #0
    beq RESTO_DIVZERO_11_6
    mov r7, r4
    cmp r4, #0
    rsblt r4, r4, #0
    cmp r5, #0
    rsblt r5, r5, #0
RESTO_LOOP_11_7:
    cmp r4, r5
    blt RESTO_FIM_11_8
    sub r4, r4, r5
    b RESTO_LOOP_11_7
RESTO_DIVZERO_11_6:
    mov r4, #0
    b RESTO_END_11_10
RESTO_FIM_11_8:
    cmp r7, #0
    bge RESTO_END_11_10
    b RESTO_NEG_11_9
RESTO_NEG_11_9:
    rsb r4, r4, #0
RESTO_END_11_10:
    vmov s0, r4
    vcvt.f64.s32 d0, s0
    ldr r0, =MEM_RESTO
    vstr d0, [r0]
    ldr r0, =RESULTADO_11
    vstr d0, [r0]

    @ Linha 13
    @ Fonte: (((Z) 1.0 +) ZSOMA)
    ldr r0, =MEM_Z
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =MEM_ZSOMA
    vstr d0, [r0]
    ldr r0, =RESULTADO_13
    vstr d0, [r0]

    @ Linha 14
    @ Fonte: (((Z) 2.0 |) ZDIV)
    ldr r0, =MEM_Z
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_2_0
    vldr d0, [r0]
    vpop {d1}
    vdiv.f64 d0, d1, d0
    ldr r0, =MEM_ZDIV
    vstr d0, [r0]
    ldr r0, =RESULTADO_14
    vstr d0, [r0]

    @ Linha 16
    @ Fonte: (((X)  (Y) ^) POT)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vcvt.s32.f64 s0, d0
    vmov r4, s0
    vpop {d2}
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    cmp r4, #0
    ble POT_FIM_16_12
POT_LOOP_16_11:
    vmul.f64 d0, d0, d2
    subs r4, r4, #1
    bne POT_LOOP_16_11
POT_FIM_16_12:
    ldr r0, =MEM_POT
    vstr d0, [r0]
    ldr r0, =RESULTADO_16
    vstr d0, [r0]

    @ Linha 18
    @ Fonte: (((X) (Z) +) MIX)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Z
    vldr d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =MEM_MIX
    vstr d0, [r0]
    ldr r0, =RESULTADO_18
    vstr d0, [r0]

    @ IF linha 20
    @ Fonte: ((X) (Y) > IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    ble IF_ELSE_20_13

    @ Linha 21
    @ Fonte: (1 RGT)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_RGT
    vstr d0, [r0]
    ldr r0, =RESULTADO_21
    vstr d0, [r0]
    b IF_FIM_20_14
IF_ELSE_20_13:

    @ Linha 23
    @ Fonte: (0 RGT)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_RGT
    vstr d0, [r0]
    ldr r0, =RESULTADO_23
    vstr d0, [r0]
IF_FIM_20_14:

    @ IF linha 25
    @ Fonte: ((X) (Y) < IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    bge IF_ELSE_25_15

    @ Linha 26
    @ Fonte: (1 RLT)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_RLT
    vstr d0, [r0]
    ldr r0, =RESULTADO_26
    vstr d0, [r0]
    b IF_FIM_25_16
IF_ELSE_25_15:

    @ Linha 28
    @ Fonte: (0 RLT)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_RLT
    vstr d0, [r0]
    ldr r0, =RESULTADO_28
    vstr d0, [r0]
IF_FIM_25_16:

    @ IF linha 30
    @ Fonte: ((X) (Y) >= IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    blt IF_ELSE_30_17

    @ Linha 31
    @ Fonte: (1 RGE)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_RGE
    vstr d0, [r0]
    ldr r0, =RESULTADO_31
    vstr d0, [r0]
    b IF_FIM_30_18
IF_ELSE_30_17:

    @ Linha 33
    @ Fonte: (0 RGE)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_RGE
    vstr d0, [r0]
    ldr r0, =RESULTADO_33
    vstr d0, [r0]
IF_FIM_30_18:

    @ IF linha 35
    @ Fonte: ((X) (Y) <= IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    bgt IF_ELSE_35_19

    @ Linha 36
    @ Fonte: (1 RLE)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_RLE
    vstr d0, [r0]
    ldr r0, =RESULTADO_36
    vstr d0, [r0]
    b IF_FIM_35_20
IF_ELSE_35_19:

    @ Linha 38
    @ Fonte: (0 RLE)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_RLE
    vstr d0, [r0]
    ldr r0, =RESULTADO_38
    vstr d0, [r0]
IF_FIM_35_20:

    @ IF linha 40
    @ Fonte: ((X) (Y) == IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    bne IF_ELSE_40_21

    @ Linha 41
    @ Fonte: (1 REQ)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_REQ
    vstr d0, [r0]
    ldr r0, =RESULTADO_41
    vstr d0, [r0]
    b IF_FIM_40_22
IF_ELSE_40_21:

    @ Linha 43
    @ Fonte: (0 REQ)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_REQ
    vstr d0, [r0]
    ldr r0, =RESULTADO_43
    vstr d0, [r0]
IF_FIM_40_22:

    @ IF linha 45
    @ Fonte: ((X) (Y) != IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    beq IF_ELSE_45_23

    @ Linha 46
    @ Fonte: (1 RNE)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_RNE
    vstr d0, [r0]
    ldr r0, =RESULTADO_46
    vstr d0, [r0]
    b IF_FIM_45_24
IF_ELSE_45_23:

    @ Linha 48
    @ Fonte: (0 RNE)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_RNE
    vstr d0, [r0]
    ldr r0, =RESULTADO_48
    vstr d0, [r0]
IF_FIM_45_24:

    @ WHILE linha 51
    @ Fonte: ((Y) 0 > WHILE)
WHILE_INICIO_51_25:
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    ble WHILE_FIM_51_26

    @ Linha 52
    @ Fonte: (((Y) 1 -) Y)
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    vpop {d1}
    vsub.f64 d0, d1, d0
    ldr r0, =MEM_Y
    vstr d0, [r0]
    ldr r0, =RESULTADO_52
    vstr d0, [r0]
    b WHILE_INICIO_51_25
WHILE_FIM_51_26:

    @ Linha 55
    @ Fonte: (1 RES)
    ldr r0, =RESULTADO_52
    vldr d0, [r0]
    ldr r0, =RESULTADO_55
    vstr d0, [r0]

    @ Linha 56
    @ Fonte: ((1 RES) ULTIMO)
    ldr r0, =RESULTADO_55
    vldr d0, [r0]
    ldr r0, =MEM_ULTIMO
    vstr d0, [r0]
    ldr r0, =RESULTADO_56
    vstr d0, [r0]

    @ Linha 57
    @ Fonte: (SOMA)
    ldr r0, =MEM_SOMA
    vldr d0, [r0]
    ldr r0, =RESULTADO_57
    vstr d0, [r0]

    @ Linha 59
    @ Fonte: (TRUE LIGADO)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_LIGADO
    vstr d0, [r0]
    ldr r0, =RESULTADO_59
    vstr d0, [r0]

    @ Linha 60
    @ Fonte: (FALSE DESLIGADO)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_DESLIGADO
    vstr d0, [r0]
    ldr r0, =RESULTADO_60
    vstr d0, [r0]

    @ Linha 61
    @ Fonte: (LIGADO)
    ldr r0, =MEM_LIGADO
    vldr d0, [r0]
    ldr r0, =RESULTADO_61
    vstr d0, [r0]

    @ Linha 62
    @ Fonte: (DESLIGADO)
    ldr r0, =MEM_DESLIGADO
    vldr d0, [r0]
    ldr r0, =RESULTADO_62
    vstr d0, [r0]

@ ============================================================
@ Impressao dos resultados no JTAG UART
@ ============================================================
    @ Imprime DESLIGADO
    ldr r1, =STR_DESLIGADO
    bl print_str
    ldr r0, =MEM_DESLIGADO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime DIF
    ldr r1, =STR_DIF
    bl print_str
    ldr r0, =MEM_DIF
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime DIVINT
    ldr r1, =STR_DIVINT
    bl print_str
    ldr r0, =MEM_DIVINT
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime LIGADO
    ldr r1, =STR_LIGADO
    bl print_str
    ldr r0, =MEM_LIGADO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime MIX
    ldr r1, =STR_MIX
    bl print_str
    ldr r0, =MEM_MIX
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime POT
    ldr r1, =STR_POT
    bl print_str
    ldr r0, =MEM_POT
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime PROD
    ldr r1, =STR_PROD
    bl print_str
    ldr r0, =MEM_PROD
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime REQ
    ldr r1, =STR_REQ
    bl print_str
    ldr r0, =MEM_REQ
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RESTO
    ldr r1, =STR_RESTO
    bl print_str
    ldr r0, =MEM_RESTO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RGE
    ldr r1, =STR_RGE
    bl print_str
    ldr r0, =MEM_RGE
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RGT
    ldr r1, =STR_RGT
    bl print_str
    ldr r0, =MEM_RGT
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RLE
    ldr r1, =STR_RLE
    bl print_str
    ldr r0, =MEM_RLE
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RLT
    ldr r1, =STR_RLT
    bl print_str
    ldr r0, =MEM_RLT
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RNE
    ldr r1, =STR_RNE
    bl print_str
    ldr r0, =MEM_RNE
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime SOMA
    ldr r1, =STR_SOMA
    bl print_str
    ldr r0, =MEM_SOMA
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime ULTIMO
    ldr r1, =STR_ULTIMO
    bl print_str
    ldr r0, =MEM_ULTIMO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime X
    ldr r1, =STR_X
    bl print_str
    ldr r0, =MEM_X
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime Y
    ldr r1, =STR_Y
    bl print_str
    ldr r0, =MEM_Y
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime Z
    ldr r1, =STR_Z
    bl print_str
    ldr r0, =MEM_Z
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime ZDIV
    ldr r1, =STR_ZDIV
    bl print_str
    ldr r0, =MEM_ZDIV
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime ZSOMA
    ldr r1, =STR_ZSOMA
    bl print_str
    ldr r0, =MEM_ZSOMA
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str

    b fim

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


fim:
    b fim