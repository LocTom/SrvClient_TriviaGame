import socket

HOST = '192.168.0.105'  # The server's hostname or IP address
PORT = 65432  # The port used by the server





play = input("Would you like to be chased!?!?! /n YES OR NO")
if play == "YES" or play == "yes":
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    while True:
        msg = conn.recv(1024).decode('utf-8')

        print(msg[1:])

        if msg[0] == '1':
            msg = input()
            conn.send(msg.encode())

        elif msg == 'DISSCONNECT':
            break

        else:
            msg = 'a'
            conn.send(msg.encode())




    conn.close()