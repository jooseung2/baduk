import json, sys
from socket import socket, AF_INET, SOCK_STREAM, timeout
from time import sleep
from rulechecker import RuleChecker

from constants import SIZE, STONES, BOARD_COL_LENGTH, BOARD_ROW_LENGTH
from board import Board

def main():
    server = socket(AF_INET, SOCK_STREAM)
    with open('go.config') as f:
        data = json.load(f)
        IP = data["IP"]
        port = data["port"]
    
    address = (IP, port)
    rc = RuleChecker(BOARD_COL_LENGTH, BOARD_ROW_LENGTH)
    my_stone = None
    registered = False

    while(True):
        try:
            server.connect(address)
            break
        except (ConnectionRefusedError, OSError):
            sleep(2)
    
    while True:
        try:
            received = server.recv(SIZE).decode("utf-8").strip()         
            if received == "":
                print('No response from the game server, terminating.')
                break
            
            received = json.loads(received)

            if received[0] == "register":
                if len(received) > 1:
                    print('[register] weird input from admin: {}\nexiting'.format(received))
                    break

                print("register your name: ")
                result = sys.stdin.readline().rstrip('\n')
                result = str.encode(json.dumps(result))
                server.send(result)
                registered = True

            elif received[0] == "receive-stones":
                if not registered:
                    print('not registered')
                    break

                if len(sys.argv) > 1 and sys.argv[1] == "1":
                    print('receive-stones close connection')
                    server.close()

                if my_stone is not None:
                    print('[receive-stones] I already have a stone, exiting')
                    break
                if len(received) != 2 or received[1] not in STONES:
                    print('[receive-stones] weird input from admin: {}\nexiting'.format(received))
                    break

                print('received {} stones'.format(received[1]))
                my_stone = received[1]

            elif received[0] == "make-a-move":
                if not registered:
                    print('not registered')
                    break
                
                if len(received) != 2:
                    print('[make-a-move] weird input from admin: {}\nexiting'.format(received))
                    break
                if not Board.validate_boards_list(received[1]):
                    print('[make-a-move] invalid boards format from admin: {}\nexiting'.format(received[1]))
                    break

                boards = [Board(i) for i in received[1]]
                if not rc.check_history(my_stone, boards):
                    print('[make-a-move] invalid boards history from admin: {}\nexiting'.format(boards))
                    break

                [print(board) for board in boards]
                print("make a move: ")

                if len(sys.argv) > 1 and sys.argv[1] == "3":
                    sleep(5)

                if len(sys.argv) > 1 and sys.argv[1] == "2":
                    print('make-a-move close connection')
                    server.close()

                result = sys.stdin.readline().rstrip('\n')
                result = str.encode(json.dumps(result))
                server.send(result)

            elif received[0] == "end-game":
                if not registered:
                    print('not registered')
                    break

                
                if len(received) != 1:
                    print('[end-game] weird input from admin: {}\nexiting'.format(received))
                    break

                print("game end. say OK to proceed: ")
                result = sys.stdin.readline().rstrip('\n')

                if result == "OK":
                    my_stone = None

                result = str.encode(json.dumps(result))
                server.send(result)

            else:
                print("Received")
                
        except Exception as e:
            print(e)
            break

    server.close()
        
if __name__ == "__main__":
    main()