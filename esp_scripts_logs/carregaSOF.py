# ====================================================================
# Carga do executavel (.sof) na placa FPGA
# ====================================================================
import os
import sys
from client_mqtt import *
from log import *

arquivo = "Carregar SOF"

if len(sys.argv) != 2:
    escreve_terminal("O numero de agumentos eh invalido!")
    escreve_terminal("O script devera ser executado como:")
    escreve_terminal("       python carregaSOF.py nome_do_projeto")
    escreve_log(arquivo + "," + "Numero de argumentos incorreto")
    sys.exit()
    
projeto = sys.argv[1]   # Nome do projeto

escreve_terminal("Carregando arquivo sof na placa FPGA")

comando = "quartus_pgm -c usb-blaster -m JTAG -o p;" + projeto + ".sof"

if os.system(comando) != 3:
    escreve_terminal("O arquivo sof foi carregado com sucesso")
    escreve_log(arquivo + "," + "SOF carregado")
else:
    escreve_terminal("Erro na carga do arquivo sof. Verifique se o nome do sof e o nome do projeto sao iguais")
    escreve_log(arquivo + "," + "Erro na carga do SOF")
    sys.exit()