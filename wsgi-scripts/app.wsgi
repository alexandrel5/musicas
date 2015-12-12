#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from cgi import parse_qs, escape
from webob import Request
from string import Template

import sys
import json
sys.path.append('/var/www/wsgi-scripts/')#coloca no python path a referencia da pasta wsgi-scripts pois wsgi nao consegue importar os arquivo constantes, verifications, downloadvi, conversor. Acho que wsgi nao inicializa na mesma pasta
import constantes
import verifications
import downloadvi
import conversor
import bancodados

class htmlpgs(object):
    """docstring for htmlpgsme"""

    def index(self, paginas='', lista_resp_a='', input_text=''):

        pag_html = Template("""

            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>Urrar</title>
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">

                    <script src="media/js/jquery-1.10.2.js"></script>
                    <link href="media/css/bootstrap.min.css" rel="stylesheet">
                    <script src="media/js/bootstrap.min.js"></script>

                    <link rel="Stylesheet" href="media/css/style.css" />
                    <script src="media/js/script.js"></script>

                </head>
                <body>
                    <div id='root'>
                        <!--<div class='box' id='menu'>
                        Menu
                        </div>-->
                        <div class='box' id='principal'>
                            <div id="logo">
                                <h1>Urrar</h1>
                            </div>
                            <div class='f-busca'>
                                <form action="/search?" method="GET" class="form-inline" role="form">
                                    <div class="form-group col-xs-9">
                                        <input type="text" class="form-control" id="i-q" name="q" value="$input_text" placeholder="Busca" >
                                    </div>
                                    <button type="submit" class="btn btn-success" id="b-submit">
                                        <span class="glyphicon glyphicon-search"></span> Buscar
                                    </button>
                                </form>
                            </div>
                            <div class="conversor-div">
                                <div id="conversor-progress" class="progress">
                                    <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%;">
                                            <span class="sr-only">60% Complete</span>
                                    </div>
                                </div>
                                <div id="gif-carregando">
                                    <img src="media/images/carregando.gif" >
                                </div>
                                <div id="conversor-down" class='conversor-dow'>
                                    <a id="bt-down-mp3" href="#" class="btn btn-success active" role="button" download>Download MP3</a>
                                    <a id="bt-down-video" href="#" class="btn btn-success active" role="button" download>Download Video</a>
                                </div>
                            </div>
                        </div>
                        <div class='box' id='lista'>
                            <div class='box' id='listaa'>
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr><th colspan="2">Nome</th><th>Tamanho</th><th>Player</th><th>Download</th></tr>
                                        </thead>
                                        <tbody>
                                            $listaa
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div id="paginacao">
                                <ul class="pagination pagination-sm" id="paginacao-ul">
                                    $paginas
                                </ul>
                            </div>
                        </div>
                        <div id='rodape'>
                        rodape
                        </div>
                    </div>
                </body>
            </html>

        """ )

        resu = pag_html.substitute(paginas=paginas, listaa=lista_resp_a, input_text=input_text)

        return resu

    def nofound(self):
        pag_html="""
        <html>
            <head>
                <title>Pagina nao encontrada</title>
            </head>
            <body>
                <p>Pagina nao encontrada</p>
            </body>
        </html>
        """
        return pag_html

def inicio():

    pg = htmlpgs()
    pag_html = pg.index()
    response_body = pag_html #% ('#', '#', '#')
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]

    return [response_headers,response_body]

