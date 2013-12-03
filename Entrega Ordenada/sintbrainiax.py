#!/usr/bin/env python
#coding: utf8 
# Analisis Sintactico del lenguaje Brainiac.
# Modulo: SintBrainiac
# Autores:  Wilthew, Patricia    09-10910
#           Leopoldo Pimentel    06-40095

import ply.lex as lex
import ply.yacc as yacc
import sys
import funciones
import LlexBrainiax as lexer
import clases

tokens = lexer.tokens


contador = -1

def main():

    # Se abre el archivo y se guarda su contenido en el string codigo
    file_name = sys.argv[1]
    fp = open(file_name)
    codigo = fp.read()

    ####################################################
    #                    Manejo de gramática y construccion de arbol                                  #
    ####################################################



    # Definicion del símbolo inicial
    start = 'programa'

    # Precedencia de los operadores
    precedence = (
            ('left','TkDisyuncion'),
            ('left','TkConjuncion'),
            ('left','TkIgual','TkDesigual'),
            ('left','TkMenor','TkMayor','TkMayorIgual','TkMenorIgual'),
            ('left','TkMas','TkResta'),
            ('left','TkMult','TkDiv','TkMod'),
            ('left','TkConcat'),
            ('left','TkInspeccion'),
            ('left','TkAt'),
            ('right','uminus','unot'),                
        )

    # PROGRAMA
    def p_programa(p):
        ''' programa : declaracion TkExecute instlist TkDone
                          |  TkExecute instlist TkDone '''
        if len(p) == 5:
            p[0] = p[3]
        elif len(p) == 4:
            p[0] = p[2]


    # TERMINO UNARIO
    def p_term_num(p):
        ''' term : TkNum '''
        p[0] = clases.numero(p[1])
        str_ = ""
        tabs = (contador+1)*"  "


    # IDENTIFICADOR
    def p_term_ident(p):
        ''' term : TkIdent '''
        p[0] = clases.ident(p[1])
        str_ = ""
        tabs = (contador+1)*"  "


    # EXPRESION UNARIA
    def p_exp_un(p):
        ''' exp_un : TkResta exp %prec uminus
                      | TkNegacion exp %prec unot '''
        p[0] = clases.op_un(p[1],p[2])


    # EXPRESION
    def p_exp(p):
        ''' exp : term
                | TkTrue
                | TkFalse
                | exp_un
                | TkParAbre exp TkParCierra
                | TkCorcheteAbre exp TkCorcheteCierra
                | TkLlaveAbre exp TkLlaveCierra
                | exp TkMas exp 
                | exp TkMult exp
                | exp TkMod exp
                | exp TkDiv exp
                | exp TkResta exp
                | exp TkIgual exp
                | exp TkDesigual exp
                | exp TkMenor exp
                | exp TkMayor exp
                | exp TkMenorIgual exp
                | exp TkMayorIgual exp
                | exp TkConcat exp
                | exp TkInspeccion exp
                | exp TkDisyuncion exp
                | exp TkConjuncion exp
                | exp TkAt exp '''
#TkPunto
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4 and p[1] != '(' and p[1] != '[' and p[1] != '{':
            p[0] = clases.op_bin(p[1],p[3],p[2])
        else:
			p[0] = p[2]
                

    # ASIGNACION
    def p_instruccion_asignacion(p):
        ''' instruccion : TkIdent TkAsignacion exp '''
        p[0] = clases.inst_asig(p[1],p[3])


    # READ
    def p_instruccion_read(p):
        ''' instruccion : TkRead exp '''
        p[0] = clases.inst_read(p[2])


    # WRITE
    def p_instruccion_write(p):
        ''' instruccion : TkWrite exp '''
        p[0] = clases.inst_write(p[2])


    # WHILE
    def p_instruccion_while(p):
        ''' instruccion : TkWhile exp TkDo instlist TkDone '''
        p[0] = clases.inst_while(p[2],p[4])


    # FOR
    def p_instruccion_for(p):
        ''' instruccion : TkFor TkIdent TkFrom exp TkTo exp TkDo instlist TkDone'''
        p[0] = clases.inst_for(p[2],p[4],p[6],p[8])

    # IF
    def p_instruccion_if(p):
        ''' instruccion : TkIf exp TkThen instlist TkDone
			                | TkIf exp TkThen instlist TkElse instlist TkDone '''
        if len(p) == 6:
            p[0] = clases.inst_if(p[2],p[4],None)
        else:
            p[0] = clases.inst_if(p[2],p[4],p[6])


    # Gramatica del bloque de instrucciones
    def p_instruccion_bloque(p):
        ''' instruccion :  declaracion TkExecute instlist TkDone
                            | TkExecute instlist TkDone '''
        if len(p) == 4:
            p[0] = clases.inst_bloque(p[2])
        elif len(p) == 5:
            p[0] = clases.inst_bloque(p[3])


    # SECUENCIACION DE INSTRUCCIONES
    def p_instlist(p):
        '''  instlist : instlist semicoloninst 
                      | instruccion '''
        if len(p) == 2:
            p[0] = clases.inst_list()
            p[0].lista.append(p[1])
        elif len(p) == 3:
            p[0] = p[1]
            p[0].lista.append(p[2])
                
    def p_commainst(p):
        ''' semicoloninst : TkPuntoYComa instruccion '''
        p[0] = p[2]


    # DECLARACION
    def p_declaracion(p):
        ''' declaracion : TkDeclare declist '''

    def p_declist(p):
        ''' declist : dec TkPuntoYComa declist 
                    | dec '''

    def p_dec(p):
        ''' dec : varlist TkType tipo '''

    def p_varlist(p):
        '''varlist : TkIdent TkComa varlist 
                    | TkIdent '''

    def p_tipo_int(p):
        'tipo : TkInteger'

    def p_tipo_bool(p):
        'tipo : TkBoolean'

    def p_tipo_tape(p):
        'tipo : TkTape'




    #Funcion de error del parser
    def p_error(p):
        c = lexer.hallar_columna(codigo,p)
        print "Error de sintaxis en linea %s, columna %s: token \'%s\' inesperado." % (p.lineno,c,p.value)
        sys.exit(0)


    
    # Se construye la funcion del parser
    parser = yacc.yacc()


    # LOGGER

    # Set up a logging object
    import logging
    logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()

    # Se construye el árbol.
    arbol = parser.parse(codigo,debug=log)

    # Se imprime el árbol.
    print funciones.print_arbol(arbol)


if __name__ == "__main__":
    main()



