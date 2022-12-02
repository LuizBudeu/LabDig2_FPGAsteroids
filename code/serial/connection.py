import serial
import time 


ser = serial.Serial()  # open serial port
ser.baudrate = 115200
ser.port = 'COM6'
ser.bytesize = 7
ser.parity = 'E'
ser.stopbits = 2
ser.timeout = 0.2
print(ser.name)         # check which port was really used


# ser.write(b'hello')     # write a string

# while True:
#     try:
#         ser.open()

#         msg = ser.read(8)
#         print(int(msg.decode('utf-8')))
#         # print(ser.read(8))
#         time.sleep(1)

#         ser.close()             # close port
#     except KeyboardInterrupt:
#         break


    
# env = bin(env)
# ser.write(env.encode())
# ser.write('420'.encode())



ser.close()             # close port