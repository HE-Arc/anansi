import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import logging
from .models import Game, GamePlayer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['room_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.player_name = ""
        self.player = None

        # Join game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):      
        # Remove the player from database
        if self.player_name and self.player:
            # await sync_to_async(GamePlayer.objects.get)(username=self.player_name)
            
            await sync_to_async(self.player.delete)()
            
            # Update players list for other players
            players_names = []
            async for p in GamePlayer.objects.filter(game=self.player.game):
                players_names.append(p.username)
            
            message = {
                'action': 'update_players',
                'players': players_names,
            }
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'player_list',
                    'message': json.dumps(message),
                }
            )
            
        # If the game (room) is empty, remove it from database
        # TODO

        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']

        if action == 'create_or_join_game':
            game = await sync_to_async(Game.objects.get_or_create)(name=self.game_name)
            
            # Join game
            # Get player name, if not provided, use Anonymous
            self.player_name = data['username'] if data['username'] != '' else 'Anonymous'
            
            game = await sync_to_async(Game.objects.get)(name=self.game_name)

            # Create GamePlayer object
            self.player = await sync_to_async(GamePlayer.objects.create)(username=self.player_name, game=game)

            # Send message to all players in game
            players_names = []
            async for p in GamePlayer.objects.filter(game=game):
                players_names.append(p.username)
            
            message = {
                'action': 'update_players',
                'players': players_names,
            }
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'player_list',
                    'message': json.dumps(message),
                }
            )
            
    # Receive message from game group
    async def player_list(self, event):
        message = event['message']
        await self.send(text_data=message)