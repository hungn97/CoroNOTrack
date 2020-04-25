#!/bin/usr/env python
import socket
import ssl
import pprint

#server
if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 1234 #note that the 2 servers use different ports, still the same host address though

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs = r"C:\Users\longn\Desktop\ECE547\opensslCerts\client.pem", certfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\authServer.pem", keyfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\authServer.key", cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1_2)

    print(repr(secure_sock.getpeername()))
    print(secure_sock.cipher())
    print(pprint.pformat(secure_sock.getpeercert()))
    cert = secure_sock.getpeercert()
    print(cert)

    response = 'acknowledge from serverA'

    try:
        data = secure_sock.read(1024)
        MSG = data.decode()
        echoMSG = MSG.encode()
        replyMSG = response.encode()
        secure_sock.write(replyMSG) #to echo, send back echoMSG, to send nonecho reply, send replyMSG
    finally:
        secure_sock.close()
        server_socket.close()