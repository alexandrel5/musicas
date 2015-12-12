#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import gridfs
import hashlib
from functools import partial

class arquivos(object):
	"""Banco de dados MongoDB+ GridFS"""

	def md5sum(self, filename):
		with open('/var/www/urrar/downloads/musicas/'+filename, mode='rb') as f:
			d = hashlib.md5()
			for buf in iter(partial(f.read, 128), b''):
				d.update(buf)
		return d.hexdigest()

	def progressbarSave(self, idprogress, value=1):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados

		arq = db.barprogress.insert({"_id": idprogress, "value": value})

		return arq

	def progressbarConsulta(self, idprogress):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados

		arq = list(db.barprogress.find({'_id' : idprogress}))									

		return arq

	def progressbarUpdate(self, idprogress, value, fileid='', filename=''):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados

		arq = db.barprogress.update({"_id": idprogress}, {"$set": {"value":value, "fileid":fileid, "filename":filename}})

		return arq

	def save(self, arquivo, filename, Banda, Categoria, referencia_id):
		arq=''
		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados
		fs = gridfs.GridFS(db) #collection (optional): root collection to use

		md5 = self.md5sum(filename)

		md5check = list(db.fs.files.find({'md5' : md5}))

		if len(md5check) > 0:
			return md5check[0]['_id']
		else:		
			conn = pymongo.Connection('localhost', 27017) #####$$$$ busca id para a musica no bd
			db = conn.music #Cria o banco de dados
			db = db.idmusic #mesma coisa db = cliente['idmusic'] # nome do Documento o mesmo que tabela Nome do collection
			id_musica = db.find_one({'used': 0})
			id_musica = id_musica['_id'].encode()
			db.update({'_id': id_musica}, {'used:': 1}) # atualiza a collection id_musica e marca o id como usado

			conn = pymongo.Connection('localhost', 27017)
			db = conn.Music_List_Arquivos #Cria o banco de dados
			fs = gridfs.GridFS(db) #collection (optional): root collection to use
			arq = fs.put(arquivo.read(), _id=id_musica, filename=filename, contentType='mp3', Banda=Banda, Categoria=Categoria, referencia_id=referencia_id)

		return arq

	def check_id_youtube(self, idyoutube=''):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados
		fs = gridfs.GridFS(db)

		resp = list(db.fs.files.find({'referencia_id' : str(idyoutube)}))

		return resp


	def delete(self, file_id):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados
		fs = gridfs.GridFS(db) #collection (optional): root collection to use
		arq = fs.delete(file_id)


	def update(self):
		pass

	def download(self, file_id):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados
		fs = gridfs.GridFS(db) #collection (optional): root collection to use
		#arq = fs.get(file_id).read()
		arq = fs.get(file_id)

		return arq


	def listar(self, query='', start=0, limite=15, nresultado=False):

		conn = pymongo.Connection('localhost', 27017)
		db = conn.Music_List_Arquivos #Cria o banco de dados
		fs = gridfs.GridFS(db)

		arquivos = ""

		if nresultado :                                                                        # skip = quantos resultados a pular, limit resultado a mostrar
			#arquivos = list(db.fs.files.find({'filename':{'$regex': query+'*','$options': 'i'}}).skip(0).limit(0))
			arquivos = list(db.fs.files.find({'filename':{'$regex': query+'*','$options': 'i'}}).skip(0).limit(0))
		else:
			#arquivos = list(db.fs.files.find({'filename':{'$regex': query+'*','$options': 'i'}}).skip(pag).limit(limite))
			arquivos = list(db.fs.files.find({'filename':{'$regex': query+'*','$options': 'i'}}).skip(start).limit(limite))


		return arquivos


#musica = open('ADAO.mp3')

#bd = arquivos()
#id_musica = bd.save(musica.read())
#print musica.read()
#musica.close()

#print id_musica
#print type(id_musica)

#musica = bd.download(id_musica)
#print musica