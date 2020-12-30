import socket
import threading
import random
from time import sleep

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = 'utf-8'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
questions = []
questions.append(('how far away is the sun?', '10  km', '50 km ', '60 km', '147 millions km', 4))
questions.append(('What country won the very first FIFA World Cup in 1930?', 'Uruguay', 'Israel', 'Spain', 'France', 1))
questions.append(('Which email service is owned by Microsoft?', 'Gmail', 'Hotmail', 'Walla mail', 'AOL', 2))
questions.append(('What’s the hardest rock?', 'Diamond', 'Quartz', 'Dwayne johnson', 'Granite', 1))
questions.append(('Whats the heaviest creature in the world?', 'African elephant', 'Hippo', 'Blue whale', 'Yo mamma', 3))
questions.append(('Which planet has the most gravity?', 'Jupiter', 'Mercury', 'Uranus', 'Saturn', 1))
questions.append(('Which of the following was not an impressionist?', 'Manet', 'Pissarro', 'Renoir', 'Picasso', 4))
questions.append(('Which author wrote the ‘Winnie-the-Pooh’ books?', 'JK Rowling', 'Andrew Clements ', 'A.A Milne', 'Ori Karni', 3))
questions.append(('What was the first toy to be advertised on television?', 'Mr Potato Head', 'Soccer Ball ', 'Xbox 360', 'GamCube', 1))
questions.append(('What is the tiny piece at the end of a shoelace called?', 'Rain Guard', 'Aglet ', 'Plastic', 'Thingymjab', 2))
questions.append(('What is the world’s biggest island?', 'Iceland', 'Greenland ', 'Australia', 'Dirichletland', 2))
questions.append(('Which country is known as the Land of White Elephant?', 'Iceland', 'Japan', 'Thailand', 'Canada', 3))
questions.append(('What is the name of the Earth’s largest ocean?', 'Artic', 'Atlantic', 'Kineret', 'Pacific', 4))
questions.append(('What country won the very first FIFA World Cup in 1930??', 'Brazil', 'Uruguay', 'Argentina', 'France', 2))
questions.append(('In what year was the first ever Wimbledon Championship held?', '1877', '1923', '1969', '1854', 1))
questions.append(('When will Binyamin Netanyahu end  his reign?', '1998', '2021', '2026', 'Over 9000', 4))
questions.append(('How many hearts does an octopus have?', '0', '1', '2', '3', 4))
questions.append(('Power outages in the US are mostly caused by what?', 'Scientist', 'Squirrels', 'Uri Locker', 'Pigeons', 2))
questions.append(('What did the Crocodile swallow in Peter Pan?', 'An alarm clock', 'Another crocodile', 'A shoe', 'Tinker Bell', 1))
questions.append(('What are nails made of?', 'Diamond', 'Charcoal', 'Keratin', 'Gelatin', 3))
questions.append(('Who invented the scissors', 'Benjamin Franklin', 'Picasso', 'Leonardo da Vinci', 'George Washington', 3))

def aa(a):
    a.clear()
    a+= [1,2,4]
    return True
a = [1,2,3]
print(a)
aa(a)
print(a)
def askAQuestion(list, questions):
    if len(list) == 0:
        list += list(range(0, 20))
    qusetionNum = random.choice(list)
    list.remove(qusetionNum)
    conn.send((f"1{questions[qusetionNum][0]}\n(1) {questions[qusetionNum][1]}\n(2) {questions[qusetionNum][2]}\n(3) {questions[qusetionNum][3]}\n(4) {questions[qusetionNum][4]}").encode(FORMAT))
    msg = conn.recv(1024).decode(FORMAT)
    return int(msg) == questions[qusetionNum][5]

