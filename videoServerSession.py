import socket
import struct
import pickle
import cv2

# 통신 정보 설정
IP = ''
PORT = 5000
SIZE = 1024
ADDR = (IP, PORT)

# 서버 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)  # 주소 바인딩
    server_socket.listen()  # 클라이언트의 요청을 받을 준비

    # 무한루프 진입
    while True:
        client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
        data = b''
        payload_size = struct.calcsize("L")
        while True:
            while len(data) < payload_size:
                data += client_socket.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)

            cv2.imshow('frame', frame)
            cv2.waitKey(1)

            if data == "":
                break;
        msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
        print("[{}] message : {}".format(client_addr,msg))  # 클라이언트가 보낸 메시지 출력

        client_socket.sendall("welcome!".encode())  # 클라이언트에게 응답

        client_socket.close()  # 클라이언트 소켓 종료