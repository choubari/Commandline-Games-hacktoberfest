"""
crazy_eights_game.py
A game of Crazy Eights.
Copyright (C) 2018-2020 by Craig O'Brien and the t_games contributors.
See the top level __init__.py file for details on the t_games license.
Constants:
CREDITS: The credits for Crazy Eights. (str)
OPTIONS: The options for Crazy Eights. (str)
RULES: The rules for Crazy Eights. (str)
Classes:
Crazy8Bot: A basic Crazy Eights bot. (player.Bot)
CrazySmartBot: A smarter bot for Crazy Eights. (Crazy8Bot)
CrazyEights: A game of Crazy Eights (game.Game)
"""


from __future__ import division

import random

from .. import cards
from .. import game
from .. import options
from .. import player
from .. import utility


# The credits for Crazy Eights.
CREDITS = """
Game Design: Traditional (Venezuela)
Game Programming: Craig "Ichabod" O'Brien
"""

# The options for Crazy Eights.
OPTIONS = """
change= (c): The rank that allows you to change suits. (default = 8)
change-match (cm): The change suit card must match the discard's suit or rank.
change-set (cs): The change suit card only changes to it's own suit.
draw= (d): The rank, typically 2, that forces the next player to draw that many
    cards without playing any.
draw-one (d1): A player who can't play only has to draw one card.
easy= (e): The number of easy bots in the game. (default = 2)
empty-deck (ed): What to do when the deck is empty: pass (players can pass
    instead of drawing), reshuffle, or score. (default = score)
medium= (m): The number of medium bots in the game. (default = 2)
multi-score (ms): Each players scores the points in the largest hand minus the
    points in their own hand.
one-alert (1a): A warning is given when a player has one card.
one-round (1r): Only play one round.
psychotic (@, gonzo, gz): The four special ranks are set randomly, and change
    every deal.
reverse= (r): The rank, typically A, that reverses the order of play.
skip= (s): The rank, typically Q, that skips the next player.
To set a rank option to no rank, use ! instead of a rank character.
"""

# The rules for Crazy Eights.
RULES = """
Each player is dealt 5 cards, 7 in a two player game. The top card of the deck
is discarded face up. Each player in turn must discard a card face up that
matches the suit or rank of the top card on the discard pile. Any 8 may always
be played, and allows the player to pick a new suit to match. If a player
can't (or doesn't want to) play any cards, they may draw from the deck until
they can (or choose to) play a card.
When a player runs out of cards, the cards in all the other hands are added up
(face cards are 10, eights are 50, all other cards are face value), and the
player who ran out of cards scores that many points. If the deck runs out of
cards, the player with the least points in their hand scores the difference
between their points and the points in each hand. In the case of ties, the
points are split between the tied players. After scoring, all cards are
shuffled into the deck and the game is started again.
The first player to get 50 points times the number of players wins the game.
"""


