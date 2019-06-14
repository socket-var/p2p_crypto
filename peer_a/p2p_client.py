import socket

destination_server_settings = ("169.229.118.206", 1500)

client_settings = ('169.229.118.124', 1501)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(client_settings)
    s.connect(destination_server_settings)
    s.sendall(b'Hello world from 169.229.118.124')

    while True:
        data = s.recv(1024)
        print('Received', repr(data), " from ", destination_server_settings[0])    


