import trio
import os
from itertools import count
from dotenv import load_dotenv
import pickle


load_dotenv()

server_host = os.getenv(
    "SELF_SERVER_ADDRESS")

server_port = int(os.getenv(
    "SELF_SERVER_PORT"))

BUFSIZE = 16384

CONNECTION_COUNTER = count()


async def p2p_server(server_stream):
    # Assign each connection a unique number to make our debug prints easier
    # to understand when there are multiple simultaneous connections.
    ident = next(CONNECTION_COUNTER)
    print("Server {}: started".format(ident))
    try:
        while True:
            data = await server_stream.receive_some(BUFSIZE)
            print("Server {}: received data {!r}".format(ident, data))
            if not data:
                print("Server {}: connection closed".format(ident))
                return
            print("Server {}: sending data {!r}".format(ident, data))
            await trio.sleep(3)

            await server_stream.send_all(data)
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
    await trio.serve_tcp(p2p_server, server_port)


# We could also just write 'trio.run(serve_tcp, echo_server, PORT)', but real
# programs almost always end up doing other stuff too and then we'd have to go
# back and factor it out into a separate function anyway. So it's simplest to
# just make it a standalone function from the beginning.
trio.run(main)
