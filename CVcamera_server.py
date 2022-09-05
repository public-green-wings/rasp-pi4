import socket
from telnetlib import SE
import cv2
import pickle
import struct

LocalIP = ''
Port = 9999
Size = 1024
Server_Address = (LocalIP, Port)

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 수신 준비
server_socket.bind(Server_Address)
print("Start Listen!")
server_socket.listen() 


# 연결
client_socket, client_address = server_socket.accept()

# 4 bytes
L_size = struct.calcsize("L")
print("L_size: ", L_size)

buffer = b""

while True:
    try:
        while len(buffer) < L_size:
            buffer += client_socket.recv(4096)

        header = buffer[:L_size]
        data = buffer[L_size:]

        frame_size = struct.unpack(">L", header)[0]
        print(frame_size)

        while len(data) < frame_size:
            data += client_socket.recv(4096)

        frame_data = data[:frame_size]
        buffer = data[frame_size:]

        encoded_frame = pickle.loads(frame_data)

        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

        cv2.imshow('Frame', frame)

    except Exception as error:
        print("{} : Error occured" .format(error))
        break;
    
client_socket.close()
server_socket.close()
