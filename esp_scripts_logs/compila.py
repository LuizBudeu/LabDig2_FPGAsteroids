# ====================================================================
# Script para compilar projeto do Quartus
# ====================================================================
# sys.exit() ira retornar 2 na chamada os.system() do main.py indicando erro na execucao
import os
import sys
import shutil
from client_mqtt import *
from log import *

arquivo = "Compila"

# pinos validos para utilizar da placa FPGA DE0-CV (clocks, leds, displays e GPIOs)
pinos = ["N16", "B16", "M16", "C16", "D17", "K20", "K21", "K22", "M20", "M21",
         "N21", "R22", "R21", "T22", "N20", "N19", "M22", "P19", "L22", "P17",
         "P16", "M18", "L18", "L17", "L19", "K17", "K19", "P18", "R15", "R17",
         "R16", "T20", "T19", "T18", "T17", "T15",  "M9", "H13", "E10", "V15", 
         "H16", "A12", "H15", "B12", "A13", "B13", "C13", "D13", "G18", "G17",
         "H18", "J18", "J19", "G11", "H10", "J11", "H14", "A15", "J13",  "L8",
         "A14", "B15", "C15", "E14", "E15", "E16", "F14", "F15", "F13", "F12",
         "G16", "G15", "G13", "G12", "J17", "K16", "AA2", "AA1",  "W2",  "Y3", 
          "N2",  "N1",  "U2",  "U1",  "L2",  "L1", "U21", "V21", "W22", "W21", 
         "Y22", "Y21", "AA22", "AA20", "AB20", "AA19", "AA18", "AB18", "AA17", 
         "U22", "Y19", "AB17", "AA10", "Y14", "V14", "AB22", "AB21", "Y16", "W16", 
         "Y17", "V16", "U17", "V18", "V19", "U20", "Y20", "V20", "U16", "U15", 
         "Y15", "P9", "N9", "M8", "T14", "P14", "C1", "C2", "W19"]

# ====================================================================
# Inicializacao
# ====================================================================
if len(sys.argv) != 2:
    escreve_terminal("O numero de agumentos eh invalido!")
    escreve_terminal("O script devera ser executado como:")
    escreve_terminal("       python compila.py nome_do_projeto")
    escreve_log(arquivo + "," + "")
    sys.exit(2)
    
projeto = sys.argv[1]   # Nome do projeto

# Leitura do arquivo txt com a designacao de pinos do projeto
try:
    f = open(projeto + ".txt", "r")
except IOError:
    escreve_terminal("O arquivo " + projeto + ".txt nao existe")
    escreve_log(arquivo + "," + "Arquivo de designacao de pinos inexistente")
    sys.exit(2)

linhas = f.readlines()
f.close()

# ====================================================================
# Extracao do QAR e captura do nome do projeto
# ====================================================================    
# Limpa diretorio com o nome da projeto e o seu conteudo caso ele ja exista
try:
    shutil.rmtree(projeto)
except OSError as e:
    pass
    
os.mkdir(projeto)                               # Cria diretorio com o nome do projeto

qar = projeto + ".qar"                          # Monta o nome do arquivo .qar
path_file = projeto + "/" + qar

try:
    shutil.copy(qar, path_file)                 # Copia o arquivo qar e move a copia para diretorio criado
except OSError as e:
    escreve_terminal("O arquivo " + qar + " nao existe")
    escreve_log(arquivo + "," + "QAR iexistente")
    sys.exit(2)
    
os.chdir(projeto)                               # Muda para o diretorio criado

# Descompacta o arquivo qar
escreve_terminal("Extraindo qar")
comando = "quartus_sh --restore " + qar
os.system(comando)
escreve_terminal("Qar extraido com sucesso")

# Descoberta do verdadeiro nome do projeto (pode ser diferente do nome do qar)
for arquivo in os.listdir():
    if arquivo.endswith(".qsf"):
        projeto = arquivo.split(".")[0]
escreve_terminal("O nome do projeto eh " + projeto)

# ====================================================================
# Montagem do arquivo de setup do projeto (.tcl)
# ====================================================================
escreve_terminal("Criando arquivo tcl")

# Criacao do arquivo de setup do projeto
f = open("setup_project.tcl", "w+")

f.write("package require ::quartus::flow \n")
f.write("package require ::quartus::project \n\n")

frase = "project_open " + projeto + "\n\n"
f.write(frase)

f.write('set_global_assignment -name FAMILY "Cyclone V" \n')
f.write("set_global_assignment -name DEVICE 5CEBA4F23C7 \n\n")

# Atribuicao da pinagem feita pelos alunos no arquivo txt
for linha in linhas:
    linha = linha.replace("\t", " ")    # Remocao de eventuais TABS dados pelos alunos
    dado = linha.split(" ")   # Separacao dos dois campos da linha do arquivo (sinal | pinagem)
    dado = [x for x in dado if x != ""] # Remocao de eventuais espacos adicionais escritos pelo aluno
    
    if len(dado) == 2:                # dado[0] = sinal | dado[1] = pino
        dado[1] = dado[1].strip()     # Remove \n do fim da string do pino
        dado[1] = dado[1].upper()     # Muda todos os caracteres para maiusculo

        if dado[1].startswith("PIN_"):  # Se o aluno colocou "PIN_" antes da pinagem (ex: PIN_M9)
            dado[1] = dado[1][4:]       # Fica apenas M9

        if dado[1] in pinos:    # Verifica se eh uma pinagem valida
            frase = "set_location_assignment PIN_" + dado[1] + " -to " + dado[0] + "\n"
            f.write(frase)
        else:
            f.close()
            escreve_terminal("Pinagem PIN_" + dado[1] + " nao eh valida", db)
            escreve_log(arquivo + "," + "Pinagem invalida")
            sys.exit(2)


f.write("\n")
f.write("execute_flow -compile")

f.close()

escreve_terminal("Criacao do arquivo tcl finalizada")

# ====================================================================
# Execucao do arquivo tcl
# ====================================================================

# Limpa eventual pinagem feita pelos alunos no arquivo qsf
# O arquivo qsf eh aberto e as linhas correspondentes a pinagens feitas sao apagadas
try:
    f1 = open(projeto + ".qsf", "r")
except OSError as e:
    escreve_terminal("Arquivo .qsf nao encontrado dentro do qar")
    escreve_log(arquivo + "," + "QSF nao encontrado no QAR")
    sys.exit(2)

linhas = f1.readlines()
f1.close()

f1 = open(projeto + ".qsf", "w")
for linha in linhas:
    dado = linha.split(" ")
    if dado[0] != "set_location_assignment":
        f1.write(linha)
f1.close()

# Executa o arquivo tcl para abrir o projeto, designar os pinos e compilar o projeto
escreve_terminal("Iniciando execucao do arquivo tcl (OBS: Pode demorar um pouco)")  
comando = "quartus_sh -t setup_project.tcl > " + projeto

if os.system(comando) != 3:
    escreve_terminal("O projeto foi compilado com sucesso") 
    escreve_log(arquivo + "," + "Compilacao feita com sucesso")
else:
    escreve_terminal("Erro durante a compilacao do projeto. Verifique se o projeto esta correto ou se não houve problema na pinagem")
    escreve_log(arquivo + "," + "Erro de compilacao")
    sys.exit(2)

# Limpa arquivos intermediarios
os.remove("setup_project.tcl")
os.remove(qar)