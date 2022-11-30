# ====================================================================
# Script para compilar e carregar script do ESP8266
# ====================================================================
# 1 eh o codigo de erro retornado pelo os.system() caso ambos os comandos do arduino-cli deem errado
# sys.exit() ira retornar 2 na chamada os.system() do main.py indicando erro na execucao
from cmath import log
import os
import sys
from client_mqtt import *
from usuario import *
from log import *

arquivo = "Arduíno" 
logMessage = ""

escreve_terminal("Comencando processo de compilacao e carga do script do ESP8266")



# Altera o usuario/senha no script do esp8266
try:
    f1 = open("mqtt_esp8266/mqtt_esp8266.ino", "r")
except OSError as e:
    escreve_terminal("Script do ESP8266 nao encontrado")
    escreve_log(arquivo + "," + "Scrip do ESP8266 nao encontrado")
    sys.exit(2)
    
linhas = f1.readlines()
f1.close()

f1 = open("mqtt_esp8266/mqtt_esp8266.ino", "w")
for linha in linhas:
    if "String user" in linha:
        texto = 'String user = "' + user + '";\n'
        f1.write(texto)
    elif "String passwd" in linha:
        texto = 'String passwd = "' + passwd + '";\n'
        f1.write(texto)        
    else:
        f1.write(linha)
f1.close()

# Compila o script
if os.system("arduino-cli compile --fqbn esp8266:esp8266:nodemcuv2 mqtt_esp8266") != 1:
    escreve_terminal("O script do ESP8266 foi compilado com sucesso") 
else:
    escreve_terminal("Erro no processo de compilacao do script do ESP8266") 
    escreve_log(arquivo + "," + "Erro de compilacao do Script do ESP8266")
    sys.exit(2)
    
# Localiza a porta COM que esta conectada ao ESP8266
os.system("arduino-cli board list > log.txt")
f1 = open("log.txt", "r")
linhas = f1.readlines()
linha = linhas[2]
porta = linha.split(" ")[0]
f1.close()
os.remove("log.txt")

escreve_terminal("A porta identificada do ESP8266 foi a " + porta)

# Carrega o script
if os.system("arduino-cli upload -p " + porta + " --fqbn esp8266:esp8266:nodemcuv2 mqtt_esp8266") != 1:
    escreve_terminal("O script do ESP8266 foi carregado com sucesso")
    escreve_log(arquivo + "," + "Scrip do ESP8266 carregado com sucesso")
else:
    escreve_terminal("Erro no processo de carga do script do ESP8266") 
    escreve_log(arquivo + "," + "Erro de carregamento do script do ESP8266")
    sys.exit(2)