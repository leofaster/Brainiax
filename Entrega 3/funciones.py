#!/usr/bin/env python
#coding: utf8 
# Analisis Sintactico del lenguaje Brainiac.
# Modulo: funciones
# Autores:  Wilthew, Patricia    09-10910
#           Leopoldo Pimentel    06-40095

# Funcion que imprime un arbol sintactico abstracto  
def print_arbol(arb):
        str_ = ""
        str_ = str(arb)
        str_ = str_[:len(str_)-1]
        return str_

# Funcion que halla la columna donde se encuentra un token dado
def hallar_columna(input, t):
        inicio = input.rfind('\n',0,t.lexpos)
        # Si es el primer token de la primera linea, su posicion es 1
        if inicio < 0 and t.lexpos == 0:         
            inicio = 0
            return 1
        column = (t.lexpos - inicio)
        return column
def find_column_parser(input,lexpos):
        aux = input.rfind('\n',0,lexpos)
        # Si es el primer token de la primera línea, su posición es 1
        if aux < 0 and lexpos == 0:         
                aux = 0
                return 1
        column = (lexpos - aux)
        return column
