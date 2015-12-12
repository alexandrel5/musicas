

s_recebida = 'casamen'
tam = len(s_recebida)
porcentagem = 100 / tam #arrumar para nao dar exceção da divisao por zero
s_lista = {'casa':0, 'bola':0, 'asa':0, 'amor':0, 'camila':0, 'dora':0, 'casamento':0}

for r in s_recebida: #percorre a string recebida
	for l in s_lista: #percorre a lista de palavras armazenadas localmente 
		if r in l : #letra de string recebida esta contida em palavra armazenada localmente
			s_lista[r] = s_lista[r] + porcentagem