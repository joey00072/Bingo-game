import socket
import threading
import time

PORT = 5065
HEADER = 64
FORMAT = "utf-8"
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

queue = []


def dequeue():
    try:
        return queue.pop(0)
    except:
        return None


def send(msg):
    message = msg.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' '* (HEADER - len(send_length))
    # client.send(send_length)
    client.send(message)


def recive():
    massage = client.recv(HEADER)

    if len(massage) != 0:
        # print(massage.decode(FORMAT))
        return massage.decode(FORMAT)

# rv = threading.Thread(target=recive,args=())
# rv.start()


def stop():
    conn.close()
    exit()

# send("WORKING")


if __name__ == "__main__":
    while True:
        send(input())
