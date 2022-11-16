from client import client, user
import time


counter = 0
while True:
    client.loop_start()
    client.publish(user+'/hello', counter)
    print(f'Sent message: {counter}' )
    counter += 1
    time.sleep(1)
    # client.loop_stop()