class Crazy8Bot(player.Bot):
    """
    A basic Crazy Eights bot. (player.Bot)
    Attributes:
    discard: The card that was discarded. (cards.Card)
    eights: The eights that the bot has in hand. (list of cards.Card)
    hand: The bot's hand of cards. (cards.Hand)
    held_suit: The suit to switch to after playing an 8. (str)
    plays: The last round of plays in the game. (list of cards.Card)
    rank_matches: The bot's cards that match the rank to play. (list of Card)
    rank_suits: The suits of cards that match the current rank. (list of str)
    suit: The suit for the bot to match. (str)
    suit_matches: The bot's cards that match the suit to play. (list of Card)
    suits: The suits in hand and their counts. (list of (int, str))
    Methods:
    get_status: Calculate the legal plays and statistics of the game. (None)
    Overridden Methods:
    ask
    tell
    """

    def ask(self, prompt):
        """
        Get information from the player. (str)
        Parameters:
        prompt: The question being asked of the player. (str)
        """
        self.get_status()
        # Playing a card.
        if prompt == 'What is your play? ':
            # Play a suit match if possible.
            if self.suit_matches:
                self.suit_matches.sort()
                card = str(self.suit_matches[-1])
            # Otherwise play a rank match.
            elif self.rank_matches:
                self.rank_suits = [card.suit for card in self.rank_matches]
                for count, suit in self.suits:
                    if suit in self.rank_suits:
                        card = self.discard.rank + suit
                        break
            # Play eights as a last resort.
            elif self.eights:
                card = str(self.eights[0])
                self.held_suit = self.suits[0][1]
            # Draw if you can't play anything.
            elif self.game.deck.cards:
                card = 'draw'
                self.game.human.tell('{} drew a card.'.format(self.name))
            # Pass if you can.
            else:
                card = 'pass'
            # Inform the human.
            if card in self.hand.cards:
                self.game.human.tell('{} played the {}.'.format(self.name, card))
            return card
        # Choosing a suit.
        elif prompt == 'What suit do you choose? ':
            suit, self.held_suit = self.held_suit, None
            self.game.human.tell('The new suit to match is {}.'.format(suit))
            return suit
        # Avoid forced draw.
        elif prompt.endswith('(return to draw)? '):
            card = random.choice(self.rank_matches)
            self.game.human.tell('{} played the {}.'.format(self.name, card.rank + card.suit))
            return str(card)
        # Raise an error if you weren't programmed to handle the question.
        else:
            raise ValueError('Invalid prompt to Crazy8Bot: {!r}'.format(prompt))

    def get_status(self):
        """Calculate the legal plays and statistics of the game state. (None)"""
        # Get the relevant cards.
        self.discard = self.game.deck.discards[-1]
        self.hand = self.game.hands[self.name]
        # Get the current suit.
        if self.game.suit:
            self.suit = self.game.suit
        else:
            self.suit = self.discard.suit
        # Calculate the legal plays.
        self.suit_matches = [card for card in self.hand if card.suit == self.suit and
            card.rank != self.game.change_rank]
        self.rank_matches = [card for card in self.hand if card.rank == self.discard.rank and
            card.rank != self.game.change_rank]
        self.eights = [card for card in self.hand if card.rank == self.game.change_rank]
        # Check for change card matching.
        if self.game.change_match and self.discard.rank != self.game.change_rank:
            self.eights = [card for card in self.eights if card.suit == self.suit]
        # Calculate the frequencies of suits in hand.
        self.suits = []
        for suit in self.game.deck.suit_set:
            self.suits.append((len([card for card in self.hand if card.suit == suit]), suit))
        self.suits.sort(reverse = True)
        # Get the recent plays.
        self.plays = self.game.history[-len(self.game.players):]

    def tell(self, text = ''):
        """
        Give information to the player. (None)
        Parameters:
        The parameters are as per the built-in print function.
        """
        pass


class CrazySmartBot(Crazy8Bot):
    """
    A smarter bot for Crazy Eights. (Crazy8Bot)
    Methods:
    get_play: Get the next card to play. (str)
    Overridden Methods:
    ask
    """

    def ask(self, prompt):
        """
        Get information from the player. (str)
        Parameters:
        prompt: The question being asked of the player. (str)
        """
        self.get_status()
        # Playing a card.
        if prompt == 'What is your play? ':
            return self.get_play()
        # Choosing a suit.
        elif prompt == 'What suit do you choose? ':
            suit = self.suits[0][1]
            self.game.human.tell('The new suit to match is {}.'.format(suit))
            return suit
        # Avoid forced draw.
        elif prompt.endswith('(return to draw)? '):
            card = random.choice(self.rank_matches)
            self.game.human.tell('{} played the {}.'.format(self.name, card.rank + card.suit))
            return str(card)
        # Raise an error if you weren't programmed to handle the question.
        else:
            raise ValueError('Invalid prompt to CrazySmartBot: {!r}'.format(prompt))

    def get_play(self):
        """Get the next card to play. (str)"""
        # Check for suit having been switched.
        suit_switch = self.plays[0].suit != self.suit
        suit_switch = suit_switch or self.game.change_rank in [card.rank for card in self.plays]
        # Get the playable ranks.
        if self.game.change_match and self.discard.rank != self.game.change_rank:
            valid_ranks = (self.discard.rank,)
        else:
            valid_ranks = (self.discard.rank, self.game.change_rank)
        # Get the playabel cards.
        maybes = []
        for maybe in self.hand.cards:
            if maybe.suit == self.suit or maybe.rank in valid_ranks:
                maybes.append(maybe)
        maybes = {card: 0 for card in maybes}
        # Calculate the value of each card.
        final_card = None
        best_count = -5
        for card in maybes:
            if card.rank == self.game.change_rank:
                # Penalize eights by one point to hold them until needed.
                maybes[card] = self.suits[0][0] - 1
                if card.suit == self.suits[0][1]:
                    maybes[card] -= 1
                if suit_switch and self.suits[0][1] != self.suits:
                    maybes[card] += 2
            else:
                # Score cards by cards left in suit, plus two if it's a switch.
                maybes[card] = len([maybe for maybe in self.hand if maybe.suit == card.suit]) - 1
                if suit_switch and card.suit != self.suits:
                    maybes[card] += 2
            # Track  the best card.
            if maybes[card] > best_count:
                best_count = maybes[card]
                final_card = card
        # Make the move
        if final_card is None:
            # Handle not having a card to play.
            if self.game.deck.cards:
                self.game.human.tell('{} drew a card.'.format(self.name))
                return 'draw'
            else:
                return 'pass'
        else:
            # Play a card.
            self.game.human.tell('{} played the {}.'.format(self.name, final_card))
            return str(final_card)


