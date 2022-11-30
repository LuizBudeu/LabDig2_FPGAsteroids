from usuario import *
import os
from datetime import datetime

nome = "logs/"+ user + "_log.csv"
nomeMQTT = "logs/"+ user + "_MQTTlog.csv"

def cria_logs():
	# Cria pasta "logs" caso ela nao exista
	try:
		os.mkdir("logs")
	except OSError as e:
		pass

    # Cria arquivo logs caso ele nao exista
	if not(os.path.isfile(nome)):
		f = open(nome, "w")
		f.write("data,arquivo,evento\n")
		f.close()

	# Cria arquivos logsMQTT caso ele nao exista
	if not(os.path.isfile(nomeMQTT)):
		f = open(nomeMQTT, "w")
		f.write("tempo,topico,conteudo\n")
		f.close()

def escreve_log(texto):
	if "Scripts" in str(os.path.basename(os.getcwd())): 
		f = open(nome, "a")
	else:
		f = open("../" + nome, "a")
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	f.write(dt_string + "," + texto + "\n")

	f.close()