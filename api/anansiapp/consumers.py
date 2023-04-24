import json
import random
from .serializers import ResponseCardSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import logging
from .models import ClozeCard, Game, GamePlayer, ResponseCard, Round, RoundResponseCard
from channels.db import database_sync_to_async


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['room_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.player = None

        # Join game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if self.player_name and self.player:
            game = self.player.game

            game_creator = await self.get_game_creator(game)

            # Remove the player from database
            await database_sync_to_async(self.player.delete)()

            # Get player from the game
            players = await self.get_game_players(game)
            players_names = [p.username async for p in players]

            # If there is no player, delete the room
            if len(players) == 0:
                await database_sync_to_async(game.delete)()

            else:  # If there are still players in the room

                # If the leaving player is the creator
                if self.player_name == game_creator.username:
                    # update the creator (change to the first player in the list)
                    game_creator = await sync_to_async(GamePlayer.objects.get)(game=game)
                    game.creator = game_creator
                    await sync_to_async(game.save)()

                # update the players list for other players
                message = {
                    'action': 'update_players',
                    'players': players_names,
                    'creator': game_creator.username,
                }

                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        'type': 'basic_message_receive',
                        'message': json.dumps(message),
                    }
                )

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
            game, created = await database_sync_to_async(Game.objects.get_or_create)(name=self.game_name)
                        
            # If the game is already started, send error message
            if not created and game.is_started:
                message = {
                    'action': 'game_already_started',
                }
                await self.send(text_data=json.dumps(message))
                return

            # Get player name, if not provided, use Anonymous
            player_name = data['username'] if data['username'] != '' else 'Anonymous'
            
            # Create GamePlayer object
            self.player = await database_sync_to_async(GamePlayer.objects.create)(username=player_name, game=game)

            if created:
                # Add creator to the game, and update the game in database
                game.creator = self.player
                await database_sync_to_async(game.save)()

            # Send message to all players in game
            players = await self.get_game_players(game)
            players_names = [p.username async for p in players]

            game_creator = await self.get_game_creator(game)

            message = {
                'action': 'update_players',
                'players': players_names,
                'creator': game_creator.username,
            }

            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'basic_message_receive',
                    'message': json.dumps(message),
                }
            )

        elif action == "start_game":
            # Update the game status to started
            game = self.player.game
            
            game.is_started = True
            
            await database_sync_to_async(game.save)()
            
            # Select a random player to be the master
            master = await self.select_master(game)
            
            # Select a cloze card
            cloze_card = await self.select_cloze_card()
            
            # Create a new round
            round = await database_sync_to_async(Round.objects.create)(game=game, master=master, cloze_card=cloze_card, round_number=0) 
            
            # Send a message to every player
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'generate_cards'
                }
            )
            
            # Send the number of players to every player
            player_number = await self.get_game_players_number(self.player.game)
            
            message = {
                'action': 'update_players_count',
                'player_number': player_number,
            }
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'basic_message_receive',
                    'message': json.dumps(message),
                }
            )
            
        elif action == "send_card": # A card is received from one player
            # Get the card from the card id received
            card_id = data['card_id']
            
            # Get the card from the database
            card = await database_sync_to_async(ResponseCard.objects.get)(id=card_id)
            
            # Get the round for the game, and the last round (with no winner)
            current_round = await database_sync_to_async(Round.objects.get)(game=self.player.game, round_response_card_winner=None)
            
            # Create a RoundResponseCard with the card and the player
            await database_sync_to_async(RoundResponseCard.objects.create)(player=self.player, round=current_round, response_card=card)
            
            # Get the number of cards sent by the players
            # Get the rounds for the game
            rounds = await database_sync_to_async(Round.objects.filter)(game=self.player.game)
            
            # Get the last round (with no winner)
            round = await database_sync_to_async(rounds.get)(round_response_card_winner=None)
            
            # Get the number of cards sent in the last round
            cards_played_in_round_count = await self.get_cards_played_in_round(round)
            
            # Send a message to every player, with the updated counter
            message = {
                'action': 'update_card_sent_counter',
                'card_sent_counter': cards_played_in_round_count,
            }
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'basic_message_receive',
                    'message': json.dumps(message),
                }
            )
            

    # Receive message from game group
    async def basic_message_receive(self, event):
        ''' Receive a message from the game group and send it to the player '''
        message = event['message']
        await self.send(text_data=message)

    # Receive message from game group
    async def generate_cards(self, event):
        ''' Generate 7 random cards and send them to the players'''
        # Get 7 random cards
        cards = await self.get_random_cards()

        # TODO : Fix this shit
        # cards_names = [(card.id, card.text) async for card in cards]

        # Send the cards to the player
        message = {
            'action': 'game_starting',
            'cards_count': len(cards),
            'cards': cards  # cards_names, # TODO : Fix this shit
        }

        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_random_cards(self):
        ''' Get 7 random cards from the database '''

        # Get the game based on the player
        game = self.player.game

        # Get the card deck (CardGame)
        card_game = game.cardgame

        # Get the cards (Card) from the card deck
        responseCards = ResponseCard.objects.filter(
            cardgame=1)

        print(responseCards)

        serializer = ResponseCardSerializer(responseCards, many=True)

        # Select 7 random cards
        # cards = responseCards  # random.sample(list(responseCards), 7)
        cards = serializer.data

        print(serializer.data)

        # TODO : Be sure that the cards have not already been distributed to other players

        return cards

    # Get game creator
    @database_sync_to_async
    def get_game_creator(self, game):
        ''' Get the game creator '''
        return game.creator

    # Get game players
    @database_sync_to_async
    def get_game_players(self, game):
        ''' Get the game players '''
        return GamePlayer.objects.filter(game=game)
    
    # Get card from id
    @database_sync_to_async
    def get_responsecard_from_id(self, card_id):
        ''' Get the card from the card id '''
        return ResponseCard.objects.get(id=card_id)
    
    # get game players number
    @database_sync_to_async
    def get_game_players_number(self, game):
        ''' Get the number of players in the game '''
        return GamePlayer.objects.filter(game=game).count()
    
    # Select a master
    @database_sync_to_async
    def select_master(self, game):
        ''' Select a random player to be the master '''
        # Get the game players
        players = GamePlayer.objects.filter(game=game)
        
        # Select a random player
        master = random.choice(players)
        
        # Set the player as the master
        game.master = master
        
        # Save the game
        game.save()
        
        return master
    
    # Select a cloze card
    @database_sync_to_async
    def select_cloze_card(self):
        ''' Select a random cloze card '''
        # Get the cloze cards
        # TODO : Select a cloze card from the selected card deck
        cloze_cards = ClozeCard.objects.all()
        
        # Select a random cloze card
        cloze_card = random.choice(cloze_cards)
        
        return cloze_card
    
    # Get the number of cards played in the round
    @database_sync_to_async
    def get_cards_played_in_round(self, round):
        ''' Get the number of cards played in the round '''
        return RoundResponseCard.objects.filter(round=round).count()
