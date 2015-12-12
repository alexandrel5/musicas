#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

def gerarmp3(diretoriov, nomevideo, nomemp3, diretoriom):
	resu = ['','']

	try:
		subprocess.call(["ffmpeg", "-i", diretoriov+nomevideo, "-f", "mp3", nomemp3], cwd=diretoriom) #diretoriov, diretoriom variavel vem do arquivo constantes
		#subprocess.call(["ffmpeg", "-i", "/home/alexandre/videos/file.flv", "-f", "mp3", "nomefile.mp3"], cwd="/home/alexandre/musicas") #diretoriom variavel vem do arquivo constantes
	except Exception, e:
		resu[0] = False
		resu[1]	= 'Erro ao converter video'
	else:
		resu[0] = True
		resu[1]	= 'Sucesso ao converter video'
	finally:
		return resu