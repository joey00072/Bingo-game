import socket
import threading
import time
import random


PORT = 5065
HEADER = 64
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
EXIT = "EXIT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users_list = []

room = True
allRooms = []


class Game(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        print("Object Created")
        self.turn = False
        self.player1 = conn
        self.player2 = None
        self.state = "RUN"
        # self.buff = None

    def set_player2(self, conn):
        self.player2 = conn

    def isPlayer2_valid(self):
        return self.player2 != None

    def endGame(self, player):
        if player == "P1":
            self.player1.send(bytes("WIN", FORMAT))
            self.player2.send(bytes("LOST", FORMAT))
        else:
            self.player2.send(bytes("WIN", FORMAT))
            self.player1.send(bytes("LOST", FORMAT))

    def run(self):
        print(f"[ROOM STARTED]")
        self.turn = random.choice([True, False])
        self.player1.send(bytes(str(self.turn), FORMAT))
        self.player2.send(bytes(str((not self.turn)), FORMAT))

        # state = "RUN"
        msg = ""
        while self.state == "RUN":
            time.sleep(0.01)
            if self.turn:
                # msg_len = self.player1.recv(HEADER)
                msg = self.player1.recv(HEADER)
                if msg:
                    print(msg.decode())
                    if msg.decode().strip() == "BINGO":
                        self.endGame("P1")
                        self.state = "HULT"
                    self.player2.send(msg)
                    self.turn = False
            else:
                # msg_len = self.player2.recv(HEADER)
                msg = self.player2.recv(HEADER)
                if msg:
                    print(msg.decode())
                    if msg.decode().strip() == "BINGO":
                        self.endGame("P2")
                        self.state = "HULT"
                    self.player1.send(msg)
                    self.turn = True


def handle_client(conn, addr):
    global users_list, room

    if room:
        g = Game(conn)
        room = False
        allRooms.append(g)
        print("[ROOM CREATED]")
        print("HEEjdissdsdhsdhdh")
    else:
        if allRooms[-1].isPlayer2_valid():
            print("HEREEEEEEEEEEEEEEEEEEEEE")
            allRooms[-1].set_player2(conn)
            t1 = threading.Thread(target=allRooms[-1].run(), args=())
            t1.start()
            print("STARING THREAD")
        room = True
        print(f"[ROOMS] :{len(allRooms)}")

    print(f"[NEW CONNECTION] {addr} connected...")

    connected = True

    while connected:
        time.sleep(0.01)

        try:
            message_len = conn.recv(HEADER).decode(FORMAT)
        except BaseException as e:
            print(f'Exception occured: {e}')
            continue
        if message_len:
            print(message_len)
            message_len = int(message_len.strip())
            msg = conn.recv(message_len).decode(FORMAT)

            for users in users_list:
                try:
                    users.send(str(msg).encode(FORMAT))
                except BaseException as e:
                    print(f"User Disconned ")
            print(f"{addr} : {msg}")
            if msg.strip() == EXIT:
                connected = False
    conn.close()
    print(f"{addr} is disconnected")


def start():
    global users_list, room
    server.listen()
    print(f"[LISTING] server is listing on  {SERVER}")
    count = -1
    while True:
        time.sleep(0.01)
        conn, addr = server.accept()
        if room:
            g = Game(conn)
            room = False
            allRooms.append(g)
            print("[ROOM CREATED]")
            print('log1')
            count += 1
        else:
            print("log2")
            if not allRooms[count].isPlayer2_valid():
                print('log3')
                allRooms[count].set_player2(conn)
                # t1= threading.Thread(target=allRooms[count].run() ,args=())
                # t1.start()
                allRooms[count].start()
            room = True
            print(f"[ROOMS] :{len(allRooms)}")

        # thread = threading.Thread(target=handle_client,args=(conn,addr))
        # thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")


if __name__ == "__main__":
    print("[STARING] server is staring ... ")
    start()
