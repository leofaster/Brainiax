#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8 
# Analisis de Contexto del lenguaje Brainiac.
# Modulo: ContBrainiac
# Autores:  Wilthew, Patricia    09-10910
#           Leopoldo Pimentel    06-40095

import ply.lex as lex
import ply.yacc as yacc
import sys
import funciones
import tablaSimbolos
from LexBrainiax import tokens  
from LexBrainiax import comm

contador = -1
stack = []  #Pila de tabla de simbolos
Analisis = ""
first_line = 1

post_program = False


# Clases utilizadas para imprimir el arbol sintactico
                                               
# Clase para NUMERO
class numero:

    def __init__(self,value,line,column):
        self.type = "Numero"
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = str(self.value) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        return 'integer'

    def getLine(self):
        return self.line

    def getColumn(self):
        return self.column
        
    def evaluate(self):
		return self.value

# Clase para BOOLEAN
class booleano:

    def __init__(self,value,line,column):
        self.type = "boolean"
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = str(self.value)
        contador = contador - 1
        return str_

    def checktype(self):
        return 'boolean'

    def getLine(self):
        return self.line

    def getColumn(self):
        return self.column
        
    def evaluate(self):
		if self.value == 'true':
			return True
		return False

# Clase para una EXPRESION TAPE [a]
class tape:
	def __init__(self,tamano,line,column):
		self.type = tape
		self.tamano = tamano
		
	def __str__(self):
		global contador
		contador = contador + 1
		tabs = "  "*contador
		str_ = "[ " + str(self.tamano) + "]"
		contador = contador - 1
		return str_
        
	def checktype(self):
		return 'tape'

	def getLine(self):
		return self.line

	def getColumn(self):
		return self.column
        
	def evaluate(self):
		return self.tamano
		
# Clase para IDENTIFICADOR           
class ident:

    def __init__(self,name, line, column):
        self.type = "Identificador"
        self.name = name
        self.line = line  
        self.column = column

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ =  str(self.name) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        clone = list(stack)
        result = 'error' 
        while clone and result == 'error':
            st = clone.pop()
            if st.isMember(self.name):
                if st.goesTo(self.name,'integer'):
                    result = 'integer'  
                elif st.goesTo(self.name,'boolean'):
                    result = 'boolean'
                elif st.goesTo(self.name,'tape'):
                    result = 'tape'

		if result == 'error':
			global Analisis
			str0 = "Error en Linea %s , Columna %s:" %(self.line,self.column) 
			str0 = str0 + " no puede usar la variable " + '"' + self.name + '"' + ", pues no ha sido declarada" 
			Analisis = Analisis + "\n" + str0
		self.type = result
		return result 
            
    def getLine(self):
        return self.line 
        
    def getColumn(self):
        return self.column
        
    def evaluate(self):
        i = len(stack)-1
        r = None
        found = False 
        while (found == False):
            st = stack[i]
            if st.isMember(self.name):
                found = True
                r = st.findValue(self.name)
            if r == None:
                print "Error: La variable \"{}\" no ha sido inicializada.".format(self.name)
                sys.exit(0)
	return r

# Clase para EXPRESION UNARIA
class op_un:

    def __init__(self,pre,e,line,column):                        
        self.pre = pre
        self.e = e
        self.type = None
        self.line = line  
        self.column = column

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = "EXPRESION_UNARIA\n" + tabs + "Operador: " + str(self.pre) + "\n" + tabs +  "Valor: "  + str(self.e) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        if self.pre == '-':
            return 'integer'
        elif self.pre == '#':
            return 'integer'
        elif self.pre == '~':
            return 'boolean'

    def getLine(self):
        return self.line 

    def getColumn(self):
        return self.column
        
    def evaluate(self):
		elem = self.evaluate()
		if self.type == 'boolean':
			r = not elem
		elif self.type == 'integer':
			r = elem*(-1)
		elif self.type == 'tape':
			r = elem 
		return r

