import socket as sock

#check proxy with a http get request to google.com
def CheckConnection(addr:str,port:int) -> bool:
    try:
        proxysock = sock.socket(sock.AF_INET,sock.SOCK_STREAM,0)
        proxysock.settimeout(5)
        proxysock.connect((addr,port))
        proxysock.send(bytes([0x05,0x01,0x00]))
        rcvd1 = proxysock.recv(1024)
        if(rcvd1[0] == 0x05 and rcvd1[1] == 0xff):
            proxysock.close()
            return False
        proxysock.send(b'\x05\x01\x00\x03'+bytes([len("google.com")])+"google.com".encode()+int(80).to_bytes(2,'big'))
        rcvd2 = proxysock.recv(1024)
        if(rcvd2[0] == 0x05 and rcvd2[1] != 0x00):
            proxysock.close()
            return False
        proxysock.send(b"GET / HTTP/1.1\r\n\r\n")
        if(str(proxysock.recv(1024)) != ""):
            proxysock.close()
            return True
    except Exception as e:
        print(e)
        return False