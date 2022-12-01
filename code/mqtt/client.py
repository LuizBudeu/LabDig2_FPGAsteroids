import paho.mqtt.client as mqtt


user = 'grupo1-bancadaA6'
passwd = 'digi#@1A6'

Broker = "labdigi.wiseful.com.br"            # Endereco do broker
Port = 80                           # Porta utilizada (firewall da USP exige 80)
KeepAlive = 60                      # Intervalo de timeout (60s)
# TopicoL = user+"/req"               # Topico que sera lido
# TopicoE = user+"/resp"              # Topico que sera escrito
topics = [(user+'/input', 0), (user+'/pos', 0), (user+'/S0', 0)]

db = 1                              # Flag de depuracao (verbose)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topics)
    # client.subscribe(user+'/pos')

# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     global fim_de_jogo
#     print(f"{msg.topic} {msg.payload.decode('utf-8')}")
#     # send_to_game(msg.payload.decode('utf-8'))
#     with open('code/mqtt/msg.txt', 'w') as f:
#         f.write(msg.payload.decode('utf-8'))
#     fim_de_jogo = [msg.payload.decode('utf-8')]
#     # message = msg.payload.decode('utf-8')
#     # return message

# def send_to_game(msg=None):
#     if msg is not None:
#         return msg


client = mqtt.Client()                      # Criacao do cliente MQTT
client.on_connect = on_connect              # Vinculo do Callback de conexao
# client.on_message = on_message              # Vinculo do Callback de mensagem recebida
client.username_pw_set(user, passwd)        # Apenas para coneccao com login/senha
client.connect(Broker, Port, KeepAlive)     # Conexao do cliente ao broker
# client.loop_forever()
# client.loop_start()





# # ====================================================================
# # Implementacao do client MQTT utilizando a bilbioteca MQTT Paho
# # ====================================================================
# import paho.mqtt.client as mqtt
# import time
# from usuario import *

# Broker = "3.141.193.238"            # Endereco do broker
# Port = 80                           # Porta utilizada (firewall da USP exige 80)
# KeepAlive = 60                      # Intervalo de timeout (60s)
# TopicoL = user+"/req"               # Topico que sera lido
# TopicoE = user+"/resp"              # Topico que sera escrito

# db = 1                              # Flag de depuracao (verbose)

# # Quando conectar na rede (Callback de conexao)
# def on_connect(client, userdata, flags, rc):
#     print("Conectado com codigo " + str(rc))
#     client.subscribe(TopicoL, qos=0)

# # Quando receber uma mensagem (Callback de mensagem)
# def on_message(client, userdata, msg):
#     client.newmsg = True    
#     client.msg = msg.payload.decode("utf-8")

# # Funcao que espera nova mensagem do terminal
# # Por enquanto o parametro "topico" nao possui utilidade
# def le_terminal(topico=TopicoL, verbose=db):
#     client.newmsg = False

#     # Fica em loop infinito ate receber uma nova mensagem
#     while not client.newmsg:
#         client.loop_start()
#         time.sleep(2)
#         client.loop_stop()

#     if verbose == 1:
#         print("> " + client.msg)

#     return client.msg

# # Funcao que escreve no terminal
# # Por padrao vai escrever no topico apontado por "TopicoE"
# def escreve_terminal(frase, topico=TopicoE, verbose=db):
#     client.publish(topico, payload=frase, qos=0, retain=False)
#     if verbose == 1:
#         print(frase)

# client = mqtt.Client()                      # Criacao do cliente MQTT
# client.on_connect = on_connect              # Vinculo do Callback de conexao
# client.on_message = on_message              # Vinculo do Callback de mensagem recebida
# client.username_pw_set(user, passwd)        # Apenas para coneccao com login/senha
# client.connect(Broker, Port, KeepAlive)     # Conexao do cliente ao broker