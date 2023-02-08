import json
from socket import socket, AF_INET, SOCK_STREAM, timeout
from time import sleep

from constants import SIZE, BOARD_ROW_LENGTH, BOARD_COL_LENGTH
from player import Player
from board import Board

def main():
    server = socket(AF_INET, SOCK_STREAM)
    with open('go.config') as f:
        data = json.load(f)
        IP = data["IP"]
        port = data["port"]
    address = (IP, port)

    while(True):
        try:
            server.connect(address)
            break
        except ConnectionRefusedError:
            sleep(2)

    p1 = Player("alphabeta",2,BOARD_ROW_LENGTH,BOARD_COL_LENGTH)
    
    while True:
        try:
            received = server.recv(SIZE).decode("utf-8").strip()            
            if received == "":
                break
            
            received = json.loads(received)

            if received[0] == "register":
                result = p1.register()
                result = str.encode(json.dumps(result))
                server.send(result)

            elif received[0] == "receive-stones":
                result = p1.receive_stones(received[1])

            elif received[0] == "make-a-move":
                result = p1.make_a_move([Board(i) for i in received[1]])
                result = str.encode(json.dumps(result))
                print('result',result)
                server.send(result)

            elif received[0] == "end-game":
                result = p1.end_game()
                result = str.encode(json.dumps(result))
                server.send(result)
        except:
            break

    server.close()
        
if __name__ == "__main__":
    main()