def askAQuestionLvl2(list, questions, help):
    if len(list) == 0:
        list += list(range(0, 20))
    qusetionNum = random.choice(list)
    list.remove(qusetionNum)
    if help == [1]:
        conn.send(f"1{questions[qusetionNum][0]}\n(1) {questions[qusetionNum][1]}\n(2) {questions[qusetionNum][2]}\n(3) {questions[qusetionNum][3]}\n(4) {questions[qusetionNum][4]}\nRemember you still have your safty net, if you would like to use it press 5\n".encode(FORMAT))
        msg = conn.recv(1024).decode(FORMAT)
        if msg == '5':
            if questions[qusetionNum][5] in [1, 2]:
                conn.send(f"1{questions[qusetionNum][0]}\n(1) {questions[qusetionNum][1]}\n(2) {questions[qusetionNum][2]}\n".encode(FORMAT))
            else:
                conn.send(f"1{questions[qusetionNum][0]}\n(3) {questions[qusetionNum][3]}\n(4) {questions[qusetionNum][4]}\n".encode(FORMAT))
            help[0] = 0
            msg = conn.recv(1024).decode(FORMAT)
    else:
        conn.send((f"1{questions[qusetionNum][0]}\n(1) {questions[qusetionNum][1]}\n(2) {questions[qusetionNum][2]}\n(3) {questions[qusetionNum][3]}\n(4) {questions[qusetionNum][4]}").encode(FORMAT))
        msg = conn.recv(1024).decode(FORMAT)
    return int(msg) == questions[qusetionNum][5]

def handle_client(conn, addr, numConnections,questions):
    print(f"[NEW CONNECTION] {addr} connected.")
    playing = 1
    while playing == 1:
        level = 1
        remaining = list(range(0, 20))
        if numConnections>3:
            conn.send(("0Sorry, there are too many players already: you will be disconnected").encode(FORMAT))
            conn.recv(1)
            break
            level = -1
        else:
            conn.send("0Welcome to the game! \n".encode(FORMAT))
            conn.recv(1)

        money = 0
        numCorrect = 0
        numQuestions = 0
        # Level 1
        while level == 1:
            numQuestions += 1
            if askAQuestion(remaining, questions):
                conn.send(f"0Correct!\n".encode(FORMAT))
                conn.recv(1)
                numCorrect += 1
            else:
                conn.send(f"0Incorrect!\n".encode(FORMAT))
                conn.recv(1)
            if numQuestions == 3:
                if numCorrect == 0:
                    conn.send(f"0You didn't make it to LEVEL 2 , starting level  1 again\n".encode(FORMAT))
                    conn.recv(1)
                    numQuestions = 0
                    numCorrect = 0
                else:
                    money = numCorrect * 5000
                    level = 2
                    conn.send(f"0Congrats! You made it to LEVEL 2 \nYou have {numCorrect} correct answers, and {money}$\n".encode(FORMAT))
                    conn.recv(1)

        conn.send(f"1The chaser is currently at level 0, you are at level 3 \nYou have the following 3 options:\n1. Start at your current location (3) for {money}$\n2. Take a step forward towards the chaser for {money*2}$\n3. Take a step back for {money/2}$\n".encode(FORMAT))
        msg = conn.recv(1024).decode(FORMAT)
        chaser = 0
        player = 3
        help = [1]
        if msg == '2':
            player -= 1
            money *= 2
        if msg == '3':
            player += 1
            money /= 2

        # level 2
        while (not player == 7) and (not player == chaser):
            if askAQuestionLvl2(remaining, questions, help):
                conn.send(f"0Correct!\n".encode(FORMAT))
                conn.recv(1)
                player += 1
            else:
                conn.send(f"0Incorrect!\n".encode(FORMAT))
                conn.recv(1)
            a = random.randint(1, 4)
            if not a == 1:
                chaser += 1

            conn.send(f"0You have {money}$\nYou are in place {player} , the chaser is in place {chaser}\nYou {'dont' if (help[0] == 0) else ''} have a help\n".encode(FORMAT))
            conn.recv(1)

        if player == 7:
            conn.send(f"0Congratulations! You have won {money}$\n".encode(FORMAT))
            conn.recv(1)
        if player == chaser:
            conn.send(f"0Sorry! You lost\n".encode(FORMAT))
            conn.recv(1)
        conn.send(f"1Would you like to play again?\n".encode(FORMAT))
        playing = False
        msg = conn.recv(1024).decode(FORMAT)
        if msg == "Yes" or msg == "yes":
            playing = True

    conn.close()




s.listen(2)

while True:
    conn, addr = s.accept()
    # msg = input()
    # conn.send(msg.encode())
    # msg = conn.recv(1024)
    # print('Received: ' + msg.decode())
    thread = threading.Thread(target=handle_client, args=(conn, addr,threading.activeCount()-1,questions))
    thread.start()



conn.close()
s.close()