# Clase para EXPRESION BINARIA                       
class op_bin:

    def __init__(self,left,right,op):
        self.left = left
        self.right = right
        self.op = op
        self.type = None
        if op == '+':
            self.op = 'Suma'
        elif op == '-':
            self.op = 'Resta'
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
        elif op == '\/':
            self.op = 'Or'
        else:
            self.op = 'And'

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = contador*"  "
        tabs_plus =  "  " + tabs
        str_ = "EXPRESION_BINARIA\n" + tabs  + "Operacion: " + str(self.op) + "\n"  
        str_ = str_ + tabs + "Operador izquierdo: " + str(self.left) + "\n"  + tabs + "Operador derecho: " + str(self.right)  + " "
        contador = contador - 1
        return str_

    def checktype(self):
        result1 = self.left.checktype() 
        result2 = self.right.checktype()
        result = "error"
        global Analisis
        if (result1 == 'integer') and (result2 == 'integer'): 
            if (self.op == 'Suma' or self.op == 'Resta' or self.op == 'Multiplicacion'
                or self.op == 'Modulo' or self.op == 'Division'):
                result = 'integer' 
            elif (self.op == 'Mayor que' or self.op == 'Mayor o igual que' or self.op == 'Menor que'
                or self.op == 'Menor o igual que' or self.op == 'Igual' or self.op == 'Desigual'):
                result = 'boolean'
            else:
                str0 = "Error en Linea %s, Columna %s: " % (self.left.getLine(),self.left.getColumn())
                str0 = str0 + "Se intenta operacion " + self.op
                str1 = " con expresiones del tipo entera" 
                Analisis = Analisis + "\n" + str0 + str1
        elif (result1 == 'tape') and (result2 == 'tape'):
            if (self.op == 'Concatenacion'):   
                result = 'tape'
            else:
                str0 = "Error en Linea %s, Columna %s: " % (self.left.getLine(),self.left.getColumn())
                str0 = str0 + "Se intenta operacion " + self.op
                str1 = " con expresiones del tipo tape" 
                Analisis = Analisis + "\n" + str0 + str1
        elif (result1 == 'boolean' and result2 == 'boolean'):
            if self.op == 'Igual' or self.op == 'Desigual' or self.op == 'Or' or self.op ==  'And':
                result = 'boolean'
            else:
                str0 = "Error en Linea %s, Columna %s: " % (self.left.getLine(),self.left.getColumn())
                str0 = str0 + "Se intenta operacion " + self.op
                str1 = " con expresiones del tipo boolean" 
                Analisis = Analisis + "\n" + str0 + str1
        else:
            if result1 != "error" and result2 != "error":   
                str0 = "Error en Linea %s, Columna %s: " % (self.left.getLine(),self.left.getColumn())
                str0 = str0 + "Se intenta operacion " + self.op
                str1 = " con expresion izquierda del tipo " + result1 + " y expresion derecha del tipo " + result2
                Analisis = Analisis + "\n" + str0 + str1
        return result 
    
    def getLine(self):
        return self.left.getLine()

    def getColumn(self):
        return self.left.getColumn()

	def evaluate(self):
		if self.op == 'Suma':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left + right
		elif self.op == 'Resta':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left - right
		if self.op == 'Multiplicacion':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left * right
		if self.op == 'Modulo':
			left = self.left.evaluate()
			right = self.right.evaluate()
			if right == 0:
				return "Error: Division modulo entre cero. "
				sys.exit(0)
			else:
				r = left % right
		if self.op == 'Division':
			left = self.left.evaluate()
			right = self.right.evaluate()
			if right == 0:
				return "Error: Division entre cero. "
				sys.exit(0)
			else:
				r = left / right
		if self.op == 'Igual':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left == right
		if self.op == 'Desigual':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left != right
		if self.op == 'Menor que':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left < right
		if self.op == 'Mayor que':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left > right
		if self.op == 'Mayor o igual que':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left >= right
		if self.op == 'Menor o igual que':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left <= right
		if self.op == 'Concatenacion':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left + right
		if self.op == 'Or':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left or right
		if self.op == 'And':
			left = self.left.evaluate()
			right = self.right.evaluate()
			r = left and right
		return r
		
