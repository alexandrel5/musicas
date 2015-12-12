#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import itertools

conn = pymongo.Connection('localhost', 27017)
db = conn.music #Cria o banco de dados
idmusic = db.idmusic #mesma coisa db = cliente['idmusic'] # nome do Documento o mesmo que tabela Nome do collection

#idmusic_extrutura = {
#	'_id' : '',
#	'used' : 0 # 0 = false e 1 = true
#}


letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
letrasUP=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
caracters=['-','_']
numerais = ['0','1','2','3','4','5','6','7','8','9']

random = letras+letrasUP+caracters+numerais

e = itertools.permutations(random, 2) # retorna um objeto do tipo interable

for x in e:	
	idmusic_extrutura = {
		'_id' : ''.join(x),
		'used' : 0
	}

	print idmusic.insert(idmusic_extrutura)


