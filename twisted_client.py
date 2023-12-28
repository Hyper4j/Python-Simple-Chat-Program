import socket
import sys
import threading

def onReadChat(name, client):
    while True:
        data = client.recv(4096).decode("utf-8")
        print(data)
        if data == "서버와 연결에 성공했습니다.":
            client.send(("닉네임: "+name).encode("utf-8"))

client = socket.socket()

name = input("접속할 사용자이름을 정해주세요: ")
server_ip, server_port = input("서버아이피:서버포트 를 적어 연결시도 해주세요! ").split(":")

client.connect((server_ip, int(server_port)))

t = threading.Thread(target=onReadChat, args=(name, client))
t.start()

while True:
    msg = sys.stdin.readline()
    msg = msg.replace("\n", "")
    client.send(msg.encode("utf-8"))