# Clase para ITERACION_INDETERMINADA
class inst_while:

    def __init__(self,cond,inst):
        self.cond = cond
        self.inst = inst

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = "ITERACION_INDETERMINADA\n" + tabs + "Condicion: " 
        str_ = str_+ str(self.cond) + "\n" + tabs + "Instruccion: \n" + str(self.inst) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        result = self.cond.checktype()
        if result != 'boolean' and result != "error":
            global Analisis
            str0 = "Error en Linea %s, Columna %s: " % (self.cond.getLine(),self.cond.getColumn())
            str0 = str0 + "Se esperaba expresion del tipo boolean, no del tipo " + result 
            Analisis = Analisis + "\n" + str0 

    def execute(self):
		while self.cond.evaluate() == True:
			self.inst.execute()
			
# Clase para ITERACION_DETERMINADA
class inst_for:

    def __init__(self,ident,inf,sup,inst,line,column):
        self.ident = ident
        self.inf = inf
        self.sup = sup
        self.inst = inst
        self.line = line
        self.column = column

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        identificador = " "
        if not(str(self.ident) == None):
			identificador = str(self.ident) 
        str_ = "ITERACION_DETERMINADA\n" + tabs + "Identificador: " + identificador
        str_ = str_ + "\n" + tabs + "Cota inf: " + str(self.inf) +", Cota sup: " 
        str_ = str_ + str(self.sup) + "\n" + tabs + "Instruccion: \n" + str(self.inst) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        clone = list(stack)
        while clone:
            st = clone.pop()    
            global Analisis
            if not(self.ident == None):
                if not(st.isMember(self.ident)):
                    str0 = "Error en Linea %s, Columna %s" %(self.line,self.column)
                    str0 = str0 + " variable de iteracion determinada " + identificador  + " no ha sido declarada"
                    Analisis = Analisis + "\n" + str0
            break
            
	def execute(self):
		x = self.inf
		##############HAY QUE OBTENER EL INDICE DE LA PILA DONDE ESTA EL ULTIMO IDENT
		index = len(stack)
		for x in range(self.inf, self.sup):
			self.inst.execute()
			stack[index].update(self.ident.name,['integer',x+1])

# Clase para CONDICIONAL
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
            aux = "\n" +tabs + "Else: \n" + str(self.instr1) + " "
        str_ = "CONDICIONAL\n" + tabs + "Guardia: " + str(self.cond) + "\n" + tabs + "Exito: \n" + str(self.instr0) + aux  
        contador = contador - 1
        return str_

    def checktype(self):
        result = self.cond.checktype()
        if result != 'boolean' and result != 'error':
            global Analisis
            str0 = "Error en Linea %s, Columna %s: " % (self.cond.getLine(),self.cond.getColumn())
            str0 = str0 + "Se esperaba expresion del tipo boolean, no del tipo " + result 
            Analisis = Analisis + "\n" + str0 

	def execute(self):
		if self.cond.evaluate() == True:
			self.instr0.execute()
			return
		if instr1 != None:
			self.instr1.execute()
			
# Clase para B-INSTRUCCION
class inst_b:

    def __init__(self, slist, ident):
        self.slist = slist
        self.ident = ident

    def __pop__(self):
        return self.slist.pop()

    def __len__(self):
        return len(self.slist)

    def __str__(self):
        global contador
        contador = contador +1
        tabs = "  "*contador
        lista_simbolos = ""
        for elem in self.slist:
            lista_simbolos = lista_simbolos + str(elem)
        str_ = "B-INSTRUCCION\n" + tabs + "Lista de simbolos: " + lista_simbolos + "\n" 
        straux = tabs + "Identificador: " + str(self.ident) + " "
        contador = contador - 1
        return str_ + straux


