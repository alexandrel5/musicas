#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

def baixarvideo(nomevideo, linkvideo, diretoriov):
	resu = ['','']

	try:
		#
		# Implementar a verificacao se ja existe o arquivo no futuro BD
		#
		subprocess.call(["youtube-dl", "-o", nomevideo, "-f", "flv", linkvideo], cwd=diretoriov) #diretoriov variavel vem do arquivo constantes
		#subprocess.call(["youtube-dl", "-o", "teste.flv", "-f", "flv", "http://www.youtube.com/watch?v=2ApkOkhp2vg"], cwd='/home/alexandre/videos/')	
	except Exception, e:
		resu[0] = False
		resu[1]	= 'Erro ao baixar video'
	else:
		resu[0] = True
		resu[1]	= 'Sucesso ao baixar video'
	finally:
		return resu
	