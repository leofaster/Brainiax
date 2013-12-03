

####################################################
#                                                        CLASES                                                     #
####################################################

# Clase para NUMERO
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

# Clase para IDENTIFICADOR           
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

# Clase para EXPRESION UNARIA
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

# Clase para EXPRESION BINARIA                       
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
        str_ = str_ + tabs + "Operador izquierdo: " + str(self.left) + "\n"  + tabs + "Operador derecho: " + str(self.right)  + " "
        contador = contador - 1
        return str_

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
        str_ = str_+ str(self.cond) + "\n" + tabs + "Instruccion: " + str(self.inst)
        contador = contador - 1
        return str_

# Clase para ITERACION_DETERMINADA
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
        str_ = "ITERACION_DETERMINADA\n" + tabs + "Identificador: " + str(self.ident) 
        str_ = str_ + "\n" + tabs + "Cota inf: " + str(self.inf) +", Cota sup: " 
        str_ = str_ + str(self.sup) + "\n" + tabs + "Instruccion: " + str(self.inst)
        contador = contador - 1
        return str_

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
            aux = "\n" +tabs + "Else: " + str(self.instr1)
        str_ = "CONDICIONAL\n" + tabs + "Guardia: " + str(self.cond) + "\n" + tabs + "Exito: " + str(self.instr0) + aux  
        contador = contador - 1
        return str_

# Clase para ASIGNACION
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

# Clase para READ
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

# Clase para WRITE
class inst_write:
    def __init__(self,expr):
        self.expr = expr
    def __str__(self):
        global contador
        contador += 1
        tabs = contador*"  "
        strw = "WRITE"
        str0 = strw + "\n"
        str1 = ""
        strs = "CADENA\n" + tabs + "  " + "Valor: "
        str1 = tabs + "Elemento: " + strs + str(self.expr) + "\n" + str1
        contador = contador - 1
        return str0 + str1


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
                str_ = str_ + ";"
        return str_

# Clase para BLOQUE
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
                    
