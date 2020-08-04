import pygame
import random
import math
import client
import threading
import time
pygame.init()


# rv =threading.Thread(target=client.recive,args=())
# rv.start()
GameEnd = False
Result = True
GameTurn = False
Connection = False

RUNNING = True

screen = pygame.display.set_mode((700, 450))

background = pygame.image.load("images/background.jpg")
v_line = pygame.image.load("images/v_line.png")
h_line = pygame.image.load("images/h_line.png")
lr = pygame.image.load("images/lr.png")
rl = pygame.image.load("images/rl.png")
WIN = pygame.image.load("images/WIN.png")
LOST = pygame.image.load("images/LOST.png")


font = pygame.font.Font("freesansbold.ttf", 62)


def num_genrator():
    arr = [int(i)+1 for i in range(25)]
    mtx = []
    tmp = []
    for i in range(25):
        n = random.randint(0, (24-i))
        t_num = arr.pop(n)
        Number = font.render(str(t_num), True, ((0, 0, 0)))
        tmp.append([Number, t_num, False])
        if (i+1) % 5 == 0:
            mtx.append(tmp.copy())
            tmp = []
    return mtx


matrix = num_genrator()


def board_init():
    global matrix
    matrix = num_genrator()


def buff_time():
    global RUNNING
    while RUNNING:
        time.sleep(0.1)
        client.send("")
        if RUNNING == False:
            print("BREAK!1")
            exit()


buff_thread = threading.Thread(target=buff_time, args=())
buff_thread.start()


font2 = pygame.font.Font("freesansbold.ttf", 72)
cross = font2.render("X", True, ((0, 0, 0)))
connecting = font.render("connecting...", True, ((0, 0, 0)))

varr = [False]*5
harr = [False]*5
dig = [False]*2


def checkGrid():
    global matrix, dig
    dig[0] = True
    dig[1] = True
    for i in range(5):
        chack_v = True
        chack_h = True
        for j in range(5):
            if not matrix[i][j][2]:
                chack_h = False
            if not matrix[j][i][2]:
                chack_v = False
            if i == j and (not matrix[i][j][2]):
                dig[0] = False
            if i+j == 4 and (not matrix[i][j][2]):
                dig[1] = False
        harr[i] = chack_h
        varr[i] = chack_v


bingo_state = [False]*5


def check_bingo():
    cnt = 0

    for val in harr+varr+dig:
        if val:
            cnt += 1
    return cnt if cnt < 5 else 5


# MOUSE POINTER
pos = (-100, -100)


def reset_bord():
    global matrix, harr, varr, dig, bingo_state, pos
    pos = (-100, -100)
    matrix = num_genrator()
    for i in range(5):

        harr[i] = False
        varr[i] = False
        bingo_state[i] = False
    dig[0] = False
    dig[1] = False


run = True


def connection_init():
    global GameTurn, connecting

    msg = client.recive()
    print(f"start msg = {msg}")
    GameTurn = msg.strip() == "True"
    connecting = False
    if not GameTurn:
        get_num()


connection_thread = threading.Thread(target=connection_init, args=())
connection_thread.start()


# RECV_NUM=-1
def get_num():
    global matrix, GameTurn, RUNNING
    while RUNNING:
        if RUNNING == False:
            print("BREAK!2")
            exit()
        RECV_NUM = client.recive()
        print(f"RECV :{RECV_NUM}")
        if RECV_NUM.strip() == "BUFF":
            continue
        if RECV_NUM == "LOST":
            Result = False
            GameEnd = True

        try:
            RECV_NUM = int(RECV_NUM.strip())
        except:
            Result = False
        for i in range(5):
            for j in range(5):
                if matrix[i][j][1] == RECV_NUM:
                    matrix[i][j][2] = True
        if RECV_NUM:
            GameTurn = True


while run:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # time.sleep(0.1)
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUIT")
            run = False
            RUNNING = False
            # client.stop()
            break
        # if event.type == pygame.KEYDOWN:
        #     # board_init()
        #     pass
        if event.type == pygame.MOUSEBUTTONUP and GameTurn:
            pos = pygame.mouse.get_pos()

    checkGrid()
    for wdth, ln in enumerate(matrix):
        for index, val in enumerate(ln):

            if 40 > math.sqrt((45+(index*89) - pos[0])**2 + (44+(wdth*90) - pos[1])**2):
                if matrix[wdth][index][2] == False and GameTurn:
                    matrix[wdth][index][2] = True
                    print("SEND", matrix[wdth][index][1])
                    client.send(str(matrix[wdth][index][1]))
                    GameTurn = False
                    rv = threading.Thread(target=get_num, args=())
                    rv.start()
                    # rv =threading.Thread(target=client.recive,args=())
                    # rv.start()
                    print(f"RES:{Result}")
            if val[1] < 10:
                k = 13
            else:
                k = 0

            screen.blit(val[0], (15+(index*89)+k, 14+(wdth*90)))
            if val[2]:
                screen.blit(cross, (26+(index*89), 14+(wdth*90)))

    print(threading.active_count())
    for index in range(5):
        if varr[index]:
            screen.blit(v_line, (40+(index*90), 0))
        if harr[index]:
            screen.blit(h_line, (0, 35+(index*90)))
    if dig[1]:
        screen.blit(lr, (-440, -120))
    if dig[0]:
        screen.blit(rl, (-120, -450))

    for index in range(check_bingo()):
        screen.blit(cross,  (585,  66+(index*66)))
        # print(index)
    # screen.blit(LOST,(100,100))
    if GameEnd:
        if Result:
            screen.blit(WIN, (100, 100))
        else:
            screen.blit(LOST, (100, 100))

    if check_bingo() == 5:
        GameEnd = True
        # client.send("BINGO")

    pygame.display.update()

# rv.join()
