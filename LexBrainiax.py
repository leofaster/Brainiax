#!/usr/bin/python



# Especificacion, definicion y expresiones regulares

# asociadas a los tokens propios del lenguaje Brainiac.

# Modulo: expresiones.py

# Autores: Wilthew, Patricia    09-10910

#          Leopoldo Pimentel    06-40095

import ply.lex as lex

import sys



#String que contiene el codigo

#codigo = raw_input("Inserte el codigo: ")

#print codigo

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

         'execute' : 'TkExecute',

         'to' : 'TkTo',

         'from' : 'TkFrom',
          
         'at'  : 'tkAt'


}



tokens = tokens + list(palabras_reservadas.values())



# A continuacion, se presentan las expresiones regulares para cada token

def t_TkComa(t):

  r','

  tok_lista.append(t)

  return t


def t_TkPunto(t):

  r'\.'

  tok_lista.append(t)

  return t


def t_TkPuntoYComa(t):

   r';'

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

  r'\{'

  tok_lista.append(t)

  return t


def t_TkLlaveCierra(t):

  r'\}'

  tok_lista.append(t)

  return t




def t_TkAsignacion(t):

  r':='

  tok_lista.append(t)

  return t


def t_TkType(t):

  r':{2}'

  tok_lista.append(t)

  return t


def t_TkMas(t):

  r'\+'

  tok_lista.append(t)

  return t


def t_TkResta(t):

  r'-'

  tok_lista.append(t)

  return t


def t_TkMult(t):

  r'\*'

  tok_lista.append(t)

  return t


def t_TkConjuncion(t):

  r'/\\'

  tok_lista.append(t)

  return t

def t_TkDesigual(t):

  r'/='

  tok_lista.append(t)

  return t

def t_TkDiv(t):

  r'/'

  tok_lista.append(t)

  return t


def t_TkMod(t):

  r'%'

  tok_lista.append(t)

  return t


  r'\\/'

  tok_lista.append(t)

  return t





def t_TkMenor(t):

  r'<'

  tok_lista.append(t)

  return t



def t_TkMenorIgual(t):

  r'<='

  tok_lista.append(t)

  return t


def t_TkMayor(t):

  r'>'

  tok_lista.append(t)

  return t



def t_TkMayorIgual(t):

  r'>='

  tok_lista.append(t)

  return t


def t_TkIgual(t):

  r'='

  tok_lista.append(t)

  return t


def t_TkNegacion(t):

  r'\~'

  return t


def t_TkConcat(t):

  r'&'

  tok_lista.append(t)

  return t


def t_TkInspeccion(t):

  r'\#'

  tok_lista.append(t)

  return t



def t_TkNum(t):

  r'[\+-]?\d+'

  #t.value = int(t.value)

  t.value = str(t.value)

  tok_lista.append(t)

  return t


def t_TkCadena(t): 

  r'\"(.)*\\"(.)*\\"(.)*\"|\"[^"]*\"'

  tok_lista.append(t)

  return t



def t_TkIdent(t):

   r"[a-zA-Z_][a-zA-Z0-9]*"

   t.type = palabras_reservadas.get(t.value, "TkIdent")

   tok_lista.append(t)

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



#Leemos entrada y concatenamos en data

#for line in sys.stdin:

#codigo += line



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

    if elem.type == ("TkNum"):
      print '%s(%s)' %(elem.type,elem.value)
    if elem.type == ("TkIdent"):
      print '%s("%s")' %(elem.type,elem.value)
    else:
      if elem.type !=("TkNum"):
        print '%s' %(elem.type)


# En caso contrario, se imprimen solo los errores encontrados

if errores:

  for err in errores:

    posCol= hallar_columna(codigo,err)

    if err.type == 'TkNumero' :

      print 'Error: Numero no valido en linea %d, columna %d.' %(err.lineno, posCol)  

    else:

       print 'Error: caracter inesperado \"%s\" en linea %d, columna %d.' %(err.value[0], err.lineno, posCol)
