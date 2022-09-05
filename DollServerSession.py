import socket
from threading import Thread
import time
import struct

LocalIP = ''
Port = 9999
Size = 1024
Server_Address = (LocalIP, Port)
global AddressBook
AddressBook = []
global Users
Users = []
# global dialogs_buffer
dialogs_buffer = []
# struct_Lsize = struct.calcsize("L")
struct_Lsize = 4

def answerThread(size, buffer):
    while True:
        if len(buffer) > 0:
            c_socket, c_address, message = buffer[0]
            print("<{}> loaded one dialog : {}" .format(c_address, message))
            c_socket.sendall("Received Completely!".encode())
            del buffer[0]
        time.sleep(5)

def make_new_chatThread(c_socket, c_address, size, is_newbie, buffer):
    # global Users
    # Users.append(c_name)

    while True:
        received = c_socket.recv(size)
        nameLength_byte = received[:struct_Lsize]
        received_data = received[8:]
        nameLength = struct.unpack("L", nameLength_byte)[0]
        name = received_data[:nameLength].decode()
        data = received_data[nameLength:].decode()
        if data == 'end':
            break;
        buffer.append((c_socket, c_address, data))
        print("received by <{}> : {}" .format(name, data))

    c_socket.close()


# server 소켓 생성. with로 작성해서 server 소켓 close를 안써도 됨
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(Server_Address)
    print("Start Listen!")
    server_socket.listen()  # 클라이언트 소켓 수신 준비
    receiving_thread = Thread(target=answerThread, args=(Size, dialogs_buffer))
    receiving_thread.daemon = True
    receiving_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        print(1)
        if client_address not in AddressBook:
            AddressBook.append(client_address)
            newbie = True
        user_thr = Thread(target=make_new_chatThread, args=(client_socket, client_address, Size, newbie, dialogs_buffer))
        user_thr.daemon = True
        user_thr.start()
        newbie = False
        