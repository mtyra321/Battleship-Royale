#############################################################################
# Program:
#    Lab 5 Client, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Matt Tyra
# Summary:
#   This code is for the rock paper scissors game using sockets. 
#   This is the client portion of the assignment.
#   I altered my Lab 4 in order to comply with the protocol set by the class
##############################################################################

from socket import *
import sys
from ship import Ship
from board import Board
from os import read
import pickle

CRLF = "\r\n"
SPELL_WORD = {'h':'Hit', 'm':'Miss'}
grid_response =     ['A1','A2','A3','A4','A5','A6','A7','A8',
                    'B1','B2','B3','B4','B5','B6','B7','B8',
                    'C1','C2','C3','C4','C5','C6','C7','C8',
                    'D1','D2','D3','D4','D5','D6','D7','D8',
                    'E1','E2','E3','E4','E5','E6','E7','E8',
                    'F1','F2','F3','F4','F5','F6','F7','F8',
                    'G1','G2','G3','G4','G5','G6','G7','G8',
                    'H1','H2','H3','H4','H5','H6','H7','H8',
                    'q']
#where your ships are stored
my_ship_board = Board()
player_number = 0
alivePlayers = []

#will be an H or M
coord_dict = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8}
game_active = True
def setup_board():
    #ship would have a coord for start (A1), then horiz or vert (A1v) and up/down/left/right (A1vu)

   # ships =[ Ship('Carrier',5,'C'),Ship('Battleship',4,'B'),Ship('Destroyer',3,'D'),Ship('Submarine',3,'S'),Ship('Patrol Boat',2,'P')]
    ships = [Ship('Patrol Boat',2,'P')]
    for x in ships:
        get_ship_data(x)
        valid =place_ship(x)
        while valid == False:
            print("You cannot place your ship there. Try again")
            get_ship_data(x)
            valid =place_ship(x)
    display_board()

def get_ship_data(ship):
    ship_coord = input(f"Select a coordinate (ex: A1) for your {ship.name}? Length {ship.length}: ")
    ship_coord=ship_coord.upper()
    while (ship_coord not in grid_response):
        ship_coord = input("Select a row (A-H) and a column (1-8) or quit(q)\n-> ")
        ship_coord = ship_coord.upper()
    ship_direction = ''
    while (ship_direction not in ['h','v']):
        ship_direction = input("Which way will your ship go? Horizontal (H), or vertical (V)? ")
        ship_direction = ship_direction.lower()
    ship_alignment = ''
    if ship_direction == 'h':
        while (ship_alignment not in['l','r']):
            ship_alignment = input(f"Will your ship be to the left (L) or the right (R) of {ship_coord}? ")
            ship_alignment = ship_alignment.lower()
    elif ship_direction == 'v':
        while (ship_alignment not in['u','d']):
            ship_alignment = input(f"Will your ship be above (U) or below (D) {ship_coord}? ")
            ship_alignment = ship_alignment.lower()
    ship.set_position((str)(coord_dict[ship_coord[:1]])+ (str)(ship_coord[1:])+ship_direction+ship_alignment)

def place_ship(ship):
    #spots is array of possible places, with letters turned to numbers, everything as strings 
    spots = ship.return_places()
    for x in spots:
        if((int)(x[1])<1 or (int)(x[1])>8 or (int)(x[0])<1 or (int)(x[0])>8):
            return False        
   
        #if the row or column is <0 or >8, return false, it's out of bounds
        
    for x in spots:
        #change the numbers to the correct letters (1 = A)
        for coord,num in coord_dict.items():
            if ((str)(num) == (x[0])):
                x= x.replace(x[0], coord,1)     
        for thing in my_ship_board.board:
            if(thing == x):
                
                if(my_ship_board.is_taken(thing) == False):
                    my_ship_board.board[thing] = ship.length
                else:
                    return False
    return True
    
def display_board():
    print("This is your board")
    print("  1 2 3 4 5 6 7 8 ")
    print("-------------------")
    for x in my_ship_board.board:
        if x[1] == '1':
            print(f"{x[0]}|", end = "")        
        print(f"{my_ship_board.board[x]} ", end = "")
        if x[1] == '8':
            print("|\n", end = "")
    print("-------------------")




def getShot(coord):
    if my_ship_board.board[coord] != ' ' and my_ship_board.board[coord] != 'M':
       my_ship_board.board[coord] = 'H'
    else:
        my_ship_board.board[coord] = 'M'




