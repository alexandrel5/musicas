#!/usr/bin/env python
# -*- coding: utf-8 -*-

import verifications
import downloadvi
import conversor
import constantes

nomevideoConst = ''
nomevideo = ''
nomemp3 = '' 
idvideo = ''
l_imgvideo = ''

error = ''

#link = 'http://www.youtube.com/watch?v=1nM-6rYXJB0'
#link = 'http://www.youtube.com/watch?v=vgZwa7GKRCA'# 
link = 'http://www.youtube.com/watch?v=kMKgHFEyx80'
#link = raw_input('Digite o link')

p = verifications.urlid(link)# retorna true, menssagem, idvideo
print 'verifications.urlid'
print p[1]
print p[2]
if p[0]:
	p = verifications.getdados(p[2])#passa p[2] link video como referencia e retorna p[0] true, p[1] mensagem, p[2]constante nome video, p[3] nome video, p[4] l_imgvideo
	
	l_imgvideo = p[4]#colocar l_imgvideo na variavel l_imgvideo pois vai ser resetada na proxima ocorrenicia
	print 'verifications.getdados'
	print p[1]
	print p[2]
	print p[3]
	print p[4]

	if p[0]:
		p = verifications.nomevideo(p[3], constantes.diretoriov)# passa p[4]nomevideo, diretoriov e retorna  p[0] true, p[1] mensagem, p[2] nomemp3, p[3] nomevideo
		
		nomevideo = p[3]# colocar nomevideo na variavel nomevideo pois vai ser resetada na proxima ocorreicia
		nomemp3 = p[2]# colocar nomemp3 na variavel nomemp3 pois vai ser resetada na proxima ocorreicia
		print 'verifications.nomevideo'
		print p[1]
		print p[2]
		print p[3]

		if p[0]:
			p = downloadvi.baixarvideo(p[3], link, constantes.diretoriov)#passa nome do video e link, diretoriov
			print 'verifications.baixarvideo'
			print p[1]

			#print constantes.diretoriov
			#print nomevideo
			#print nomemp3
			#print constantes.diretoriom

			if p[0]:
				p = conversor.gerarmp3(constantes.diretoriov, nomevideo, nomemp3, constantes.diretoriom)#passa diretoriov, nomevideo, nomemp3, diretoriom

				if p[not p[0]]:#verifica se conversor.gerarmp3 deu erro
					error = p[1]#

			else:
				error = p[1] #p[1] verifica se downloadvi.baixarvideo deu erro

		else:
			error = p[1] #p[1] verifica se verifications.nomevideo deu erro

	else:
		error = p[1] #p[1] verifica se verifications.getdados deu erro				

else:
	error = p[1] #p[1] verifica se verifications.urlid deu erro

print error