class CrazyEights(game.Game):
    """
    A game of Crazy Eights. (game.Game)
    Attributes:
    any_card: A flag for being able to play any card. (bool)
    change_match: A flag for the change card having to match suit or rank. (bool)
    change_rank: The rank that allows the current suit to be changed. (str)
    change_set: A flag for the change chard only changing to it's own suit. (bool)
    deck: The deck of cards used in the game. (cards.Deck)
    draw_one: A flag for only having to draw one card when unable to play. (bool)
    draw_rank: The rank that forces a player to draw. (str)
    empty_deck: What to do when the deck is empty. (str)
    forced_draw: A flag for the next player being forced to draw cards. (bool)
    goal: The number of points needed to win the game. (int)
    hands: The player's hands. (dict of str: cards.Hand)
    history: The cards played so far. (list of cards.Card)
    last_player: The player to take the last action. (player.Player)
    multi_score: A flag for almost everyone scoring each round. (bool)
    num_players: The number of players requested. (int)
    num_easy: The number of easy bots requested. (int)
    num_medium: The number of easy bots requested. (int)
    one_alert: A flag for alerts when a player has one card. (bool)
    pass_count: How many players have passed in a row. (bool)
    reverse_rank: The rank that reverses the order of play. (str)
    skip_rank: The rank that skips the next player. (str)
    suit: The suit called with the last eight. (str)
    Methods:
    deal: Deal the cards to the players. (None)
    draw: Draw a card. (bool)
    force_draw: Draw extra cards due to special rank of previous play. (bool)
    help_ranks: Show the current special ranks in the game. (None)
    pass_turn: Pass the turn. (bool)
    play_card: Play a card. (bool)
    score: Score the round's winner. (None)
    validate_card: Validate a card to play. (bool)
    Overridden Methods:
    game_over
    handle_options
    player_action
    set_options
    set_up
    """

    aka = ['Rockaway', 'Swedish Rummy', 'CrEi']
    categories = ['Card Games']
    crazy_quotes = ("I don't really come from outer space.",
        "I'm a dog chasing cars. I wouldn't know what to do with one if I caught it!",
        "I'm insane and you are my insanity.", 'Colonics for everyone!',
        'Viddy well, little brother, viddy well.',
        "No. I don't keep count. But you do. And I love you for it.",
        'If I have to have a past, then I prefer it to be multiple choice.',
        "I'm a goddamn marvel of modern science.", 'When I was a little kid, I was just like anybody else.',
        "A long time ago being crazy meant something. Nowadays everybody's crazy.",
        'That is not dead which can eternal lie, and with strange aeons even death may die.',
        'All work and no play makes Jack a dull boy.')
    credits = CREDITS
    name = 'Crazy Eights'
    num_options = 13
    options = OPTIONS
    rules = RULES

    def deal(self, keep_one = False):
        """
        Deal the cards to the players. (None)
        Parameters:
        keep_one: A flag for keeping the top card of the discard pile. (bool)
        """
        # Keep the discard if requested.
        if keep_one:
            self.human.tell('Reshuffling the deck.')
            keeper = self.deck.discards[-1]
        else:
            # Empty the current hands.
            for hand in self.hands.values():
                hand.discard()
        # Reset and the deck.
        self.deck.shuffle()
        self.forced_draw = 0
        self.suit = ''
        # Set the discard pile.
        if keep_one:
            self.deck.discards = [keeper]
            self.deck.remove(keeper)
        else:
            self.deck.discard(self.deck.deal(), up = True)
            self.history.append(self.deck.discards[-1])
            self.human.tell('\nThe starting card is the {}.'.format(self.deck.discards[-1]))
            # Determine the number of cards to deal.
            if len(self.players) == 2:
                hand_size = 7
            else:
                hand_size = 5
            # Deal the cards.
            for card in range(hand_size):
                for player in self.players:
                    self.hands[player].draw()
            # Sort the human's hand for readability.
            self.hands[self.human].sort()

    def do_gipf(self, arguments):
        """
        Strategy allows you to play one rank above or below the current rank.
        Spider (hah!) allows you to play any card, but it doesn't change the suit to
        play.
        """
        # Run the edge, if possible.
        game, losses = self.gipf_check(arguments, ('strategy', 'spider'))
        # Winning Strategy gets you a fuzzy rank match.
        if game == 'strategy':
            if not losses:
                self.human.tell('\nYour next play may be one rank above or below the required rank.')
                self.fuzzy_ranks = True
        # Winning Spider (hah!) lets you play any card.
        elif game == 'spider':
            if not losses:
                self.human.tell("\nYou can play any card, but it won't change the suit for the next play.")
                self.any_card = True
        # Otherwise I'm confused.
        else:
            self.human.tell("I'm sorry, I quit gipfing for Lent.")
        return True

    def draw(self, player):
        """
        Draw a card. (bool)
        Parameters:
        player: The player to draw a card for. (player.Player)
        """
        # Check for a forced pass.
        if self.empty_deck == 'pass' and not self.deck:
            player.tell('You cannot draw, you must pass.')
            self.human.tell('{} passes.'.format(player.name))
            self.pass_count += 1
            if self.pass_count >= len(self.players):
                self.score()
                if max(self.scores.values()) < self.goal:
                    self.deal()
            return False
        # Draw the card.
        hand = self.hands[player.name]
        new_card = hand.draw()
        player.tell('You drew the {}.'.format(new_card))
        # Sort the human's cards.
        if player.name == self.human.name:
            hand.sort()
        # Check for empty deck.
        if not self.deck.cards:
            self.human.tell('The deck is empty.')
            if self.empty_deck == 'score':
                self.score()
            if self.empty_deck != 'pass':
                if max(self.scores.values()) < self.goal:
                    self.deal(self.empty_deck == 'reshuffle')
            return self.empty_deck != 'score' and not self.draw_one
        else:
            return not self.draw_one

    def force_draw(self, player):
        """
        Draw extra cards due to special rank of previous play. (bool)
        Parameters:
        player: The player to draw a card for. (player.Player)
        """
        # Check the hand for playable cards.
        hand = self.hands[player.name]
        playable = [card for card in hand if card.rank == self.draw_rank]
        # Check for chance to play.
        if not playable:
            player.tell('You must draw {} cards.'.format(self.forced_draw))
            if not self.deck.cards:
                player.tell('There are no cards to draw so you must pass.')
                return self.pass_turn(player)
        if playable:
            # Get the playable card.
            player.tell('You must play a {} or draw {} cards.'.format(self.draw_rank, self.forced_draw))
            query = 'Which {} would you like to play (return to draw)? '.format(self.draw_rank)
            while True:
                play = player.ask(query)
                if not play or play.lower() in ('d', 'draw'):
                    break
                elif play in hand.cards:
                    self.play_card(player, play)
                    return False
                else:
                    message = 'That is not a valid play. Please draw or play a {}.'
                    player.error(message.format(self.draw_rank))
        # Draw the cards.
        if self.deck:
            plural = utility.plural(self.forced_draw, 'card')
            self.human.tell('{} must draw {} {}.'.format(player.name, self.forced_draw, plural))
            for card in range(self.forced_draw):
                hand.draw()
                self.forced_draw = 0
                self.human.tell('{} drew a card.'.format(player.name))
                # Handle the deck running out.
                if not self.deck:
                    self.human.tell('The deck is empty.')
                    if self.empty_deck == 'score':
                        self.score()
                    if self.empty_deck != 'pass':
                        if max(self.scores.values()) < self.goal:
                            self.deal(self.empty_deck == 'reshuffle')
                    if self.empty_deck != 'reshuffle':
                        return False
        # Sort the human's cards.
        if player.name == self.human.name:
            hand.cards.sort()
        return False

    def game_over(self):
        """Check for the game being over. (bool)"""
        # Win if someone scored enough points.
        if max(self.scores.values()) >= self.goal:
            self.wins_by_score(show_self = False)
            return True
        else:
            return False

    def handle_options(self):
        """Handle the game options. (None)"""
        super(CrazyEights, self).handle_options()
        # Set up the players.
        self.players = [self.human]
        if not self.num_easy + self.num_medium:
            self.num_medium = 7
        for bot in range(self.num_easy):
            self.players.append(Crazy8Bot(self.players))
        for bot in range(self.num_medium):
            self.players.append(CrazySmartBot(self.players))
        # Set the winning score.
        if not self.goal:
            self.goal = 50 * len(self.players)

    def help_ranks(self):
        """Show the current special ranks in the game. (None)"""
        if self.psychotic:
            self.human.tell('\n', random.choice(self.crazy_quotes), sep = '')
        else:
            self.human.tell('\nThe current special ranks are:\n')
            if self.change_rank:
                rank_name = self.deck.rank_set.names[self.change_rank]
                self.human.tell('The rank to change the suit is {}.'.format(rank_name))
            if self.draw_rank:
                rank_name = self.deck.rank_set.names[self.draw_rank]
                self.human.tell('The rank to force drawing cards is {}.'.format(rank_name))
            if self.reverse_rank:
                rank_name = self.deck.rank_set.names[self.reverse_rank]
                self.human.tell('The rank to reverse the order of play is {}.'.format(rank_name))
            if self.skip_rank:
                rank_name = self.deck.rank_set.names[self.skip_rank]
                self.human.tell('The rank to skip the next player is {}.'.format(rank_name))

    def mental_health(self):
        """Perform a mental health evaluation."""
        if self.psychotic:
            # Get some random ranks.
            ranks = random.sample(self.all_ranks, 4)
            # Make sure eight is one of them.
            if '8' not in ranks:
                ranks[0] = '8'
            # Assign the roles randomly.
            random.shuffle(ranks)
            for rank, action in zip(ranks, ('change_rank', 'draw_rank', 'reverse_rank', 'skip_rank')):
                setattr(self, action, rank)

    def pass_turn(self, player):
        """
        Pass the turn. (bool)
        Parameters:
        player: The player whose turn it is. (Player)
        """
        # Check for a valid pass.
        if not self.deck and self.empty_deck == 'pass':
            self.human.tell('{} passes.'.format(player.name))
            self.pass_count += 1
            if self.pass_count >= len(self.players):
                self.score()
                if max(self.scores.values()) < self.goal:
                    self.deal()
            return False
        # Give appropriate error for invalid pass.
        elif self.empty_deck == 'pass':
            player.error('You may not pass until the deck is empty.')
        else:
            player.error('None shall pass.')
        return True

    def play_card(self, player, card_text):
        """
        Play a card. (bool)
        Parameters:
        player: The player whose turn it is. (Player)
        card_text: The card to play. (str)
        """
        # Play the card.
        hand = self.hands[player]
        hand.discard(card_text)
        # Update the tracking variables.
        self.history.append(self.deck.discards[-1])
        self.pass_count = 0
        # Handle crazy eights.
        if self.change_rank == card_text.upper()[0] and not self.change_set and hand:
            while True:
                suit = player.ask('What suit do you choose? ').upper()
                if suit and suit[0] in 'CDHS':
                    self.suit = suit[0]
                    break
                player.error('Please enter a valid suit (C, D, H, or S).')
        # Handle any card being playable.
        elif self.any_card:
            if not self.suit:
                self.suit = self.history[-2].suit
            self.any_card = False
        # Reset suit tracking.
        else:
            self.suit = ''
        # Handle forced draws.
        if self.draw_rank and self.draw_rank in card_text.upper():
            self.forced_draw += self.deck.rank_set.index(card_text[0].upper())
        # Check for reversing the order of play.
        if card_text[0].upper() == self.reverse_rank:
            self.human.tell('The order of play is reversed.')
            self.players.reverse()
            self.player_index = self.players.index(player)
        # Check for skipping players.
        if card_text[0].upper() == self.skip_rank:
            skipped = self.skip_player()
            self.human.tell("{}'s turn is skipped.".format(skipped))
        # Check for playing their last card.
        if not hand:
            self.human.tell('{} played their last card.'.format(player.name))
            self.score()
            if max(self.scores.values()) < self.goal:
                self.deal()
            self.forced_draw = 0
        # Check for one card warning.
        elif self.one_alert and len(hand.cards) == 1:
            self.human.tell('{} has one card left.'.format(player.name))

    def player_action(self, player):
        """
        Handle a player's turn or other player actions. (bool)
        Parameters:
        player: The player whose turn it is. (Player)
        """
        if self.last_player != player or player == self.human:
            self.human.tell()
        self.last_player = player
        # Get the relevant cards.
        hand = self.hands[player.name]
        discard = self.deck.discards[-1]
        # Show the game status.
        player.tell('The card to you is {:u}.'.format(discard))
        if self.suit:
            player.tell('The suit to you is {}.'.format(self.suit))
        player.tell('Your hand is {}.'.format(hand))
        # Check for forced draw.
        if self.forced_draw:
            return self.force_draw(player)
        # Get and process the move.
        move = player.ask('What is your play? ')
        # Draw cards.
        if move.lower() in ('d', 'draw'):
            return self.draw(player)
        # Pass
        elif move.lower() in ('p', 'pass'):
            return self.pass_turn(player)
        # Play cards.
        elif move in hand.cards:
            return self.validate_card(player, move)
        # Handle playing cards they don't have.
        elif self.deck.card_re.match(move.strip()):
            player.error('You do not have that card in your hand.')
            return True
        # Handle other commands.
        else:
            return self.handle_cmd(move)

    def score(self):
        """Score the round's winner. (None)"""
        # Set up the loop.
        round_scores = {player.name: 0 for player in self.players}
        winner = ''
        low_score = 10000
        # Score each hand.
        self.human.tell()
        for name, hand in self.hands.items():
            for card in hand:
                # !! redo with a FeatureSet (don't forget psychotic)
                if card.rank == self.change_rank:
                    round_scores[name] += 50
                elif card.rank in 'TJQK':
                    round_scores[name] += 10
                elif card.rank == 'A':
                    round_scores[name] += 1
                else:
                    round_scores[name] += int(card.rank)
            # Track the lowest hand to find the winner(s).
            if round_scores[name] < low_score:
                winners = [name]
                low_score = round_scores[name]
            # Record any ties for lowest score.
            elif round_scores[name] == low_score:
                winners.append(name)
            self.human.tell('{} had {} points in their hand.'.format(name, round_scores[name]))
        if self.multi_score:
            self.human.tell()
            # Get the max score.
            max_score = max(round_scores.values())
            for name, score in round_scores.items():
                player_score = max_score - score
                self.scores[name] += player_score
                self.human.tell('{} scores {} points.'.format(name, player_score))
            self.human.tell()
        else:
            # Get score relative to lowest score and total it.
            winner_bump = 0
            for name in round_scores:
                round_scores[name] -= low_score
                winner_bump += round_scores[name]
            # Lowest score scores the relative total, divided by the number of players with that score.
            winner_bump = int(winner_bump / len(winners))
            self.human.tell()
            for winner in winners:
                self.human.tell('{} scores {} points.'.format(winner, winner_bump))
                self.scores[winner] += winner_bump
        # Announce the scores.
        self.human.tell()
        for player in self.players:
            self.human.tell('{} has {} points.'.format(player.name, self.scores[player.name]))
        # Perform a mental health evaluation.
        self.mental_health()

    def set_options(self):
        """Define the options for the game. (None)"""
        # Get rank handlers.
        rank_set = cards.STANDARD_RANKS
        rank_error = 'The valid card ranks are {}.'.format(', '.join(rank_set.chars))
        def convert_rank(text):
            if text == '!':
                text = ''
            return text.upper()
        # Set the card options.
        self.option_set.add_option('change-match', ['cm'],
            question = 'Should the suit change card have to match the last card played? bool')
        self.option_set.add_option('change-set', ['cs'],
            question = 'Should the suit change card just change to its own suit? bool')
        self.option_set.add_option('change', ['c'], convert_rank, '8', valid = rank_set,
            question = 'What rank should change the suit? ', error_text = rank_error,
            target = 'change_rank')
        self.option_set.add_option('draw', ['d'], convert_rank, '', valid = rank_set,
            question = 'What rank should force the next player to draw? ', error_text = rank_error,
            target = 'draw_rank')
        self.option_set.add_option('reverse', ['r'], convert_rank, '', valid = rank_set,
            question = 'What rank should reverse the order of play? ', error_text = rank_error,
            target = 'reverse_rank')
        self.option_set.add_option('skip', ['s'], convert_rank, '', valid = rank_set,
            question = 'What rank should skip the next player? ', error_text = rank_error,
            target = 'skip_rank')
        self.option_set.add_option('psychotic', ['@', 'gonzo', 'gz'],
            question = 'Are you mentally divergent, friend? bool')
        # Set the bot options.
        self.option_set.add_option('easy', ['e'], int, 2, valid = range(10), target = 'num_easy',
            question = 'How many easy bots should there be (return for 2)? ')
        self.option_set.add_option('medium', ['m'], int, 2, valid = range(10), target = 'num_medium',
            question = 'How many medium bots should there be (return for 2)? ')
        # Set the play options.
        self.option_set.add_option('one-alert', ['1a'],
            question = 'Should there be an alert when a player has only one card left? bool')
        self.option_set.add_option('empty-deck', ['ed'], options.lower, default = 'score',
            valid = ('pass', 'reshuffle', 'score'),
            question = 'What should be done when the deck is empty (return for score)? ',
            error_text = 'Valid responses are pass, reshuffle, or score.')
        self.option_set.add_option('one-round', ['1r'], target = 'goal', value = 1, default = 0,
            question = 'Should the game end after one round? bool')
        self.option_set.add_option('multi-score', ['ms'],
            question = 'Should everyone but the player with the highest hand score each time? bool')
        self.option_set.add_option('draw-one', ['d1'],
            question = 'Should you only have to draw one card if you cannot play a card? ')

    def set_up(self):
        """Set up the game. (None)"""
        # Set up the deck.
        if len(self.players) < 6:
            self.deck = cards.Deck(shuffle_size = -1)
        else:
            self.deck = cards.Deck(decks = 2, shuffle_size = -1)
        self.all_ranks = self.deck.rank_set.chars
        # Perform a mental health evaluation.
        self.mental_health()
        # Set up the tracking variables.
        self.history = []
        self.suit = ''
        self.pass_count = 0
        self.forced_draw = 0
        self.any_card = False
        self.fuzzy_ranks = False
        self.last_player = None
        # Deal the hands.
        self.hands = self.deck.player_hands(self.players)
        self.deal()
        # Randomize the players.
        random.shuffle(self.players)

    def validate_card(self, player, card_text):
        """
        Validate a card to play. (bool)
        Parameters:
        player: The player playing the card. (Player)
        card_text: The card the player entered. (str)
        """
        # Get the relevant cards.
        hand = self.hands[player.name]
        discard = self.deck.discards[-1]
        # Get the valid ranks.
        if self.change_match:
            valid_ranks = (discard.rank,)
        else:
            valid_ranks = (discard.rank, self.change_rank)
        # Account for fuzzy ranks.
        if self.fuzzy_ranks:
            rank_index = discard.rank_num
            if rank_index > 0:
                valid_ranks += (discard.rank_set.chars[rank_index - 1],)
            if rank_index + 1 < len(discard.rank_set):
                valid_ranks += (discard.rank_set.chars[rank_index + 1],)
        # Get the valid suit.
        if self.suit:
            valid_suit = self.suit
        else:
            valid_suit = discard.suit
        # Check the card.
        if card_text[0].upper() in valid_ranks or card_text[1].upper() in valid_suit or self.any_card:
            self.play_card(player, card_text)
            self.fuzzy_ranks = False
        # Warn for invalid plays.
        else:
            player.error('That is not a valid play.')
            return True
        return False
