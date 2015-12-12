#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import urllib2 #Conecta-se na net para obter a arquivo json
import urlparse #Divide as e pega sa partes da URl
import unicodedata

nomevideoConst = ''
nomevideo = ''
nomemp3 = '' 
l_imgvideo = ''

def urlid(url):#recebe o link do video e retorna o id
	
	resu = ['','','']#true, menssagem, idvideo
	u = ""

	try:
		u = urlparse.urlparse(url)#'http://www.youtube.com/watch?v=5FA7koItcnQ'
	except Exception, e:
		resu[0] = False
		resu[1]	= 'Erro ao extrair id do video urlparse nao se conecta ao site'
	else:
		if u.netloc == 'youtu.be':
			resu[2] = u.path[1:].split('&')[0]#idvideo
			#print u.path[1:]
		elif u.netloc == 'youtube.be':
			resu[2] = u.path[1:].split('&')[0]#idvideo
			#print u.path[1:]
		elif u.netloc == 'www.youtube.com':			
			resu[2] = u.query[2:].split('&')[0]#idvideo
			#print idvideo
		elif u.netloc == 'm.youtube.com':			
			resu[2] = u.query[2:].split('&')[0]#idvideo
			#print idvideo
		resu[0] = True
		resu[1]	= 'Sucesso ao extrair id do video'
	finally:
		return resu

def getdados(idvideo):#recebe id, obtem os dadaos do video(nome, image_miniatura em forma de link)
	
	link = "http://gdata.youtube.com/feeds/api/videos/"+idvideo+"?v=2&alt=jsonc"# exemplo http://gdata.youtube.com/feeds/api/videos/vgZwa7GKRCA?v=2&alt=jsonc	
	resu = ['','','','',''] #true, mensagem, nomevideoconstante, nomevideo, link miniatura imagem video

	try:
		req = urllib2.Request(link)
		req.add_header('User-Agent', 'Brasil') # Modifica o user-agent
		f = urllib2.urlopen(req) # Faz o Download

		data = json.loads(f.read()) #transforma string json em objeto json
		d = data['data']['title']
		d = unicodedata.normalize('NFKD', d).encode('ASCII','ignore')
		resu[2] = d # pega nomevideoConst
		resu[3] = d # pega nome video
		resu[4] = data['data']['thumbnail']['sqDefault']# pega l_imgvideo
		
	except urllib2.HTTPError, e:
		resu[0] = False
		resu[1] = 'HTTP Error:', e.code, url
	except urllib2.HTTPError, e:
		resu[0] = False
		resu[1] = 'URL Error:', e.reason, url
	except Exception, e:
		resu[0] = False
		resu[1] = 'Erro ao buscar dados do video'
		#resu[1] = idvideo
	else:
		resu[0] = True
		resu[1]	= 'Sucesso ao buscar dados do video'
	finally:
		return resu


def nomevideo(nomevideo, diretoriov):# retira do nome caracteres(" ", "'", '"') e verifica se ja tem o video no pc
	
	no = ''
	resu = ['', '', '', '']#true,mensagem, nomevideo, nomemp3

	try:
		#no = unicodedata.normalize('NFKD', nomevideo.decode('utf-8')).encode('ASCII','ignore')

		nomevideo = nomevideo.replace(" ","_")

		nomevideo = nomevideo.translate(None, r"(\\/:,*?<>| +"')[]#=.') # r'' informa para python que é para interpretar cada caracteres individualmente

		if len(nomevideo) > 150: #Limita o numero de caracteres no nome
			nomevideo = nomevideo[:150]
		
		resu[2] = nomevideo+".mp3" #Gera nome musica
		resu[3] = nomevideo+".flv" #Gera nome video

		if not os.path.exists(diretoriov+nomevideo):#Retorna true se existir esse arquivo
			resu[0] = True
			resu[1]	= 'Arquivo não existe'
	except Exception, e:
			resu[0] = False
			resu[1]	= 'Arquivo existe'
	finally:
		return resu

 		
#resu = urlid('http://www.youtube.com/watch?v=TtB0JnJImGQ')
#print resu[0]
#print resu[1]
#print resu[2]