# Clase para ASIGNACION
class inst_asig:

    def __init__(self,ident,val, line, column):
        self.ident = ident
        self.val = val
        self.line = line
        self.column = column

    def __str__(self):          
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = "ASIGNACION\n" + tabs + "Identificador: " + str(self.ident) + "\n" + tabs + "Valor: " + str(self.val) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        clone = list(stack)
        result1 = 'error'
        while clone and result1 == 'error':
            st = clone.pop()
            if st.isMember(self.ident):
                if st.goesTo(self.ident,'integer'):
                    result1 = 'integer' 
                elif st.goesTo(self.ident,'boolean'):
                    result1 = 'boolean'
                elif st.goesTo(self.ident,'tape'):
                    result1 = 'tape'
                
        global Analisis
        if result1 == 'error':
            str0 = "Error en Linea %s, Columna %s: " %(self.line,self.column)
            str0 = str0 + "no puede usar la variable " + '"' + self.ident + '"' + ", pues no ha sido declarada"
            Analisis = Analisis + "\n" + str0
        else:
            result2 = self.val.checktype()
            if result1 != result2 and result2 != "error":
                str0 = "Error en Linea %s, Columna %s " % (self.val.getLine(),self.val.getColumn())
                str1 = ": Error de tipos en asignacion a la variable " + self.ident
                Analisis = Analisis + "\n" + str0 + str1
                
	def execute(self):
		i = len(stack)-1
		while i >= 0:
			if stack[i].isMember(self.ident):
				a = self.val.evaluate()
				stack[i].addValueToKey(self.ident,a)
				break
			i -= 1

# Clase para READ
class inst_read:

    def __init__(self,ident, line, column):
        self.ident = ident
        self.line = line
        self.column = column

    def __str__(self):
        global contador      
        contador = contador + 1
        tabs = "  "*contador
        str_ = "READ\n" + tabs + "Identificador: " +  str(self.ident.name) + " "
        contador = contador - 1
        return str_

    def checktype(self):
        clone = list(stack) 
        declared = False
        global Analisis
        while clone and not declared:
            st = clone.pop()
            if st.isMember(self.ident.name):
                declared = True
        if not declared:
            str0 = "Error en Linea %s, Columna %s: " %(self.line,self.column)
            str0 = str0 + "no puede usar la variable " + '"' + str(self.ident) + '"' + ", pues no ha sido declarada"
            Analisis = Analisis + "\n" + str0

# Clase para WRITE
class inst_write:
    def __init__(self,expr):
        self.expr = expr

    def __str__(self):
        global contador
        contador += 1
        tabs = contador*"  "
        strw = "WRITE" + "\n" + tabs + "Contenido: " 
        str1 = strw + str(self.expr) + " "
        contador = contador - 1
        return str1
        
	def execute(self):
		print self.expr
		return

# Clase para SECUENCIACION
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
        tabs = "  "*contador
        str_ = ""
        
        while self.lista:
            elemento =  self.lista.pop()
            str_ = str_ + tabs +   str(elemento)
            if len(self.lista) != 0:
                str_ = str_ +  "\n\n"  
        contador = contador - 1
                
        return str_        
        
    def print_(self,contador):
        self.lista.reverse()

        while self.lista:
            elemento =  self.lista.pop()
            elemento.print_(contador,0)
            tabs = contador*"  "
            if len(self.lista) != 0:
                str_ = str_ + ";"
        return str_

	def execute(self):
		i = 0
		while i < len(self.lista):
			self.lista[i].execute()
			i += 1

# Clase para BLOQUE
class bloque:

    def __init__(self,lista,st):
        self.lista = lista
        self.declare = st #symtable local al bloque

    def __len__(self):
        return len(self.lista)

    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_ = "BLOQUE\n"
        strdec = ""
        if self.declare != None:
            strdec = str(self.declare) + "\n" 
        str_ = str_ + strdec + str(self.lista)
        contador = contador - 1
        return str_
        
	def execute(self):
		if self.declare != None:
			stack.append(self.declare.tablaSimbolos.cloneSymtable())
			self.lista.execute()
		if self.declare != None:
			stack.pop()
			
