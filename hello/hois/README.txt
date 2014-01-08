Proyecto, Fase 2: Análisis Sintáctico y Árbol Sintáctico Abstracto

Melecio Ponte: 08-10893
Gabriel Formica: 10-11036

    Para la realización de un analizado sintactico del lenguaje RangeX, se uso
el lenguaje Python. Además de este lenguaje, se usó la libería PLY, específicamente
del módulo YACC, el cual brinda las herramientas necesarias para facilitar esta
tarea. Se mantiene el uso PLY para el análisis lexicográfico de la primera entrega.

    Para este análisis, se construyo una gramática libre de contexto la cual se en-
carga de traducir las reglas del lenguaje dado a objetos que puede el analizador ma-
nejar para construir el árbol. Dicha gramática se encuentra especificada en un ar-
chivo adjunto.

    Se presenta un problema de shift/reduce que involucra la instrucción de if/then/
else. El problema ocurre cuando se presenta una expresión de la siguiente 
forma:

                [TkIf exp TkThen instruction . TkElse]

donde el punto (.) separa la pila del próximo token, existe un conflicto respecto a 
si «shiftear» el TkElse o reducir la expresión «TkIf exp TkThen instruction» a una 
«instruction». Se decide mantener esta falla sin resolver debido a que el parser por
defecto siempre escogerá shiftear, lo cual es conveniente en este contexto. Es
decir, nunca habra una estructura válida de la forma «instruction TkElse».

     Para el análisis estático se utilizaron dos variables globales:
	-stack: que es una pila de tablas de símbolos.
	-static_analysis: que es un string en donde se tienen todos los errores
			semánticos encontrados en dicho análisis. 
Los errores de análisis estáticos se van buscando simultaneamente se parsea.
Cada tabla de símbolos va almacenandose en stack. La variable global stack,
facilita en gran medida saber qué variables pertenecen a qué bloques, pues basta 
con que la instrucción de un bloque se redusca para que la tablas de símbolos 
(de existir) declarada sea eliminada de la pila. 

