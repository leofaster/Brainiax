#!/usr/bin/env python
# Especificacion, definicion y expresiones regulares
# asociadas a los tokens propios del lenguaje Brainiac.
# Modulo: expresiones.py
# Autores: Wilthew, Patricia 	09-10910
#          Leopoldo Pimentel    06-40095
import ply.lex as lex
import sys

# Se abre el archivo y se guarda su contenido en el string codigo
file_name = sys.argv[1]
fp = open(file_name)
codigo = fp.read()

# Identificadores de los tokens del lenguaje Rangex
tokens = ['TkComa',
          'TkPunto',
          'TkPuntoYComa',
          'TkParAbre',
          'TkParCierra',
          'TkCorcheteAbre',
          'TkCorcheteCierra',
          'TkLlaveAbre',
          'TkLlaveCierra',
          'TkType',
          'TkMas',
          'TkMenos',
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
          'TkId',
          'TkNumero',
          'TkCadena',
          'TkComentario'
         ]
  
# Declaracion de lista de errores
errores = []

# Declaracion de lista de tokens a imprimir
tok_lista = []

# Diccionario con la lista de palabras reservadas del lenguaje Rangex
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
         'execute' : 'TkExecute'
         
}

tokens = tokens + list(palabras_reservadas.values())

# A continuacion, se presentan las expresiones regulares para cada token
def t_TkComa(t):
  r'\,'
  tok_lista.append(t)
  return t
  
def t_TkPunto(t):
  r'\.'
  tok_lista.append(t)
  return t
  
def t_TkPuntoYComa(t):
   r'\;'
   tok_lista.append(t)
   return t

def t_TkParAbre(t):
  r'\('
  tok_lista.append(t)
  return t
  
def t_TkParCierra(t):
  r'\)'
  tok_lista.append(t)
  return t  
  
def t_TkCorcheteAbre(t):
  r'\['
  tok_lista.append(t)
  return t
  
def t_TkCorcheteCierra(t):
  r'\]'
  tok_lista.append(t)
  return t 

def t_TkLlaveAbre(t):
  r'\['
  tok_lista.append(t)
  return t
  
def t_TkLlaveCierra(t):
  r'\]'
  tok_lista.append(t)
  return t    
  
def t_TkType(t):
  r'\::'
  tok_lista.append(t)
  return t    
  
def t_TkMas(t):
  r'\+'
  tok_lista.append(t)
  return t
  
def t_TkMenos(t):
  r'\-'
  tok_lista.append(t)
  return t

def t_TkMult(t):
  r'\*'
  tok_lista.append(t)
  return t

def t_TkDiv(t):
  r'\/'
  tok_lista.append(t)
  return t

def t_TkMod(t):
  r'\%'
  tok_lista.append(t)
  return t

def t_TkConjuncion(t):
  r'\/\\'
  tok_lista.append(t)
  return t

def t_TkDisyuncion(t):
  r'\\\/'
  tok_lista.append(t)
  return t
  
  
def t_TkNegacion(t):
  r'\~'
  return t

def t_TkMenor(t):
  r'\<'
  tok_lista.append(t)
  return t

def t_TkMenorIgual(t): 
  r'\<\='
  tok_lista.append(t)
  return t
  
def t_TkMayor(t):
  r'\>'
  tok_lista.append(t)
  return t

def t_TkMayorIgual(t): 
  r'\>\='
  tok_lista.append(t)
  return t

def t_TkIgual(t):
  r'\='
  tok_lista.append(t)
  return t
  
def t_TkDesigual(t):
  r'\/='
  tok_lista.append(t)
  return t
  
def t_TkConcat(t): 
  r'\&'
  tok_lista.append(t)
  return t
  
def t_TkInspeccion(t): 
  r'\#'
  tok_lista.append(t)
  return t
  
def t_TkComentario(t):
  r'\$-'
  tok_lista.append(t)
  return t

def t_TkNumero(t): 
  r'[\+\-]?\d+'
  t.value = int(t.value)
  if (t.value <= 2**31 - 1) :
      t.value = str(t.value)
      tok_lista.append(t)
  else:
      t.value = str(t.value)
      errores.append(t)
  return t

def t_TkCadena(t): 
  r'\"(.)*\\"(.)*\\"(.)*\"|\"[^"]*\"'
  tok_lista.append(t)
  return t

def t_TkId(t):
   r"[a-zA-Z_][a-zA-Z0-9]*"
   t.type = palabras_reservadas.get(t.value, "TkId")
   tok_lista.append(t)
   return t
  
def t_SaltoLinea(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

# Ignorar todos los espacios en blanco, salvo saltos de linea
t_ignore_EspaciosEnBlanco = r'[ \t\f\r\v]+' 

# Ignorar los comentarios hasta que se llegue a un salto de linea
t_ignore_Comentarios = r'($-)[^\n]*'

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

# Si no existen elementos en lista de errores, se imprimen los tokens    
if not errores: 
  for elem in tok_lista:
    posCol= hallar_columna(codigo,elem)
    if elem.type == "TkNumero":
      print elem.type,elem.value,"( Linea", elem.lineno , ", Columna" , posCol, ")"
    else:
      print '%s \"%s\" (Linea %d, columna %d)' %(elem.type, elem.value, elem.lineno, posCol)
      
# En caso contrario, se imprimen solo los errores encontrados
if errores:
  for err in errores:
    posCol= hallar_columna(codigo,err)
    if err.type == 'TkNumero' :
      print 'Error: Numero no valido en linea %d, columna %d.' %(err.lineno, posCol)  
    else:
      print 'Error: caracter inesperado \"%s\" en linea %d, columna %d.' %(err.value[0], err.lineno, posCol)
