import json
from constants import SIZE

class PlayerProxy():
    def __init__(self, client):
        self.client = client

    def _encode_data(self, message):
        message = str.encode(json.dumps(message))
        return message

    def register(self):
        data = self._encode_data(["register"])
        self.client.send(data)

        result = json.loads(self.client.recv(SIZE).decode("utf-8").strip())
        return result

    def receive_stones(self, stone):
        data = self._encode_data(["receive-stones", stone])
        self.client.send(data)

    def make_a_move(self, boards):
        data = self._encode_data(["make-a-move", [i.to_list() for i in boards]])
        self.client.send(data)
        result = json.loads(self.client.recv(SIZE).decode("utf-8").strip())
        return result

    def end_game(self):
        data = self._encode_data(["end-game"])
        self.client.send(data)

        result = json.loads(self.client.recv(SIZE).decode("utf-8").strip())
        return result

    def close(self):
        self.client.close()