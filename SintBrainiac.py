#!/usr/bin/env python
#coding: utf8 
# Analisis Sintactico del lenguaje Brainiac.
# Modulo: SintBrainiac
# Autores:  Wilthew, Patricia    09-10910
#               Leopoldo Pimentel    06-40095

import ply.lex as lex
import ply.yacc as yacc
import sys
import funciones
contador = -1

def main():

    # Se abre el archivo y se guarda su contenido en el string codigo
    file_name = sys.argv[1]
    fp = open(file_name)
    codigo = fp.read()


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
              'TkCadena'
             ]
#Elimine TkPunto temporalmente

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
    def t_TkComa(t):
      r','
      tok_lista.append(t)
      return t


#    def t_TkPunto(t):
#     r'\.'
#    tok_lista.append(t)
#    return t


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

      
    def t_TkDisyuncion(t):
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
      tok_lista.append(t)
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
      r'\d+'
      t.value = int(t.value)
      tok_lista.append(t)
      return t


    def t_TkIdent(t):
       r"[a-zA-Z_][a-zA-Z0-9]*"
       t.type = palabras_reservadas.get(t.value, "TkIdent")
       tok_lista.append(t)
       return t


    t_TkCadena = r'\"([^\\\n]|(\\.))*?\"'



    def t_SaltoLinea(t):
       r'\n+'
       t.lexer.lineno += len(t.value)


    # Ignorar todos los espacios en blanco, salvo saltos de linea
    t_ignore_EspaciosEnBlanco = r'[ \t\f\r\v]+' 


    # Ignorar los comentarios hasta que se llegue a un salto de linea
    t_ignore_Comentarios = r'\$-(.|\n)*?-\$|\${2}[^\n]*'


    # Funcion para hallar el nro de columna
    def hallar_columna(programa, t):
       inicio_linea = programa.rfind("\n", 0, t.lexpos)
       return (t.lexpos - inicio_linea)


    # Funcion para obtener errores en una lista
    def t_error(t):
        c = hallar_columna(codigo,t)
        print "Error: caracter inesperado \"%s\" en linea %s, columna %s." % (t.value[0],t.lineno,c)
        t.lexer.skip(1)                
        return t



    ####################################################
    #                                                        CLASES                                                     #
    ####################################################

    # Clase Numero
    class numero:
        def __init__(self,value):
            self.type = "Numero"
            self.value = value
        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = str(self.value)
            contador = contador - 1
            return str_

    # Clase Identificador           
    class ident:
        def __init__(self,name):
            self.type = "Identificador"
            self.name = name
        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ =  str(self.name)
            contador = contador - 1
            return str_

    # Clase de una expresion unaria
    class op_un:
        def __init__(self,pre,e):                        
            self.pre = pre
            self.e = e
        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = "EXPRESION_UNARIA\n" + tabs + "Operador: " + str(self.pre) + "\n" + tabs +  "Valor: "  + str(self.e)
            contador = contador - 1
            return str_

    # Clase de una expresion binaria                        
    class op_bin:
        def __init__(self,left,right,op):
            self.left = left
            self.right = right
            self.op = op
            if op == '+':
                self.op = 'Suma'
            elif op == '-':
                self.op = 'Resta'
            elif op == '~':
                self.op = 'Negacion'
            elif op == '*':
                self.op = 'Multiplicacion'
            elif op == '%':
                self.op = 'Modulo'
            elif op == '/':
                self.op = 'Division'
            elif op == '=':
                self.op = 'Igual'
            elif op == '/=':
                self.op = 'Desigual'
            elif op == '<':
                self.op = 'Menor que'
            elif op == '>':
                self.op = 'Mayor que'
            elif op == '>=':
                self.op = 'Mayor o igual que'
            elif op == '<=':
                self.op = 'Menor o igual que'
            elif op == '&':
                self.op = 'Concatenacion'
            elif op == '#':
                self.op = 'Inspeccion'
            elif op == '\/':
                self.op = 'Or'
            #elif op == '/\':
             #   self.op = 'And'
            else:
                self.op = 'And'

        def __str__(self):
            global contador
            contador = contador + 1
            tabs = contador*"  "
            tabs_plus =  "  " + tabs
            str_ = "EXPRESION_BINARIA\n" + tabs  + "Operacion: " + str(self.op) + "\n"  
            str_ = str_ + tabs + "Operador izquierdo: " + str(self.left) + "\n"  + tabs + "Operador derecho: " + str(self.right)
            contador = contador - 1
            return str_

    # Clase While
    class inst_while:
        def __init__(self,cond,inst):
            self.cond = cond
            self.inst = inst

        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = "ITERACION_INDETERMINADA\n" + tabs + "Condicion: " + str(self.cond) + "\n" + tabs + "Instruccion: " + str(self.inst) 
            contador = contador - 1
            return str_

    # Clase For
    class inst_for:
        def __init__(self,ident,inf,sup,inst):
            self.ident = ident
            self.inf = inf
            self.sup = sup
            self.inst = inst

        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = "ITERACION_DETERMINADA\n" + tabs + "Identificador: " + str(self.ident) + "\n" + tabs + "Cota inf: " + str(self.inf) +", Cota sup: " + str(self.sup) + "\n" + tabs + "instruccion: " + str(self.inst)
            contador = contador - 1
            return str_

    # Clase If
    class inst_if:
        def __init__(self,cond,instr0,instr1):
            self.cond = cond
            self.instr0 = instr0
            self.instr1 = instr1
        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            aux = ""
            if self.instr1 != None:
                aux = "\n" +tabs + "Else: " + str(self.instr1)
            str_ = "CONDICIONAL\n" + tabs + "Guardia: " + str(self.cond) + "\n" + tabs + "Exito: " + str(self.instr0) + aux  
            contador = contador - 1
            return str_

    # Clase Asignacion
    class inst_asig:
        def __init__(self,ident,val):
            self.ident = ident
            self.val = val
        def __str__(self):          
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = "ASIGNACION\n" + tabs + "Identificador: " + str(self.ident) + "\n" + tabs + "Valor: " + str(self.val)
            contador = contador - 1
            return str_

    # Clase Read
    class inst_read:
        def __init__(self,ident):
            self.ident = ident
        def __str__(self):
            global contador      
            contador = contador + 1
            tabs = "  "*contador
            str_ = "READ\n" + tabs + "Identificador: " +  str(self.ident.name)
            contador = contador - 1
            return str_

    # Clase Write
    class inst_write:
        def __init__(self,type):
            self.type = type
            self.args = []
        def __str__(self):
            global contador
            contador += 1
            tabs = contador*"  "
            strw = "WRITE"
            str0 = strw + "\n"
            str1 = ""
            while len(self.args) > 0:
                strs = ""
                elem = self.argls.pop()
                if not isinstance(elem, op_bin) and not isinstance(elem, op_un):
                # Si se trata de una cadena:
                    strs = "CADENA\n" + tabs + "  " + "Valor: "
                    str1 = tabs + "Elemento: " + strs + str(elem) + "\n" + str1
            contador = contador - 1
            return str0 + str1

    # Clase para lista de instrucciones
    class inst_list:
        def __init__(self):
            self.lista = []
        def __len__(self):
            return len(self.lista)
        def __pop__(self):
            return self.lista.pop()
        def __str__(self):
            global contador
            contador = contador + 1
                        
            self.lista.reverse()
            str_ = "SECUENCIACION\n"
            contador = contador + 1
            tabs = contador*"  "
            while self.lista:
                elemento =  self.lista.pop()
                str_ = str_ + tabs +   str(elemento)
                if len(self.lista) != 0:
                    str_ = str_ +  "\n" + tabs + ";\n"
            contador = contador - 1
            return str_

        def print_(self,contador):
            self.lista.reverse()

            while self.lista:
                elemento =  self.lista.pop()
                elemento.print_(contador,0)
                tabs = contador*"  "
                if len(self.lista) != 0:
                    str_ = str_ + "SEPARADOR"
            return str_

    # Clase para un bloque de instrucciones
    class bloque:
        def __init__(self,lista):
            self.lista = lista
        def __len__(self):
            return len(self.lista)
        def __str__(self):
            global contador
            contador = contador + 1
            tabs = "  "*contador
            str_ = "BLOQUE\n"
            str_ = str_ + str(self.lista)
            contador = contador - 1
            return str_
                        

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
        p[0] = numero(p[1])
        str_ = ""
        tabs = (contador+1)*"  "


    # IDENTIFICADOR
    def p_term_ident(p):
        ''' term : TkIdent '''
        p[0] = ident(p[1])
        str_ = ""
        tabs = (contador+1)*"  "


    # EXPRESION UNARIA
    def p_exp_un(p):
        ''' exp_un : TkResta exp %prec uminus
                      | TkNegacion exp %prec unot '''
        p[0] = op_un(p[1],p[2])


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
            p[0] = op_bin(p[1],p[3],p[2])
        else:
			p[0] = p[2]
                

    # ASIGNACION
    def p_instruccion_asignacion(p):
        ''' instruccion : TkIdent TkAsignacion exp '''
        p[0] = inst_asig(p[1],p[3])


    # READ
    def p_instruccion_read(p):
        ''' instruccion : TkRead exp '''
        p[0] = inst_read(p[2])


    # WRITE
    def p_instruccion_write(p):
        ''' instruccion : TkWrite TkCadena '''
        p[0] = inst_write(p[1])
        p[0].args = p[2]


    # WRITE ARGUMENTOS
	def p_instruccion_write_args(p):
		'''writeargs  : writeargs TkComma TkCadena
			   | writeargs TkComa exp
			   | TkCadena
			   | exp'''

		if len(p) == 2:
			p[0] = []
			p[0].append(p[1])
		elif len(p) == 4:
			p[0] = p[1]
			p[0].append(p[3])


    # WHILE
    def p_instruccion_while(p):
        ''' instruccion : TkWhile exp TkDo instruccion TkDone '''
        p[0] = inst_while(p[2],p[4])


    # FOR
    def p_instruccion_for(p):
        ''' instruccion : TkFor TkIdent TkFrom exp TkTo exp TkDo instruccion TkDone'''
        p[0] = inst_for(p[2],p[4],p[6],p[8])

    # IF
    def p_instruccion_if(p):
        ''' instruccion : TkIf exp TkThen instruccion TkDone
			                | TkIf exp TkThen instruccion TkElse instruccion TkDone '''
        if len(p) == 6:
            p[0] = inst_if(p[2],p[4],None)
        else:
            p[0] = inst_if(p[2],p[4],p[6])


    # Gramatica del bloque de instrucciones
    def p_instruction_bloque(p):
        ''' instruccion :  declaracion TkExecute instlist TkDone
                            | TkExecute instlist TkDone'''
        if len(p) == 4:
            p[0] = inst_bloque(p[2])
        elif len(p) == 5:
            p[0] = inst_bloque(p[3])


    # SECUENCIACION DE INSTRUCCIONES
    def p_instlist(p):
        '''  instlist : instlist semicoloninst 
                      | instruccion '''
        if len(p) == 2:
            p[0] = inst_list()
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
        c = hallar_columna(codigo,p)
        print "Error de sintaxis en linea %s, columna %s: token \'%s\' inesperado." % (p.lineno,c,p.value)
        sys.exit(0)


    # Construccion del lexer 
    lexer = lex.lex()
    lexer.input(codigo)


    errores = False 
    while True:
        tok  = lexer.token()
        if not tok: break
        if tok.type == 'error':
            errores = True
            continue

    # Si hay errores, se imprime el primero
    if errores:
        posCol= hallar_columna(codigo,errores[0])
        print 'Error: caracter inesperado \"%s\" en linea %d, columna %d.' %(errores[0].value[0], errores[0].lineno, posCol)
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



