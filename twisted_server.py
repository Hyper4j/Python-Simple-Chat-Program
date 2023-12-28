from twisted.internet import protocol, reactor

transports = set()
names = {}

class Chat(protocol.Protocol):
    # 사용자가 서버에 접속했을때
    def connectionMade(self):
        self.transport.write('서버와 연결에 성공했습니다.'.encode())
        transports.add(self.transport)
    
    # 사용자가 서버에 나갔을때
    def connectionLost(self, reason):
        print(names[self.transport], "가 연결을 종료하였습니다 :", reason)
        for t in transports:
            if t != self.transport:
                t.write((names[self.transport]+"가 서버에서 나갔습니다.").encode("utf-8"))
        names[self.transport] = None
        transports.remove(self.transport)
    
    # 데이터 전송을 받았을때
    def dataReceived(self, data: bytes):
        data = str(data.decode("utf-8"))
        if data.__contains__("닉네임: ") == True:
            names[self.transport] = data.split("닉네임: ")[1]
            print(names[self.transport], "가 연결에 성공했습니다.")
            for t in transports:
                if t != self.transport:
                    t.write((names[self.transport]+"가 서버에 접속했습니다.").encode("utf-8"))
        else:
            for t in transports:
                t.write(str(names[self.transport] + ":" + data).encode("utf-8"))

class ChatFactory(protocol.Factory):
    # protocol = echo
    def buildProtocol(self, addr):
        return Chat()
    

print("서버를 실행했습니다.")
reactor.listenTCP(8080, ChatFactory())
reactor.run()