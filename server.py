#############################################################################
# Program:
#    Lab 5 Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Matt Tyra
# Summary:
#   This code is for the rock paper scissors game using sockets. 
#   This is the server portion of the assignment.
#   I altered my Lab 4 in order to comply with the protocol set by the class
#
#*****************************************************************************
# RPS (rock/paper/scissors) Protocol Description
# ----------------------------------------------
# 10 Ready // From the client to tell server it is ready to begin the game.
# 15 Begin // From the server to tell the client that the game is starting.
# 30 Choice [value] // From the client to send the server the user's choice
# 35 Win [value] // From the server to tell the client it won the round
#                   and the value of the opponent's choice.
# 36 Lose [value] // From the server to tell the client it lost the round
#                   and the value of the opponent's choice.
# 37 Draw [value] // From the server to tell the client it tied the round
#                   and the value of the opponent's choice.
# 40 Close // From the client to tell the server it is closing its connection.
# 45 Close // From the server to tell the client to close its connection.
# 50 Invalid [expected code] // From client to say it received an invalid
# 55 Invalid [expected code] // From server to say it recevied invalid
##############################################################################

from os import read
import sys
import math
from board import Board
from socket import *
from client_object import Client
import pickle
CRLF = "\r\n"
LOOKUP = {'rp':False, 'rs':True, 'pr':False, 'sr':False, 'sp':True}
grid_response =     [['A1','A2','A3','A4','A5','A6','A7','A8'],
                    ['B1','B2','B3','B4','B5','B6','B7','B8'],
                    ['C1','C2','C3','C4','C5','C6','C7','C8'],
                    ['D1','D2','D3','D4','D5','D6','D7','D8'],
                    ['E1','E2','E3','E4','E5','E6','E7','E8'],
                    ['F1','F2','F3','F4','F5','F6','F7','F8'],
                    ['G1','G2','G3','G4','G5','G6','G7','G8'],
                    ['H1','H2','H3','H4','H5','H6','H7','H8'],
                    'q']

def makeShotMessage(playerNumber):
    shotMessage = ""
    print(f"PLayer nunber is {playerNumber}")
    for x in clients:
        print(f" {x.playerNumber}'s latest target is {x.latestTargetPlayer}")
        if(x.latestTargetPlayer == playerNumber):
            shotMessage += "player " + (str)(x.playerNumber) + " shot you at "+x.choice[2][1:] + " "
    if shotMessage == "":
        shotMessage = "You did not get shot this round"
    return shotMessage
        
####################################################
# Code Execution - Begins here
####################################################


try:
    while 1:
        print("[Server] The server is starting up...")
        DEFAULT_VALUE = 6789
        serverPort = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_VALUE
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('', serverPort))
        serverSocket.listen(1)
        print('[Server] The Server is ready to receive.\n')
        clients = []
        clientNumber = input("How many clients do you want?: ")
        for x in range(0,int(clientNumber)):
            clients.append(Client(x+1))
        for x in clients:
            x.connection, addr = serverSocket.accept()
            x.readyMessage = x.connection.recv(64).decode('ascii')
            x.readyCode = x.readyMessage[:2].split(' ')[0]
            print(f"[Server] Received from client {x.playerNumber}: [{x.readyMessage[:2]}]")
        allClientsReady = True
        for x in clients:
              if (x.readyCode != '10'):
                  allClientsReady = False
        if (allClientsReady == True):
            for x in clients:
                print(f"[Server] Received ready message from all {len(clients)} clients.\n")
                # Tell Clients they can Begin
                beginMessage = '15 Begin' + CRLF + 'There are ' + (str)(len(clients)) +' players\n\n You are player number '+ (str)(x.playerNumber)
                x.connection.send(beginMessage.encode())
                print(f"[Server] Sent [15 Begin] to Client {x.playerNumber}.")
            #Server Game loop
            while 1:
                # Receive choices {r,p,s,q}
                valid = True
                #loop to receive all the shots
                for x in clients:
                    if(x.isDead == False):
                        x.choice = x.connection.recv(64).decode().split()
                        print(f"[Server] Received from client {x.playerNumber} {x.choice}")


                    if x.choice[0] != '30':
                        valid = False
                #loop to set all the CLients choices and targets
                for x in clients:
                        if valid:
                            print(f"send attack. Player {x.playerNumber} is firing at Player {(int)(x.choice[2][0])}")
                            The_opponent = None
                            for y in clients:
                                if y.playerNumber ==(int)(x.choice[2][0]):
                                    The_opponent=y
                            
                            x.latestTargetPlayer = (int)(x.choice[2][0])
                    
                #loop to send the shot confirmation
                for x in clients:
                    shotMessage = makeShotMessage(x.playerNumber)
                    print(f"shot message is {shotMessage}")
                    #send the attack message
                    x.connection.send(shotMessage.encode())
                #loop to grab their board
                for x in clients:
                    x.Board = pickle.loads(x.connection.recv(4096)) 
                    #send the opponent board so the user can see what they hit
                for x in clients:
                    The_opponent = None
                    for y in clients:
                        if x.latestTargetPlayer == y.playerNumber:
                            The_opponent = y
                    x.connection.send(pickle.dumps(The_opponent.Board))
                    x.isDeadMessage = x.connection.recv(64).decode().split()
                someoneDiedThisRound = False
                deathMessage = ""
                for x in clients:
                    if x.isDeadMessage[0] == '50':
                        someoneDiedThisRound = True
                        print(f"Did someone die this round {someoneDiedThisRound}")
                        deathMessage += ' '.join(x.isDeadMessage)
                        x.isDead = True
             
                for x in clients[:]:
                    if x.isDead == True:
                        print(f"player {x.playerNumber} is dead, removing them from list")
                        clients.remove(x)
                for x in clients:
                    if  someoneDiedThisRound:
                            
                            print(f"x is player {x.playerNumber}")
                            deathMessage += " There are now "+ str(len(clients)) + " Player(s) left" + CRLF
                            print(deathMessage)
                            x.connection.send(deathMessage.encode())
                    if x.isDeadMessage[0] == '60' and someoneDiedThisRound == False:

                            deathMessage = "no die"+CRLF
                            x.connection.send(deathMessage.encode())
                if len(clients)==1:
                    print(f"The winner is player {clients[0].playerNumber}!!!")
                    break


       
except KeyboardInterrupt:
    print("\nClosing Server")
    serverSocket.close()
