# ====================================================================
# Implementacao do client MQTT utilizando a bilbioteca MQTT Paho
# ====================================================================
import paho.mqtt.client as mqtt
import time
from usuario import *
from log import *

Broker = "labdigi.wiseful.com.br"            # Endereco do broker
Port = 80                           # Porta utilizada (firewall da USP exige 80)
KeepAlive = 60                      # Intervalo de timeout (60s)
TopicoL = user+"/req"               # Topico que sera lido
TopicoE = user+"/resp"              # Topico que sera escrito

db = 1                              # Flag de depuracao (verbose)

ultimo_topico = ""

# Quando conectar na rede (Callback de conexao)
def on_connect(client, userdata, flags, rc):
    print("Conectado com codigo " + str(rc))
    client.subscribe(TopicoL, qos=0)
    client.subscribe(user+"/E0", qos=0)
    client.subscribe(user+"/E1", qos=0)
    client.subscribe(user+"/E2", qos=0)
    client.subscribe(user+"/E3", qos=0)
    client.subscribe(user+"/E4", qos=0)
    client.subscribe(user+"/E5", qos=0)
    client.subscribe(user+"/E6", qos=0)
    client.subscribe(user+"/E7", qos=0)
    client.subscribe(user+"/S0", qos=0)
    client.subscribe(user+"/S1", qos=0)
    client.subscribe(user+"/S2", qos=0)
    client.subscribe(user+"/S3", qos=0)
    client.subscribe(user+"/S4", qos=0)
    client.subscribe(user+"/S5", qos=0)
    client.subscribe(user+"/S6", qos=0)
    client.subscribe(user+"/S7", qos=0)
    client.subscribe(user+"/led", qos=0)

# Quando receber uma mensagem (Callback de mensagem)
def on_message(client, userdata, msg):
    client.newmsg = True
    client.msg = msg.payload.decode("utf-8")
    global ultimo_topico
    ultimo_topico = msg.topic

    current_topic = str(msg.topic)
    current_value = str(msg.payload.decode("utf-8")) 
    current_time = str(datetime.now())

    f = open(nomeMQTT, "a")
    f.write(current_time + "," + current_topic + "," + current_value + "\n")
    f.close()

# Funcao que espera nova mensagem do terminal
# Por enquanto o parametro "topico" nao possui utilidade
def le_terminal(topico=TopicoL, verbose=db):
    client.newmsg = False

    # Fica em loop infinito ate receber uma nova mensagem de requisicao apontada por "topico"
    while not client.newmsg or ultimo_topico != topico:
        client.loop_start()
        time.sleep(2)
        client.loop_stop()

    if verbose == 1:
        print("> " + client.msg)

    return client.msg

# Funcao que escreve no terminal
# Por padrao vai escrever no topico apontado por "TopicoE"
def escreve_terminal(frase, topico=TopicoE, verbose=db):
    client.publish(topico, payload=frase, qos=0, retain=False)
    if verbose == 1:
        print(frase)

client = mqtt.Client()                      # Criacao do cliente MQTT
client.on_connect = on_connect              # Vinculo do Callback de conexao
client.on_message = on_message              # Vinculo do Callback de mensagem recebida
client.username_pw_set(user, passwd)        # Apenas para coneccao com login/senha
client.connect(Broker, Port, KeepAlive)     # Conexao do cliente ao broker