def converter(URL):

    resp = {
        "erro": {
            "erro": "false",
            "menssagem": "No Erro"
        },
        "links": {
            "mp3": "",
            "video": ""
        }
    }

    Categoria=''
    Banda=''

    id_musica=''
    Nomevideo = ''
    nomemp3 = ''
    idvideo = r''
    p = ''


    p = verifications.urlid(URL)# retorna true, menssagem, idvideo
    idvideo = p[2]
    try:
        data = bancodados.arquivos()
        check_id_youtube = data.check_id_youtube(idyoutube=p[2])

    except Exception, e:
        resp["erro"]["erro"] = 'true'
        resp["erro"]["menssagem"] = 'Erro ao checar se o video já esta disponivel no banco de dados '
        response_body = json.dumps(resp)#transforma json em string
        return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]
    else:
        if len(check_id_youtube) > 0:
            linkmp3 = 'musica?id='+str(check_id_youtube[0]['_id'])
            linkvideo = 'downloads/videos/'+Nomevideo

            resp["links"]["mp3"] = linkmp3
            resp["links"]["video"] = linkvideo

            response_body = json.dumps(resp) #transforma json em string
            response_headers = [('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))]

            return [response_headers,response_body]

    if p[0]:
        p = verifications.getdados(p[2])#passa p[2] link video como referencia e retorna p[0] true, p[1] mensagem, p[2]constante nome video, p[3] nome video, p[4] l_imgvideo

        if p[0]:
            p = verifications.nomevideo(p[3], constantes.diretoriov)# passa p[3]Nomevideo, diretoriov e retorna  p[0] true, p[1] mensagem, p[2] nomemp3, p[3] Nomevideo
            Nomevideo = p[3]# colocar Nomevideo na variavel Nomevideo pois vai ser resetada na proxima ocorreicia
            nomemp3 = p[2]# colocar nomemp3 na variavel nomemp3 pois vai ser resetada na proxima ocorreicia

            if p[0]:
                p = downloadvi.baixarvideo(p[3], URL, constantes.diretoriov)#passa nome do video e link, diretoriov

                if p[0]:
                    p = conversor.gerarmp3(constantes.diretoriov, Nomevideo, nomemp3, constantes.diretoriom)#passa diretoriov, Nomevideo, nomemp3, diretoriom

                    if p[p[0]]:#verifica se conversor.gerarmp3 deu erro

                        try:
                            mus = open('/var/www/urrar/downloads/musicas/'+nomemp3)
                            data = bancodados.arquivos()
                            id_musica = data.save(arquivo=mus, filename=nomemp3, Banda=Banda, Categoria=Categoria, referencia_id=idvideo)
                            mus.close()
                        except Exception, e :
                            resp["erro"]["erro"] = 'true'
                            resp["erro"]["menssagem"] = 'erro ao salvar' #'Erro ao salvar arquivo no BD'
                            response_body = json.dumps(resp)#transforma json em string
                            return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]
                        else:
                            linkmp3 = 'musica?id='+str(id_musica)
                            linkvideo = 'downloads/videos/'+Nomevideo

                        resp["links"]["mp3"] = linkmp3
                        resp["links"]["video"] = linkvideo
                        #finally:
                        #	pass

                    else:
                        resp["erro"]["erro"] = 'true'
                        resp["erro"]["menssagem"] = p[1]
                        response_body = json.dumps(resp)#transforma json em string
                        return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]
                else:
                    resp["erro"]["erro"] = 'true'
                    resp["erro"]["menssagem"] = p[1] #p[1] verifica se downloadvi.baixarvideo deu erro
                    response_body = json.dumps(resp)#transforma json em string
                    return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]

            else:
                resp["erro"]["erro"] = 'true'
                resp["erro"]["menssagem"] = p[1] #p[1] verifica se verifications.Nomevideo deu erro
                response_body = json.dumps(resp)#transforma json em string
                return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]

        else:
            resp["erro"]["erro"] = 'true'
            resp["erro"]["menssagem"] = p[1] #p[1] verifica se verifications.getdados deu erro
            response_body = json.dumps(resp)#transforma json em string
            return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]

    else:
            resp["erro"]["erro"] = 'true'
            resp["erro"]["menssagem"] = p[1] #p[1] verifica se verifications.urlid deu erro
            response_body = json.dumps(resp)#transforma json em string
            return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]


    response_body = json.dumps(resp) #transforma json em string
    response_headers = [('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))]

    return [response_headers,response_body]

def download(id_musica):

    data = bancodados.arquivos()
    OBjetmusica = data.download(id_musica)

    musica = OBjetmusica.read()
    nomemusic = OBjetmusica.filename.encode()

    response_body = musica

    response_headers = [('Content-type', 'audio/mpeg'), ('Content-Disposition', 'attachment; filename='+str(nomemusic)), ('Content-Length', str(len(response_body)))]

    return [response_headers,response_body]

def busca(query, start=0, limite=15, return_type=''): #j = json

    resp=''

    try:
        start = int(start)
    except Exception, e:
        start = 0


    if return_type=='json' :

        pagi = Template("""
                           <div class='box' id='listaa'>
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr><th colspan="2">Nome</th><th>Tamanho</th><th>Player</th><th>Download</th></tr>
                                        </thead>
                                        <tbody>
                                            $listaa
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div id="paginacao">
                                <ul class="pagination pagination-sm" id="paginacao-ul">
                                    $paginas
                                </ul>
                            </div>
        """)

        data = bancodados.arquivos()
        nresultado = data.listar(query=query, nresultado=True)
        nresultado = len(nresultado)

        tag_n_paginas = r""
        lista_resp = r""

        npag = (nresultado/limite)+1
        if nresultado%limite != 0: npag = npag+1

        lim = 0
        for x in range(1, npag):
            tag_n_paginas = tag_n_paginas + r"<li><a href='/search?q="+str(query)+"&start="+str(lim)+"'>"+str(x)+"</a></li>"
            lim = lim+limite
            #tag_n_paginas = tag_n_paginas + r"<li><a href='/search?q="+str(query)+"&lim="+str(limite)+"&pag="+str(x)+"'>"+str(x)+"</a></li>"


        musicas = data.listar(query=query, start=start)

        for x in musicas:

            filename = str(x['filename']).encode("UTF-8")
            length = str(x['length']).encode("UTF-8")#Tamanho
            id_musica = str(x['_id']).encode("UTF-8")

            download=r'musica?id='+id_musica

            lista = r"<tr><td colspan='2'>%s</td><td>%s</td><td>Play</td><td><a href='%s' title='Download musica'><img height='16' width='16' src='media/images/download.png' border='0' alt='Download Musica'></a></td></tr>"

            lista_resp = lista_resp + lista % (filename, length, download)

        resu = pagi.substitute(paginas=tag_n_paginas, listaa=lista_resp)

    elif return_type=='':

        data = bancodados.arquivos()
        nresultado = data.listar(query=query, nresultado=True)
        nresultado = len(nresultado)

        tag_n_paginas = r""
        lista_resp = r""

        npag = (nresultado/limite)+1
        if nresultado%limite != 0: npag = npag+1

        lim = 0
        for x in range(1, npag):
            tag_n_paginas = tag_n_paginas + r"<li><a href='/search?q="+str(query)+"&start="+str(lim)+"'>"+str(x)+"</a></li>"
            lim = lim+limite
            #tag_n_paginas = tag_n_paginas + r"<li><a href='/search?q="+str(query)+"&lim="+str(limite)+"&pag="+str(x)+"'>"+str(x)+"</a></li>"


        musicas = data.listar(query=query, start=start)

        for x in musicas:

            filename = str(x['filename']).encode("UTF-8")
            length = str(x['length']).encode("UTF-8")#Tamanho
            id_musica = str(x['_id']).encode("UTF-8")

            download=r'musica?id='+id_musica

            lista = r"<tr><td colspan='2'>%s</td><td>%s</td><td>Play</td><td><a href='%s' title='Download musica'><img height='16' width='16' src='media/images/download.png' border='0' alt='Download Musica'></a></td></tr>"

            lista_resp = lista_resp + lista % (filename, length, download)

        #print lista_resp
        #print tag_n_paginas

        pg = htmlpgs()
        resu = pg.index(paginas=tag_n_paginas, lista_resp_a=lista_resp, input_text=str(query))

    response_body = resu
    response_headers = [('Content-type', 'text/html; charset=UTF-8'), ('Content-Length', str(len(response_body)))]

    return [response_headers,response_body]

def progresso(idprogress):

    #progresso = bancodados.arquivos()
    #resp = progresso.progressbarConsulta(idprogress)

    value = u'ú@#ç$%aáóéãõÃáóéÕ'.encode("UTF-8")

    response_body = value

    return [[('Content-type', 'application/json; charset=UTF-8'), ('Content-Length', str(len(response_body)))], response_body]


def nofound():
    pg = htmlpgs()
    pag_html = pg.nofound()
    response_body = pag_html
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]

    return [response_headers,response_body]

def application(environ, start_response):

    # the environment variable CONTENT_LENGTH may be empty or missing

    response_body=''
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]

    if environ['REQUEST_METHOD'].upper() == 'GET' and environ['PATH_INFO'].lower() == '/': #index

        resp = inicio()
        response_body = resp[1]
        response_headers = resp[0]

    elif environ['REQUEST_METHOD'].upper() == 'GET' and environ['PATH_INFO'].lower() == '/converter': #conversor

        req = Request(environ)
        URL = req.params.get('q','default').encode("utf-8")

        resp = converter(URL=URL)

        response_body = resp[1]
        response_headers = resp[0]

    elif environ['REQUEST_METHOD'].upper() == 'GET' and environ['PATH_INFO'].lower() == '/musica': #Download

        req = Request(environ)#aqui chega todas as requisicoes
        id_musica = req.params.get('id', 'default').encode("UTF-8")

        resp = download(id_musica)

        response_body = resp[1]
        response_headers = resp[0]

    elif environ['REQUEST_METHOD'].upper() == 'GET' and environ['PATH_INFO'].lower() == '/search': #busca
        resp = ['','']
        sites = ['youtu.be', 'youtube.be', 'www.youtube.com', 'm.youtube.com']

        req = Request(environ)#aqui chega todas as requisicoes
        q = req.params.get('q', '').encode("UTF-8")
        start = req.params.get('start', '0').encode("UTF-8")
        return_type = req.params.get('type', '').encode("UTF-8")

        import urlparse
        u = urlparse.urlparse(q)#divide a query em varias partes para verificar se contem algum site

        if u.netloc in sites: # verifica se query passada contem algum site
            resp = converter(URL=q)
        else:
            resp = busca(query=q, start=start, return_type=return_type)

        response_body = resp[1]
        response_headers = resp[0]

    elif environ['REQUEST_METHOD'].upper() == 'GET' and environ['PATH_INFO'].lower() == '/progress': #progresso da conversao


        req = Request(environ)#aqui chega todas as requisicoes
        idprogress = req.params.get('id', '').encode("UTF-8")

        resp = progresso(idprogress)

        response_body = resp[1]
        response_headers = resp[0]

    elif environ['REQUEST_METHOD'].upper() == 'GET': #Pagina nao encontrada

        resp = nofound()
        response_body = resp[1]
        response_headers = resp[0]


    status = '200 OK'

    start_response(status, response_headers)

    return [response_body]