#Clases para DECLARACION de variables
class declare:

    def __init__(self,declist,line,column):
        self.symtable = tablaSimbolos.symtable()
        self.declist = declist
        self.line = line
        self.column =  column 
        while declist:
            elem = declist.pop()
            if isinstance(elem, dec):
                while elem.l:
                    e = elem.l.pop()
                    if self.symtable.isMember(str(e)):
                        global Analisis
                        str0 = "Error en Linea %s, Columna %s: " %(self.line,self.column)
                        str0 = str0 + "la variable " + '"'+ str(e) + '"' + " ya ha sido declarada"
                        Analisis = Analisis + "\n" + str0
                    self.symtable.insert(str(e),elem.type)
                stack.append(self.symtable.cloneSymtable())    
       
    def __str__(self):
        global contador
        contador = contador + 1
        tabs = "  "*contador
        str_st = tabs + "DECLARACION\n"
        staux = self.symtable.get()
        for key, value in dict.items(staux):
            str0 = tabs + "Identificador: " + key
            str1 = ": " + value + "\n"
            str_st = str_st + str0 + str1 
        return str_st
                        
class dec:

    def __init__(self,l,type):
        self.l = l
        self.type = type
		




# Llamada principal al analizador sintactico
def main():

    # Se abre el archivo y se guarda su contenido en el string codigo
    file_name = sys.argv[1]
    fp = open(file_name)
    codigo = fp.read()


    # Manejo de gramática y construccion de arbol

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
            ('left','TkAt'),
            ('right','uminus','unot', 'uinspeccion'),                
        )


    # PROGRAMA
    
    def p_seen_program(p):
        ''' seen_program : '''
        global first_line
        global post_program
        post_program = True
        first_line = p.lineno(0)


    def p_programa(p):
        ''' programa : seen_program declaracion TkExecute instlist TkDone
                     |  seen_program TkExecute instlist TkDone '''
        if len(p) == 5:
            p[0] = bloque(p[4], p[2])
        elif len(p) == 4:
            p[0] = bloque(p[3], None)

            
            
            
    # NUMERO
    def p_term_num(p):
        ''' term : TkNum '''
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = numero(p[1],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))
        str_ = ""
        tabs = (contador+1)*"  "
        
        
    # TERMINO BOOLEANO
    def p_term_bool(p):
        ''' term : TkTrue
                | TkFalse '''
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = booleano(p[1],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))

        
    # IDENTIFICADOR
    def p_term_ident(p):
        ''' term : TkIdent '''
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = ident(p[1],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))
        str_ = ""
        tabs = (contador+1)*"  "


    # EXPRESION UNARIA
    def p_exp_un(p):
        ''' exp_un : TkResta exp %prec uminus 
                      | TkNegacion exp %prec unot
                      | TkInspeccion exp %prec uinspeccion '''
        p[0] = op_un(p[1],p[2],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))


    # EXPRESION
    def p_exp(p): 
        ''' exp : term
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
                | exp TkDisyuncion exp
                | exp TkConjuncion exp 
                | exp TkConcat exp '''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4 and p[1] != '(' and p[1] != '[' and p[1] != '{':
            p[0] = op_bin(p[1],p[3],p[2])
        elif len(p) == 4 and p[1] == '[':
			p[0] = tape(p[2],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))
        else:
            p[0] = p[2]
                

    # ASIGNACION
    def p_instruccion_asignacion(p):
        ''' instruccion : TkIdent TkAsignacion exp '''
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = inst_asig(p[1],p[3],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))
        p[0].checktype()


    # READ
    def p_instruccion_read(p):
        ''' instruccion : TkRead exp '''
        if post_program:
            linea = p.lineno(2)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = inst_read(p[2],p.lineno(2),funciones.find_column_parser(codigo,p.lexpos(1)))
        p[0].checktype()


    # WRITE
    def p_instruccion_write(p):
        ''' instruccion : TkWrite exp '''
        p[0] = inst_write(p[2])


    # WHILE
    def p_instruccion_while(p):
        ''' instruccion : TkWhile exp TkDo instlist TkDone '''
        p[0] = inst_while(p[2],p[4])
        p[0].checktype()


    # FOR
    def p_instruccion_for(p):
        ''' instruccion : TkFor TkIdent TkFrom exp TkTo exp TkDo instlist TkDone 
                        | TkFor exp TkTo exp TkDo instlist TkDone '''
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        if len(p) == 10:
            p[0] = inst_for(p[2],p[4],p[6],p[8],p.lineno(2),p.lexpos(2))
        else:
            p[0] = inst_for(None,p[2],p[4],p[6],p.lineno(2),p.lexpos(2))
        p[0].checktype()


    # IF
    def p_instruccion_if(p):
        ''' instruccion : TkIf exp TkThen instlist TkDone
                            | TkIf exp TkThen instlist TkElse instlist TkDone '''
        if len(p) == 6:
            p[0] = inst_if(p[2],p[4],None)
        else:
            p[0] = inst_if(p[2],p[4],p[6])
        p[0].checktype()


    # BLOQUE DE INSTRUCCIONES
    def p_instruccion_bloque(p):
        ''' instruccion :  declaracion TkExecute instlist TkDone
                            | TkExecute instlist TkDone '''
        if len(p) == 4:
            p[0] = bloque(p[2], None)
        elif len(p) == 5:
            p[0] = bloque(p[3], p[1])
            stack.pop()


    # BLOQUE DE B-INSTRUCCION (Ej: {lista_tape} At [a] )
    def p_instruccion_b(p):
        ''' instruccion : TkLlaveAbre lista_tape TkLlaveCierra TkAt ident_tape '''
        p[0] = inst_b(p[2], p[5])

    def p_ident_tape(p):
        ''' ident_tape : TkCorcheteAbre exp TkCorcheteCierra
                           | TkIdent '''
        if len(p) == 4:        
            p[0] = p[2]
        elif len(p) == 2:
            p[0] = p[1] 

 
    # LISTA DE SIMBOLOS DE B-INSTRUCCIONES (Ej: ++++--...>>><..)
    def p_lista_tape(p):
        ''' lista_tape : lista_tape simb_tape
                         | simb_tape '''
        if len(p) == 2:
            p[0] = []
            p[0].append(p[1])
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_simb_tape(p):
        '''simb_tape : TkPunto
                         | TkMayor
                         | TkMenor
                         | TkMas
                         | TkResta
                         | TkComa '''
        p[0] = p[1]


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
        if post_program:
            linea = p.lineno(1)-first_line+2+comm
        else:
            linea = comm+1
        p[0] = declare(p[2],p.lineno(1),funciones.find_column_parser(codigo,p.lexpos(1)))

    def p_declist(p):
        ''' declist : dec TkPuntoYComa declist 
                    | dec '''
        if len(p) == 2:
            p[0] = []
            p[0].append(p[1])
        else:
            p[0] = p[3]
            p[0].append(p[1])

    def p_dec(p):
        ''' dec : varlist TkType tipo '''
        p[0] = dec(p[1],p[3])

    def p_varlist(p):
        ''' varlist : TkIdent TkComa varlist 
                    | TkIdent '''
        if len(p) == 2:
            p[0] = []
            p[0].append(p[1])
        else:
            p[0] = p[3]
            p[0].append(p[1])

    def p_tipo_integer(p):
        ''' tipo : TkInteger '''
        p[0] = p[1]
        
    def p_tipo_boolean(p):
        ''' tipo : TkBoolean '''
        p[0] = p[1]
        
    def p_tipo_tape(p):
        ''' tipo : TkTape '''
        p[0] = p[1]
        

    #Funcion de error del parser
    def p_error(p):
        c = funciones.print_column(codigo,p)
        if post_program:
            linea = p.lineno-first_line+2+comm
        else:
            linea = comm+1
        str = "Error de sintaxis en linea %s, columna %s: token %s inesperado. \n" %(p.lineno, c, p.value[0])
        print str
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

    # Se construye el árbol
    arbol = parser.parse(codigo,debug=log, tracking=True)

    # Se imprime el árbol
    if Analisis == '':
		global stack
		stack = []
		arbol.execute()
		#print funciones.print_arbol(arbol)
    else:
        print Analisis	

if __name__ == "__main__":
    main()
