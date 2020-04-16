import socket
import ssl

# client
if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 1234

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1);
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(r'C:\Users\longn\Desktop\ECE547\opensslCerts\server.pem')
    context.load_cert_chain(certfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\client.pem", keyfile=r"C:\Users\longn\Desktop\ECE547\opensslCerts\client.key")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    cert = secure_sock.getpeercert()
    print(cert)

    greetings = 'hello from client'
    byt = greetings.encode()
    secure_sock.write(byt)
    print(secure_sock.read(1024))
    secure_sock.close()
    sock.close()