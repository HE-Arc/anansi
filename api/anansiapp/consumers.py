import json
import random
from .serializers import GamePlayerSerializer, GameSerializer, ResponseCardSerializer, RoundResponseCardSerializer, RoundSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
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
                    'action': 'error',
                    'message': 'The game has already started.',
                }
                
                await self.send(text_data=json.dumps(message))
                
                # Close the connection cleanly, with a normal close frame, and a message indicating why the connection is closing.
                await self.close(code = 1000, reason = 'The game has already started.') 
                return

            # Get player name, if not provided, use Anonymous
            player_name = data['username'] if data['username'] != '' else 'Anonymous'
            
            # Create GamePlayer object
            self.player = await database_sync_to_async(GamePlayer.objects.create)(username=player_name, game=game)

            if created:
                # Add creator to the game, and update the game in database
                self.player.is_game_creator = True
                await database_sync_to_async(self.player.save)()
                
            # Get the game serialized
            ser_game = await self.get_game(game)

            # Send message to all players in game
            players = await self.get_game_players(game)

            game_creator = await self.get_game_creator(game)

            message = {
                'action': 'game_joined_or_created',
                'players': players,
                'game': ser_game,
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
                    'type': 'start_new_round',
                    'cloze_card_text': cloze_card.text,
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

            # Get the last round (last created)
            round = await database_sync_to_async(Round.objects.last)()
            
            # Create a RoundResponseCard with the card and the player
            await database_sync_to_async(RoundResponseCard.objects.create)(player=self.player, round=round, response_card=card)
            
            # Get the round serialized using sync_to_async
            ser_round = await self.get_current_round_serialized(round)
            
            # Get the number of cards sent in the last round
            cards_played_in_round_count = await self.get_cards_played_in_round_count(round)
            
            # Get the number of players in the game
            player_number = await self.get_game_players_number(self.player.game)
            
            # If all the players have sent their cards, send all the cards to the players
            if cards_played_in_round_count == player_number:
                # Get all the cards sent by the players
                cards = await self.get_cards_played_in_round(round)
                
                # Send the cards to the players
                message_cards = {
                    'action': 'display_response_cards',
                    'round': ser_round,
                    'cards': cards,
                }
                
                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        'type': 'basic_message_receive',
                        'message': json.dumps(message_cards),
                    }
                )
                
            else:
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
        elif action == "choose_round_winner": # The master has chosen a winner for the round
            # Get the card id of the winner
            card_id = data['card_id']
            
            # Get the card from the database
            card = await database_sync_to_async(RoundResponseCard.objects.get)(id=card_id)
            
            # Get the round for the game, and the last round (with no winner)
            current_round = await database_sync_to_async(Round.objects.last)()
            
            # Set the winner for the round
            current_round.round_response_card_winner = card
            
            # Save the round
            await database_sync_to_async(current_round.save)()
            
            # TODO : Increase winnir score
            
            
            # Get the winner card serialized
            ser_card = await self.get_responsecard(card)
            
            # Send a message to every player, with the winner card
            message = {
                'action': 'display_round_winner',
                'card': ser_card,
            }
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'basic_message_receive',
                    'message': json.dumps(message),
                }
            )
        elif action == "next_round":
            # Get the game
            game = self.player.game
            
            # Select a random player as the master
            master = await self.select_master(game)
            
            # Select a random cloze card
            cloze_card = await self.select_cloze_card()
            
            # Create a new round
            round = await database_sync_to_async(Round.objects.create)(game=game, master=master, cloze_card=cloze_card)
            
            # Start the round
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'start_new_round',
                    'cloze_card_text': cloze_card.text,
                }
            )
            

    # Receive message from game group
    async def basic_message_receive(self, event):
        ''' Receive a message from the game group and send it to the player '''
        message = event['message']
        await self.send(text_data=message)

    # Receive message from game group
    async def start_new_round(self, event):
        ''' Generate 6 random cards and send them to the players'''
        # Get 6 random cards
        cards = await self.get_random_response_cards(6)
        
        # Send the cards to the player
        message = {
            'action': 'start_new_round',
            'cards_count': len(cards),
            'cloze_card': event['cloze_card_text'],
            'cards': cards
        }

        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_random_response_cards(self, number_of_cards):
        ''' Get N random cards from the database, where N is the number of cards to get '''

        # Get the game based on the player
        game = self.player.game

        # Get the card deck (CardGame)
        card_game = game.cardgame # TODO : Get the card game from the game and use it

        # Get the cards (Card) from the card deck
        responseCards = ResponseCardSerializer(ResponseCard.objects.filter(cardgame=1), many=True).data

        # Return n random cards that have not already been distributed to other players
        return random.sample(responseCards, number_of_cards)

    # Get game creator
    @database_sync_to_async
    def get_game_creator(self, game):
        ''' Get the game creator '''
        # Get all the player in the game
        players = GamePlayer.objects.filter(game=game)
        
        # Get the player who created the game using filter
        for player in players:
            if player.is_game_creator:
                return player
        
        return None

    # Get game players serialized
    @database_sync_to_async
    def get_game_players(self, game):
        ''' Get the game players '''
        players = GamePlayer.objects.filter(game=game)
        
        return GamePlayerSerializer(players, many=True).data
    
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
    def get_cards_played_in_round_count(self, round):
        ''' Get the number of cards played in the round '''
        return RoundResponseCard.objects.filter(round=round).count()
    
    @database_sync_to_async
    def get_cards_played_in_round(self, round):
        ''' Get serialized cards played in the round '''
        cards = RoundResponseCard.objects.filter(round=round)
        
        serializer = RoundResponseCardSerializer(cards, many=True)
        
        return serializer.data
    
    # Transform a round to a serialized round
    @sync_to_async
    def get_current_round_serialized(self, round):
        ''' Get the current round serialized '''
        serializer = RoundSerializer(round)
        
        return serializer.data
        
    # Transform a ResponseCard to a serialized ResponseCard
    @sync_to_async
    def get_responsecard(self, responsecard):
        ''' Get the ResponseCard serialized '''
        serializer = RoundResponseCardSerializer(responsecard)
        
        return serializer.data
    
    # Get the game serialized
    @sync_to_async
    def get_game(self, game):
        ''' Get the game serialized '''
        serializer = GameSerializer(game)
        
        return serializer.data
