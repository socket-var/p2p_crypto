import socket


server_settings = ("169.229.118.206", 1500)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(server_settings)
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connection succeeded with client ', addr)
        while True:
            data = conn.recv(1024)
            conn.sendall(data)
