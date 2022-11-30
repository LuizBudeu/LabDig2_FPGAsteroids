# ====================================================================
# Script top
# ====================================================================
import os
from client_mqtt import *
from log import *

arquivo = "Main"

def menu():
    escreve_terminal("==========================================================================")
    escreve_terminal("Bem vindo ao script do LabEAD")
    escreve_terminal("==========================================================================")
    escreve_terminal("Digite 'projeto'  ou 'pr' para mudar o nome do projeto")
    escreve_terminal("Digite 'compilar' ou 'co' para compilar um projeto qar")
    escreve_terminal("Digite 'carregar' ou 'ca' para carregar um projeto na placa FPGA")
    escreve_terminal("Digite 'esp8266'  ou 'es' para carregar o script no esp8266")
    escreve_terminal("Digite 'sof'      ou 'cs' para carregar um arquivo SOF na placa FPGA")
    escreve_terminal("Digite 'mostrar'  ou 'm'  para mostrar o nome atual do projeto")    
    escreve_terminal("Digite 'ajudar'   ou 'a'  para mostrar novamente esse menu")
    escreve_terminal("Digite 'sair'     ou 's'  para sair do script")
    escreve_terminal("==========================================================================")

cria_logs()

while(True):
    carga = False
    compila = False
    projeto = ""

    escreve_terminal("\nDigite 'iniciar' ou 'i' para comecar a execucao do script")
    text = le_terminal();

    if text == "iniciar" or text == "i":
        menu()

        while(True):   
            text = le_terminal();

            if text == "projeto" or text == "pr":
                escreve_terminal("Digite o nome do projeto (nome do arquivo qar)")
                projeto = le_terminal();

                while(" " in projeto or "." in projeto):
                    escreve_terminal("Digite o nome do projeto sem espacos nem extensao (.)")
                    projeto = le_terminal();  

                compila = False

            elif text == "compilar" or text == "co":
                if projeto == "":
                    escreve_terminal("Voce ainda nao configurou o nome do projeto")
                else:
                    comando = "python compila.py " + projeto
                    if os.system(comando) != 2:
                        compila = True

            elif text == "carregar" or text == "ca":
                if compila == True:
                    comando = "python carrega.py " + projeto 
                    os.system(comando)
                else:
                    escreve_terminal("Voce ainda nao compilou o projeto")  

            elif text == "esp8266" or text == "es":
                if carga == True:
                    escreve_terminal("Voce ja fez a carga do script no esp8266")
                else:
                    if os.system("python arduino.py") != 2:
                        carga = True

            elif text == "sof" or text == "cs":
                if projeto == "":
                    escreve_terminal("Voce ainda nao configurou o nome do projeto")
                else:
                    comando = "python carregaSOF.py " + projeto
                    os.system(comando)

            elif text == "mostrar" or text == "m":
                escreve_terminal("Projeto: " + projeto)

            elif text == "ajudar" or text == "a":
                menu()

            elif text == "sair" or text == "s":
                escreve_terminal("Saindo do script top")
                break

            else:
                escreve_terminal("Comando invalido. Digite 'ajudar' ou 'a' para mostrar novamente os comandos validos")
                escreve_log(arquivo + "," + "Comando invalido")
            if text != "ajudar" and text != "a":
                escreve_terminal("==========================================================================")
                escreve_terminal("Voce esta no menu do script do LabEAD")
                escreve_terminal("==========================================================================")

    else:
        escreve_terminal("Comando invalido")        
        escreve_log(arquivo + "," + "Comando invalido")