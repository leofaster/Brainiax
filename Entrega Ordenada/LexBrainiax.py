#!/usr/bin/python
# Especificacion, definicion y expresiones regulares
# asociadas a los tokens propios del lenguaje Brainiac.
# Modulo: LexBrainiax.py
# Autores: Wilthew, Patricia    09-10910
#              Pimentel, Leopoldo    06-40095

import ply.lex as lex
import ply.yacc as yacc
import sys

# Se abre el archivo y se guarda su contenido en el string codigo
file_name = sys.argv[1]
fp = open(file_name)
codigo = fp.read()


# Identificadores de los tokens del lenguaje Brainiac
tokens = ['TkComa',
          'TkPunto',
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
          'TkCadena',
          'TkComentario'
         ]


# Declaracion de lista de errores
errores = []


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
         'end' : 'TkEnd',
         'false' : 'TkFalse',
         'true' : 'TkTrue',
         'tape' : 'TkTape',
         'execute' : 'TkExecute',
         'to' : 'TkTo',
         'from' : 'TkFrom',
         'at'  : 'TkAt'
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


# Ignorar los comentarios hasta que se llegue a un salto de linea
t_ignore_Comentarios = r'\$-(.|\n)*?-\$|\${2}[^\n]*'


# Funcion para obtener errores en una lista
def t_error(t):
   errores.append(t)
   t.lexer.skip(1)


# Funcion para hallar el nro de columna
def hallar_columna(programa, t):
   inicio_linea = programa.rfind("\n", 0, t.lexpos)
   return (t.lexpos - inicio_linea)



# Construccion del lexer 
lexer = lex.lex()


# Se pasa el codigo como argumento de entrada
lexer.input(codigo)


# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No mas input
    tok_lista.append (tok)


# Si hay errores, se imprime el primero
if errores:
    posCol= hallar_columna(codigo,errores[0])
    print 'Error: caracter inesperado \"%s\" en linea %d, columna %d.' %(errores[0].value[0], errores[0].lineno, posCol)
    sys.exit(0)


# Si no hay errores, se procede a construir el arbol

# for tok in tok_lista:
#    print "tk" + str(tok.type)
