import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name
        self.players = []

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        self.players.append(username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "game_join",
                                   "username": username, "players": self.players}
        )

    def game_join(self, event):
        username = event['username']
        players = event['players']
        self.send(text_data=json.dumps({
            "type": "game_join",
            "username": username,
            "players": players
        }))
