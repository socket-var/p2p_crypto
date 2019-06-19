import trio
import os
from itertools import count
from dotenv import load_dotenv
import pickle


load_dotenv()

from p2p_module.config import self_server_host, self_server_port, self_client_host, self_client_port, owner_key_file_name, receiver_key_file_name, encryption_file_name, decryption_file_name, buffer_size

CONNECTION_COUNTER = count()

def receiver(server_stream, data):
    data = pickle.loads(data)
    dest_address, command = data["to_address"], data["command"]

    print(dest_address, "{}:{}".format(self_client_host, self_client_port), command)
    
    filename = ""

    if dest_address == "{}:{}".format(self_client_host, self_client_port):

        if (command == "start-kx" or command == "reply-kx"):
            filename = receiver_key_file_name
        elif command == "caesar-encrypt" and dest_address == "{}:{}".format(self_client_host, self_client_port):
            filename = encryption_file_name
        elif command == "caesar-decrypt" and dest_address == "{}:{}".format(self_client_host, self_client_port):
            filename = decryption_file_name
        
        with open(filename, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)
    
    else:
        print("Whoops, you choose the wrong recepient")


async def p2p_server(server_stream):
    # Assign each connection a unique number to make our debug prints easier
    # to understand when there are multiple simultaneous connections.
    ident = next(CONNECTION_COUNTER)
    print("Server {}: started".format(ident))
    try:
        while True:
            data = await server_stream.receive_some(buffer_size)
            print("Server {}: received data {!r}".format(ident, data))
            
            receiver(server_stream, data)
            
            if not data:
                print("Server {}: connection closed".format(ident))
                return

            # send_all(data)
    # FIXME: add discussion of MultiErrors to the tutorial, and use
    # MultiError.catch here. (Not important in this case, but important if the
    # server code uses nurseries internally.)
    except Exception as exc:
        # Unhandled exceptions will propagate into our parent and take
        # down the whole program. If the exception is KeyboardInterrupt,
        # that's what we want, but otherwise maybe not...
        print("Server {}: crashed: {!r}".format(ident, exc))


async def main():
    await trio.serve_tcp(p2p_server, self_server_port)


# We could also just write 'trio.run(serve_tcp, echo_server, PORT)', but real
# programs almost always end up doing other stuff too and then we'd have to go
# back and factor it out into a separate function anyway. So it's simplest to
# just make it a standalone function from the beginning.
trio.run(main)