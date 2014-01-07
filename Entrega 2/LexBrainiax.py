#!/usr/bin/python
# Especificacion, definicion y expresiones regulares
# asociadas a los tokens propios del lenguaje Brainiac.
# Modulo: LexBrainiax
# Autores:  Wilthew, Patricia    09-10910
#               Leopoldo Pimentel    06-40095

import ply.lex as lex
import ply.yacc as yacc
import sys
import funciones


# Identificadores de los tokens del lenguaje Brainiac
tokens = ['TkComa',
              'TkPuntoYComa',
              'TkParAbre',
              'TkParCierra',
              'TkCorcheteAbre',
              'TkCorcheteCierra',
              'TkLlaveAbre',
              'TkLlaveCierra',
              'TkAsignacion',
              'TkType',
              'TkMas',
              'TkResta',
              'TkMult',
              'TkDiv',
              'TkMod',
              'TkConjuncion',
              'TkDisyuncion',
              'TkNegacion',
              'TkMenor',
              'TkMenorIgual',
              'TkMayor',
              'TkMayorIgual',
              'TkIgual',
              'TkDesigual',
              'TkConcat',
              'TkInspeccion',
              'TkIdent',
              'TkNum',
              'TkPunto'
]


    # Declaracion de lista de tokens a imprimir
tok_lista = []


    # Diccionario con la lista de palabras reservadas del lenguaje Brainiac
palabras_reservadas = {
             'if' : 'TkIf',
             'then' : 'TkThen',
             'else' : 'TkElse',
             'integer' : 'TkInteger',
             'boolean' : 'TkBoolean',
             'declare' : 'TkDeclare',
             'read' : 'TkRead',
             'write' : 'TkWrite',
             'do' : 'TkDo',
             'for' : 'TkFor',
             'done' : 'TkDone',
             'while' : 'TkWhile',
             'false' : 'TkFalse',
             'true' : 'TkTrue',
             'tape' : 'TkTape',
             'execute' : 'TkExecute',
             'to' : 'TkTo',
             'from' : 'TkFrom',
             'at' : 'TkAt'
}


tokens = tokens + list(palabras_reservadas.values())

# A continuacion, se presentan las expresiones regulares para cada token
t_TkComa = r','
t_TkPunto = r'\.'
t_TkPuntoYComa =  r';'
t_TkParAbre = r'\('
t_TkParCierra =  r'\)'
t_TkCorcheteAbre = r'\['
t_TkCorcheteCierra = r'\]'
t_TkLlaveAbre = r'\{'
t_TkLlaveCierra =  r'\}'
t_TkAsignacion = r':='
t_TkType =  r':{2}'
t_TkMas = r'\+'
t_TkResta = r'-'
t_TkMult =  r'\*'
t_TkConjuncion = r'/\\'
t_TkDesigual = r'/='
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkDisyuncion =  r'\\/'
t_TkMenor = r'<'
t_TkMenorIgual = r'<='
t_TkMayor = r'>'
t_TkMayorIgual =  r'>='
t_TkIgual =  r'='
t_TkNegacion = r'\~'
t_TkConcat = r'&'
t_TkInspeccion = r'\#'


def t_TkNum(t):
  r'\d+'
  t.value = int(t.value)
  return t


def t_TkIdent(t):
   r"[a-zA-Z_][a-zA-Z0-9]*"
   t.type = palabras_reservadas.get(t.value, "TkIdent")
   return t


def t_SaltoLinea(t):
   r'\n+'
   t.lexer.lineno += len(t.value)


# Ignorar todos los espacios en blanco, salvo saltos de linea
t_ignore_EspaciosEnBlanco = r'[ \t\f\r\v]+' 


# Ignorar los comentarios 
t_ignore_Comentarios = r'\$-(.|\n)*?-\$|\${2}[^\n]*'


# Funcion para obtener errores en una lista
def t_error(t):
  c = funciones.hallar_columna(t.lexer.lexdata,t)
  print "Error: caracter inesperado \"%s\" en linea %s, columna %s." % (t.value[0],t.lineno,c)
  sys.exit(0)             
  return t


# Construccion del lexer 
lexer = lex.lex()
