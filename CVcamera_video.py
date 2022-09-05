import cv2
import numpy as np
import pickle
import struct
import socket

LocalIP = ''
Port = 9999
Size = 1024
Server_Address = (LocalIP, Port)

def recvall(socket, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = socket.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(Server_Address)
    print("Start Listen!")
    server_socket.listen()  # 클라이언트 소켓 수신 준비

    
    client_socket, client_address = server_socket.accept()
    
    while True:
        length = recvall(client_socket, 16)
        stringData = recvall(client_socket, int(length))
        data = np.fromstring(stringData, dtype='uint8')

        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

        resize_img = cv2.resize(frame, (640, 480))
        
        cv2.imshow('ImageWindow', resize_img)
        cv2.waitKey(1)