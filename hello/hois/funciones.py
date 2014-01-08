#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ply.lex as lex
import ply.yacc as yacc
import sys

#
# Función que encuentra la columna dado un string de input y un token
#
def find_column(input,token):
        aux = input.rfind('\n',0,token.lexpos)
        # Si es el primer token de la primera línea, su posición es 1
        if aux < 0 and token.lexpos == 0:         
                aux = 0
                return 1
        column = (token.lexpos - aux)
        return column

#
# Funcion que verifica la entrada al programa 
#        
def process_input():
        if len(sys.argv) != 2:
                print "Cantidad incorrecta de argumentos"
                sys.exit(0)

#
# Funcion que abre el archivo de entrada
#        
def open_file(t):
        try:
                fent = open(t,'r')
        except IOError as e:
                print "No se encuentra el archivo: ".format(e.errno, e.strerror)
                sys.exit(0)
        return fent

#
# Funcion que verifica si un entero es de 32 bits.
#        
def num_valid(n):
        try:
                bitstring=bin(n)
        except (TypeError, ValueError):
                return False
        if len(bin(n)[2:]) <=32:
                return True
        else:
                return False
                
#
# Funcion que imrpime un arbol sintactico abstracto.
#        
def print_arbol(arb):
        str_ = ""
        str_ = str(arb)
        str_ = str_[:len(str_)-1]
        return str_

	

	
def find_column_parser(input,lexpos):
        aux = input.rfind('\n',0,lexpos)
        # Si es el primer token de la primera línea, su posición es 1
        if aux < 0 and lexpos == 0:         
                aux = 0
                return 1
        column = (lexpos - aux)
        return column
