import socket
import ssl

# client
if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 1234
    PORTB = 1235

    authSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    authSock.setblocking(1);
    authSock.connect((HOST, PORT))

    recordSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recordSock.setblocking(1);
    recordSock.connect((HOST, PORTB))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(r'C:\Users\longn\Desktop\ECE547\opensslCerts\authServer.pem')
    context.load_verify_locations(r'C:\Users\longn\Desktop\ECE547\opensslCerts\recordServer.pem')
    context.load_cert_chain(certfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\client.pem", keyfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\client.key")

    if ssl.HAS_SNI:
        secure_sock_AUTH = context.wrap_socket(authSock, server_side=False, server_hostname=HOST)
        secure_sock_RECORD = context.wrap_socket(recordSock, server_side=False, server_hostname=HOST)
    else:
        secure_sock_AUTH = context.wrap_socket(authSock, server_side=False)
        secure_sock_RECORD = context.wrap_socket(recordSock, server_side=False)

    cert = secure_sock_AUTH.getpeercert()
    certB = secure_sock_RECORD.getpeercert()
    print(cert)

    greetings = 'hello from client'
    byt = greetings.encode()
    secure_sock_AUTH.write(byt)
    secure_sock_RECORD.write(byt)
    print(secure_sock_AUTH.read(1024))
    print(secure_sock_RECORD.read(1024))
    secure_sock_AUTH.close()
    secure_sock_RECORD.close()
    authSock.close()
    recordSock.close()