def display_opponent_board(opponent_number,board):
    print(f"This is player {opponent_number}'s Board")
    print("  1 2 3 4 5 6 7 8 ")
    print("-------------------")
    for x in board:
        if board[x] != 'M'and board[x] !='H':
            board[x] = ' '
        if x[1] == '1':
            print(f"{x[0]}|", end = "")        
        print(f"{board[x]} ", end = "")
        if x[1] == '8':
            print("|\n", end = "")
    print("-------------------")
def inputLoop():
    response = 0

    ValueError = True
    while ValueError==True:
        opponent = (input("Select an opponent to fire on: "))
        try:
            val = int(opponent)
            ValueError = False
            if val == player_number:
                print("You can't shoot yourself")
                ValueError = True
            if val not in alivePlayers:
                print(f"Player {val} is not in the game")
                ValueError = True               
        except:
            ValueError = True
            print("Please print a number")
    while (response not in grid_response):
        response = input("Select a row (A-H) and a column (1-8) to fire at opponent or quit(q)")
        response = response.upper()
    return (str)(opponent)+response


def isDead():
    isDead = True
    for x in my_ship_board.board:
        if my_ship_board.board[x] != 'H' and my_ship_board.board[x] != ' ' and my_ship_board.board[x] != 'M':
            isDead = False
    return isDead
# Check CL arguments
if len(sys.argv) >= 3:
    try:
        server = sys.argv[1]
        port = int(sys.argv[2])
    except ValueError:
        print('Invalid Port Number')
        exit(0)
else:
    server = 'localhost'
    port = 6789

# Connect to Server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server, port))

# Send 'ReadyMessage' to Server
readyMessage = '10 Ready' + CRLF
clientSocket.send(readyMessage.encode())

# Loop to Wait for Connection
while(1):
    print("[Client] Waiting for begin message from server")
    wholeBeginMessage = clientSocket.recv(64).decode()
    beginMessage = wholeBeginMessage[:2]
    player_number = (int)(wholeBeginMessage[-1:])
    numberOfPlayers = int(wholeBeginMessage[20])
    print(f"[Client] Received from Server - [{beginMessage}]")
    print(f"There are {numberOfPlayers} players")
    s = 0
    while s < numberOfPlayers:
        alivePlayers.append(s+1)
        s +=1
    print(alivePlayers)
    print(f"You are player #{player_number}")
    beginCode = beginMessage.split(' ')[0]
    if beginCode == '15':
        print('[Client] Opponents Connected.')
        break
    else:
        clientSocket.send(readyMessage.encode())

# Game Loop
while(game_active == True):
    setup_board()

    # Ask for Input
    while(game_active == True):
        userInput = inputLoop()
        opponent =  int(userInput[:1])
        # Check for q
        if userInput == 'q':
            endMessage = '40 Close' + CRLF
            print("[Client] Ending Game.")
            print("[Client] Close Message sent to server.")
            clientSocket.send(endMessage.encode())
            exit(0) 
        # Send Input to Server
        inputMessage = '30 Choice ' + userInput + CRLF 
        print("Wating for opponents to fire")
        clientSocket.send(inputMessage.encode())
        # Receive input
        shotMessage = clientSocket.recv(4096).decode().split()        
        shot = []
        # OpponentsBoard = clientSocket.recv(4096).decode().split()\
        #grabbing all the coordinates in the shot message
        #There could be multiple if multiple people shot them
        for z in shotMessage:
            print(z + " ", end = '')
            if z in grid_response:
                shot.append(z)
                print()
            if z == "round":
                print()
        #calling the get shot message for each shot
        for z in shot:
            getShot(z)
        clientSocket.send(pickle.dumps(my_ship_board.board))
        display_opponent_board(opponent,pickle.loads(clientSocket.recv(4096)))
        if isDead() == True:
            print("You Died!!\n\n\n\n\n")
            clientSocket.send(('50 Player '+str(player_number)+' is now dead? ' + CRLF).encode())
            game_active = False
            break
        else:
            clientSocket.send(('60 Player '+str(player_number)+' did not die today' + CRLF).encode())
        display_board()
        deathMessages = []
        EntireDeathMessage = clientSocket.recv(4096).decode().split("?")
        for x in EntireDeathMessage:
            deathMessages.append(x.split(" "))
        if len(deathMessages) > 1:
            
            for deathMessage in deathMessages:
                if(deathMessage[0] == '50'):
                    print(f"Player {deathMessage[2]} is now dead ")
                    for z in alivePlayers:
                        if int(deathMessage[2]) == z:
                            alivePlayers.remove(z)
            if deathMessages[len(deathMessages)-1][4] == '1':
                print("You won!!!\n\n\n\n\n")
                game_active = False
                break
      

endMessage = '40 Close'
clientSocket.send(endMessage.encode())
clientSocket.close()



