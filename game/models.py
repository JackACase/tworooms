from django.db import models
from datetime import datetime, timezone
import random
import game.game_logic as gl

# Create your models here.


class Game(models.Model):
    # the access code will be used to connect all players to a game instance
    access_code = models.CharField(max_length=256, unique=True)

    # TODO there will be a finite number of game states, use choices option
    state = models.CharField(max_length=256, default='waitingForPlayers')

    # a game may consist of either 3 or 5 rounds
    rounds = models.PositiveSmallIntegerField(default=3)

    current_round = models.PositiveSmallIntegerField(default=1)

    # playset = models.ForeignKey('Playset', on_delete=models.CASCADE, null=True)

    start_time = models.BigIntegerField(null=True)

    def __str__(self):
        return self.access_code

    def get_absolute_url(self):
        return '/game/' + self.access_code + '/'

    def new_game(self):
        """create a new game instance and return the access code string"""
        self.access_code = gl.generate_access_code()
        self.state = 'waitingForPlayers'
        self.save()
        return self.access_code

    def num_players(self):
        """return the current number of players in the game"""
        return Player.objects.filter(game=self).count()

    def get_player_list(self):
        return Player.objects.filter(game=self)

    def shuffle_cards(self):
        players = self.get_player_list()
        indices = range(len(players))
        shuffled = list(indices)
        random.shuffle(shuffled)
        for index, player in zip(shuffled, players):
            player.card_idx = index
            player.save()

    # def expand_playset(self):
    #     """Retrieve the cards from the selected playset from the database"""
    #     self.cards = []

    #     # append each card from the playset to the list of cards
    #     for card in self.playset.get_card_list():
    #         self.cards.append(card)

    #     # fill the remaining slots with red team and blue team
    #     red_card = Card.objects.get(name='Red Team')
    #     blue_card = Card.objects.get(name='Blue Team')
    #     for _ in range(0, int((self.num_players() - len(self.cards)) / 2)):
    #         self.cards.append(red_card)
    #         self.cards.append(blue_card)

    #     # fill in final slot for an odd number of players
    #     gambler_card = Card.objects.get(name='Gambler')
    #     if len(self.cards) != self.num_players():
    #         self.cards.append(gambler_card)

        # return self.cards


class Player(models.Model):
    name = models.CharField(max_length=256)
    is_moderator = models.BooleanField(default=False)
    game = models.ForeignKey(
        'Game', related_name='players', on_delete=models.CASCADE, null=True)
    card_idx = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def is_first_player(self):
        """the first player to join a game becomes the moderator"""
        if self.game.num_players() == 0:
            return True
        else:
            return False

    def join_game(self, access_code):
        """create a new player instance and connect to the game identified by the access code"""
        self.game = Game.objects.get(access_code=access_code)
        self.is_moderator = self.is_first_player()
        self.save()
        return self


# class Playset(models.Model):
#     name = models.CharField(max_length=256)
#     cards = models.ManyToManyField('Card')

#     def __str__(self):
#         return self.name

#     def get_card_list(self):
#         return Card.objects.filter(playset=self)


# class Card(models.Model):
#     name = models.CharField(max_length=256)

#     CARD_COLORS = [
#         ('RD', 'Red'),
#         ('BL', 'Blue'),
#         ('GR', 'Gray'),
#         ('PR', 'Purple'),
#         ('PK', 'Pink'),
#         ('GN', 'Green'),
#         ('YL', 'Yellow'),
#     ]

#     color = models.CharField(max_length=2, choices=CARD_COLORS, null=True)

#     tagline = models.TextField(null=True)
#     full_description = models.TextField(null=True)

#     def __str__(self):
#         return self.name + ' (' + self.color + ')'
