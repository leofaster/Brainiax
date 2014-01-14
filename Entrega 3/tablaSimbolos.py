#!/usr/bin/env python
#coding: utf8 
# Analisis Sintactico del lenguaje Brainiac.
# Modulo: symtable
# Autores:  Wilthew, Patricia    09-10910
#           Leopoldo Pimentel    06-40095

class symtable:

    def __init__(self):
	    self.dic = {}

    def insert(self,key,value):
	    self.dic[key] = value 

    def delete(self,elem):
	    if self.dic.isMember(elem):
		    del self.dic[str(elem)]		

    def update(self,elem,type):
	    if self.dic.isMember(elem):
		    self.dic[str(elem)] = type

    def isMember(self,key):
	    if key in self.dic:
		    return True
	    return False

    def find(self,elem):
	    return self.dic[str(elem)]

    def get(self):
	    return self.dic

    def isEmpty(self):
	    return len(self.dic.keys()) == 0

    def goesTo(self,key,value):
	    return self.dic[key] == value	

    def cloneSymtable(self):
	    d = symtable()
	    d.dic = self.get()
	    return d
		
