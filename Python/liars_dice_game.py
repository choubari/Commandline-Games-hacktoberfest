"""
liars_dice_game.py
A game of Liar's Dice.
Copyright (C) 2018-2020 by Craig O'Brien and the t_games contributors.
See the top level __init__.py file for details on the t_games license.
Constants:
CREDITS: The credits for Liar's Dice. (str)
OPTIONS: The options for Liar's Dice. (str)
RULES: The rules for Liar's Dice. (str)
Classes:
ABBot: An honest Liar's Dice bot. (player.Bot)
Challenger: A Liar's Dice bot that challenges with other heuristics. (ABBot)
Liar: A Liar's Dice bot that lies more than it needs to. (ABBot)
DoubleTrouble: A Liar's Dice both that challenges and lies. (Challenger, Liar)
LiarsDice: A game of Liar's Dice. (game.Game)
"""


from __future__ import division

import collections
import itertools
import random

from .. import dice
from .. import game
from .. import player
from ..utility import num_text, YES


# The credits for Liar's Dice.
CREDITS = """
Game Design: Traditional
Game Programming: Craig "Ichabod" O'Brien
"""

OPTIONS = """
betting (b): Instead of tokens going out of the game, they go to the winner of
    the challenge.
challenge (chal): Add a bot with different challenge heuristics to the game.
double (dbl): Add a double trouble (challenger + liar) bot to the game.
gonzo (gz): Equivalent to 'betting tokens=1 two-rerolls'.
honest (abe): Add an honest (mostly) bot to the game.
liar (lr): Add a dishonest (sometimes) bot to the game.
tokens= (t=): Change the number of tokens each player has. (default = 3)
one-six (16): Ones count as sixes.
one-wild (1w): Ones are wild.
two-rerolls (2r): Each player can roll the dice twice before stating their
    claim.
Note that the default is to have one of each bot (honest, challenge, liar, and
    double trouble).
"""

# The rules for Liar's Dice.
RULES = """
There are five dice. The first player rolls them secretly, and announces what
they rolled. They can lie about what they rolled if they want. If the next
player thinks they are lying, they can challenge the current player. If the
current player is lying, they lose a token. If they are telling the truth,
the person who challenged loses a token.
If the next player accepts the current player's claim, the dice pass to the
next player. They can reroll any of the dice passed to them and then they must
make a new claim (they must also announce how many dice they rolled). The new
claim must be higher than the previous player's claim. Then the next player in
order gets a chance to challenge.
The claims are made in terms of poker hands. The order of hands, from highest
to lowest, is:
    * Five of a kind
    * Four of a kind
    * Full house
    * Straight
    * Three of a kind
    * Two pair
    * Pair
    * High card
All five dice are announced and count toward claims being "better" than the
previous claim. So four fives and a three is better than four fives and a two.
Each player starts with three tokens. The last person with tokens left wins
the game.
"""


class ABBot(player.Bot):
    """
    An honest Liar's Dice bot. (player.Bot)
    Well, as honest as they can be.
    Class Attributes:
    believable: Score changes that will not be challenged. (dict of int: list)
    conservative: Used instead of believable with one token left. (dict)
    Methods:
    claim_check: Decide whether or not to call someone a liar. (str)
    lie: Generate a lie based on the current claim. (list of int)
    make_claim: Make a claim about the current roll. (list of int)
    reroll_check: Decide which dice to reroll. (list of int)
    Overridden Methods:
    ask
    ask_int_list
    tell
    """

    # Score changes that will not be challenged.
    believable = {7: [], 6: [6], 5: [5, 6], 4: [], 3: [3, 5], 2: [2, 3, 5], 1: [1, 2, 3],
        0: [0, 1, 2, 3]}
    # Score changes that will not be challenged with one token left.
    conservative = {7: [], 6: [6, 7], 5: [5, 6], 4: [4], 3: [3, 5, 6], 2: [2, 3, 5], 1: [1, 2, 3],
        0: [0, 1, 2, 3]}

    def ask(self, query):
        """
        Ask the bot a question.
        Parameters:
        query: The question asked of the bot. (str)
        """
        if 'liar' in query:
            return self.claim_check()
        if 'must' in query:
            return 'uh oh'
        else:
            # Error on unknown questions.
            class_name = self.__class__.__name__
            raise player.BotError('Unexpected question to {}: {!r}'.format(class_name, query))

    def ask_int_list(self, prompt, low = None, high = None, valid = [], valid_lens = [], default = None,
        cmd = True):
        """
        Get a multiple integer response from the human. (int)
        Parameters:
        prompt: The question asking for the interger. (str)
        low: The lowest acceptable value for the integer. (list or None)
        high: The highest acceptable value for the integer. (laist or None)
        valid: The valid values for the integer. (list of int)
        valid_lens: The valid numbers of values. (list of int)
        default: The default choice. (list or None)
        cmd: A flag for returning commands for processing. (bool)
        """
        # Handle based on the question.
        if 'reroll' in prompt:
            # Check for already having beat the claim.
            if self.game.rolls_left:
                claim_score = self.game.poker_score(self.game.claim)
                roll_score = self.game.poker_score(self.game.dice.values)
                if claim_score[0] and roll_score > claim_score:
                    return []
            return self.reroll_check(valid)
        elif 'claim' in prompt:
            return self.make_claim(default)
        else:
            # Error on unexpected question.
            class_name = self.__class__.__name__
            raise player.BotError('Unexpected question to {}: {!r}'.format(class_name, prompt))

    def claim_check(self):
        """Decide whether or not to call someone a liar. (str)"""
        # Get the relevant scores.
        claim_score = self.game.poker_score(self.game.claim)
        prev_score = self.game.poker_score(self.game.history[-1])
        # Get the correct believability matrix.
        if self.game.scores[self] == 1:
            dont_challenge = self.conservative
        else:
            dont_challenge = self.believable
        # Get the number of changed dice.
        current = self.game.claim[:]
        old = self.game.history[-1]
        for die in old:
            if die in current:
                current.remove(die)
        changed = len(current)
        # Get the number of rolled dice.
        rolled = self.game.rerolls
        if self.game.base_rolls == 2:
            rolled *= 2
        # Determine the challenge.
        if changed > rolled:
            return 'yes'
        elif claim_score[0] in dont_challenge[prev_score[0]]:
            return 'nope'
        elif (self.game.base_rolls == 2 or self.game.one_wild) and claim_score[0] != 7:
            return 'nah'
        elif self.game.one_six and 6 in claim_score[1:4]:
            return 'no'
        else:
            return 'yup'

    def lie(self, claim_score, roll_score):
        """
        Generate a lie based on the current claim. (list of int)
        Parameters:
        claim_score: The poker_score output for the claim to lie about. (list of int)
        roll_score: The poker_score output for the actual roll. (list of int)
        """
        # Figure out what I kept.
        kept = roll_score[1:(6 - self.game.rerolls)]
        # Get the possible claims.
        rolls = itertools.product(range(1, 7), repeat = self.game.rerolls)
        possible = [self.game.poker_score(kept + list(roll)) for roll in rolls]
        possible = [score for score in possible if score > claim_score]
        # If no possible claims based on rerolls, assume rolled all five dice.
        if not possible:
            rolls = itertools.product(range(1, 7), repeat = 5)
            possible = [self.game.poker_score(list(roll)) for roll in rolls]
            possible = [score for score in possible if score > claim_score]
        # Pick something close to an improvement.
        possible.sort()
        return random.choice(possible[:3])[1:]

    def make_claim(self, roll):
        """
        Make a claim about the current roll. (list of int)
        Parameters:
        roll: What was actually rolled. (list of int)
        """
        # Get the scores for the roll and the previous claim.
        roll_score = self.game.poker_score(self.game.dice.values)
        claim_score = self.game.poker_score(self.game.claim)
        # Be honest if you can.
        if roll_score > claim_score:
            claim = roll
        else:
            # Otherwise, try and for the next highest claim.
            claim = self.lie(claim_score, roll_score)
        return claim

    def reroll_check(self, roll):
        """
        Decide which dice to reroll. (list of int)
        Parameters:
        roll: The dice that were rolled.
        """
        score = self.game.poker_score(roll)
        # Reroll any dice not involved in scoring the hand type.
        # Straights and five of a kind score on all dice.
        if score[0] in (4, 7):
            if score[0] == 4 and score[-1] == 1:
                reroll = [1]
            else:
                reroll = score[1:]
        # Four of a kind has one die to roll.
        elif score[0] == 6:
            reroll = [score[5]]
        # Three of kind/full house has two dice to reroll
        elif score[0] in (5, 3):
            reroll = score[-2:]
        # Two pair may reroll one or three dice.
        # (Three dice is just under 50% chance of improvement.)
        elif score[0] == 2:
            trigger = 6 - score[5]
            if trigger > score[3]:
                trigger += 1
            if trigger > score[1]:
                trigger += 1
            if trigger < 3:
                reroll = score[-3:]
            else:
                reroll = [score[5]]
        # One pair has three dice to reroll
        elif score[0] == 1:
            reroll = score[-3:]
        # For high card, keep the 6 and the 5 if there is one.
        elif score[0] == 0:
            reroll = roll[:]
        return reroll

    def tell(self, *args, **kwargs):
        """
        Give information to the player. (None)
        Parameters:
        The parameters are as per the built-in print function.
        """
        pass


class Challenger(ABBot):
    """
    A Liar's Dice bot that challenges with different heuristics. (ABBot)
    Class Attributes:
    valid_dice: The dice you would expect rolled for a give hand type. (dict)
    Overridden Methods:
    claim_check
    """

    # The dice you would expect rolled for a give hand type.
    valid_dice = {0: [1, 2, 3, 4, 5], 1: [3], 2: [1, 3], 3: [2], 4: [1, 5], 5: [2, 3], 6: [1], 7: [5]}

    def claim_check(self):
        """Decide whether or not to call someone a liar. (str)"""
        # Do the standard check.
        challenge = super(Challenger, self).claim_check()
        # If it isn't obvious, look at other heuristics.
        if challenge != 'yes':
            # Get the different claims with scores.
            current_score = self.game.poker_score(self.game.claim)
            old_score = self.game.poker_score(self.game.history[-1])
            if len(self.game.history) > 1:
                older_score = self.game.poker_score(self.game.history[-2])
            else:
                older_score = [-1, 0, 0, 0, 0, 0]
            # Get the possible rolls.
            rolled = self.game.rerolls
            kept = old_score[1:(6 - rolled)]
            rolls = itertools.product(range(1, 7), repeat = rolled)
            scores = [self.game.poker_score(kept + list(roll)) for roll in rolls]
            # Calculate the probability.
            as_good = [score for score in scores if score >= current_score]
            truth_chance = len(as_good) / len(scores)
            # Decide about the risk.
            my_score = self.game.scores[self.name]
            total_score = sum(self.game.scores.values())
            try:
                challenge_chance = random.random() < my_score / (total_score - my_score)
            except ZeroDivisionError:
                challenge_chance = True
            # Make determination.
            if current_score[0] == 7:
                challenge = 'yes'
            elif rolled not in self.valid_dice[old_score[0]] and not self.game.base_rolls == 2:
                challenge = 'da'
            elif truth_chance > 0.95 and challenge_chance and current_score[0]:
                challenge = '1'
            elif older_score[0] == current_score[0] and challenge_chance:
                challenge = 'si'
            else:
                challenge = '0'
        return challenge


class Liar(ABBot):
    """
    A Liar's Dice bot that lies more than it needs to. (ABBot)
    Overridden Methods:
    make_claim
    """

    def make_claim(self, roll):
        """
        Make a claim about the current roll. (list of int)
        Parameters:
        roll: What was actually rolled. (list of int)
        """
        # Get the standard claim.
        claim = super(Liar, self).make_claim(roll)
        # Consider lying if not already lying.
        if sorted(claim) != sorted(roll) and self.game.scores[self.name] > 1:
            score = self.game.poker_score(claim)
            if random.random() < (1 - score[0] / 5) / 2:
                claim = self.lie(score, self.game.poker_score(roll))
        return claim


class DoubleTrouble(Challenger, Liar):
    """A Liar's Dice both that challenges and lies. (Challenger, Liar)"""
    pass


class LiarsDice(game.Game):
    """
    A game of Liar's Dice. (game.Game)
    Class Attributes:
    bot_classes: The bot classes available for the game. (dict of str: class)
    hand_names: The name templates for the poker hand versions of the dice. (str)
    Attributes:
    base_rolls: The default number of rolls a player gets. (int)
    betting: A flag for passing tokens instead of losing them. (bool)
    claim: The claim made by the last player. (list of int)
    dice: The dice used in the game. (dice.Pool)
    history: The claims made since the last challenge. (list of list)
    last_roller: The last player to roll the dice. (player.Player)
    one_six: A flag for ones counting as sixes. (bool)
    one_wild: A flag for ones being wild. (bool)
    phase: The current action the player needs to take. (str)
    rerolls: How many dice the last player rerolled. (int)
    rolls_left: How many rolls the player can make. (int)
    thirteen: A flag for getting a token with a sum of 13. (bool)
    tokens: The number of tokens each player starts with. (int)
    Methods:
    challenge: Handle someone making a claim. (None)
    do_score: Show how many tokens players have left. (bool)
    one_six_adjust: Adjust value counts for the one-six option. (dict)
    one_wild_adjust: Adjust value counts for the one-six option. (tuple)
    poker_score: Generate a poker hand score for a set of values. (list of int)
    poker_text: Convert a poker score into text. (str)
    reroll: Reroll the dice. (None)
    reset: Reset the tracking variables. (None)
    resolve_challenge: Handle the result of a challenge. (None)
    thirteen_check: Check if there is a sum of dice equalling 13. (None)
    validate_claim: Validate that a claim is higher than the previosu one. (bool)
    Overridden Methods:
    game_over
    player_action
    set_options
    set_up
    """

    aka = ['Doubting Dice', 'Schummeln', 'Liars Dice', 'LiDi']
    aliases = {'scores': 'score'}
    bot_classes = {'challenger': Challenger, 'double': DoubleTrouble, 'honest': ABBot, 'liar': Liar}
    categories = ['Dice Games']
    credits = CREDITS
    hand_names = ['a six-high missing a {}', 'a pair of {}s with {}', 'two pair {}s over {}s with a {}',
        'three {}s with a {} and a {}', 'a {}-high straight', 'a full house {}s over {}s',
        'four {}s and a {}', 'five {}s']
    name = "Liar's Dice"
    num_options = 5
    options = OPTIONS
    rules = RULES

    def challenge(self):
        """Handle someone making a claim. (None)"""
        # Get the relevant players.
        player_index = self.player_index
        while True:
            player_index += 1
            next_player = self.players[(player_index) % len(self.players)]
            if self.scores[next_player.name]:
                break
        player = self.players[self.player_index]
        # Show the claim.
        claim_score = self.poker_score(self.claim)
        # Check for a challenge to the claim.
        if claim_score == [7, 6, 6, 6, 6, 6]:
            next_player.ask('The claim is five sixes, you must challenge. Press Enter to continue: ')
            challenge = 'yes'
        else:
            challenge = next_player.ask('Do you wish to call {} a liar? '.format(player.name))
        if challenge in YES or challenge[:4].lower() == 'liar':
            self.human.tell('{} challenges {}.'.format(next_player.name, player.name))
            # Show the real score.
            real_score = self.poker_score(self.dice.values)
            self.human.tell('{} actually had {}.'.format(player.name, self.poker_text(real_score)))
            # Handle challengers win.
            if claim_score > real_score:
                self.human.tell('{} is a liar.'.format(player.name))
                self.resolve_challenge(next_player, player)
            # Handle challenger loss
            else:
                self.human.tell('{} told the truth.'.format(player.name))
                self.resolve_challenge(player, next_player)
            self.phase = 'start'
            self.rolls_left = self.base_rolls - 1
        else:
            self.phase = 'reroll'
            self.rolls_left = self.base_rolls
            self.rerolls = 0

    def do_gipf(self, arguments):
        """
        Backgammon gives you a free reroll if you have a pair.
        Pyramid gives you a token if the next roll has any dice that sum to thirteen.
        """
        # Run the edge, if possible.
        game, losses = self.gipf_check(arguments, ('pyramid', 'backgammon'))
        # Winning Backgammon gives you a reroll if you have a pair.
        if game == 'backgammon':
            if not losses:
                score = self.poker_score(self.dice.values)
                if score[0] in (1, 2, 3, 5, 6, 7):
                    self.human.tell('\nYou get another roll.')
                    self.rolls_left += 1
                    self.phase = 'reroll'
                else:
                    self.human.tell('\nYou have no pair in your roll, so you do not get a reroll.')
        # Winning Pyramid gives you a token if you can make 13 next roll.
        elif game == 'pyramid':
            if not losses:
                message = '\nIf the sum of any dice from the next roll is 13, that player gets a token.'
                self.human.tell(message)
                self.thirteen = True
        # Otherwise I'm confused.
        else:
            self.human.tell("You believe that old wives' tale?")
        return True

    def do_score(self, arguments):
        """
        Show how many tokens each player has left. (scores)
        """
        # Show the scores
        self.human.tell()
        for score, name in self.sorted_scores():
            self.human.tell('{}: {}'.format(name, score))
        return True

    def game_over(self):
        """Check for the human losing or winning. (bool)"""
        # Check for the human being out of the game.
        if not self.scores[self.human.name]:
            # Record the win/loss/draw.
            before = len([player for player in self.players if not self.scores[player.name]]) - 1
            self.win_loss_draw = [before, len(self.players) - before - 1, 0]
            # Announce the loss.
            self.human.tell('\nYou have no more tokens, you lose the game.')
            before_text = num_text(before, 'player').capitalize()
            self.human.tell('{} left the game before you did.'.format(before_text))
        # Check for the human being the only one left.
        elif len([player for player in self.players if self.scores[player.name]]) == 1:
            # Announce and record the win.
            self.human.tell('\nYou win!')
            self.win_loss_draw = [len(self.scores) - 1, 0, 0]
        # Otherwise, continue.
        else:
            return False
        # If not continuing, end.
        return True

    def one_six_adjust(self, by_count, values):
        """
        Adjust value counts for the one-six option. (dict of int: list of int)
        Parameters:
        by_count: The counts and values with those counts. (dict of int: list of int)
        values: The values that were counted. (list of int)
        """
        # Get the one and six counts.
        ones = values.count(1)
        sixes = values.count(6)
        # Remove the counts (if they exist)
        if ones:
            by_count[ones].remove(1)
            if not by_count[ones]:
                del by_count[ones]
            if sixes:
                by_count[sixes].remove(6)
                if not by_count[sixes]:
                    del by_count[sixes]
            # Add the new count.
            by_count[ones + sixes].append(6)
        return by_count

    def one_wild_adjust(self, by_count, values):
        """
        Adjust value counts for the one-six option. (tuple of dict, list)
        Parameters:
        by_count: The counts and values with those counts. (dict of int: list of int)
        values: The values that were counted. (list of int)
        """
        # Get the count of wilds.
        ones = values.count(1)
        if ones:
            # Remove the count of ones.
            by_count[ones].remove(1)
            if not by_count[ones]:
                del by_count[ones]
            # Get the largest value with the largest count.
            try:
                max_count = max(by_count)
                max_value = max(by_count[max_count])
            # Note if there are five wilds.
            except ValueError:
                max_count = 0
            # Check for a straight
            if max_count == 1 and ones < 3:
                by_count = {1: [2, 3, 4, 5, 6]}
                values = [2, 3, 4, 5, 6]
            # Five wilds are five sixes.
            elif max_count == 0:
                by_count[5].append(6)
                values = [6] * 5
            else:
                # Otherwise increase the best group.
                by_count[max_count].remove(max_value)
                by_count[max_count + ones].append(max_value)
                # Delete the old best group if necessary.
                if not by_count[max_count]:
                    del by_count[max_count]
        return by_count, values

    def player_action(self, player):
        """
        Get a game action from the player. (None)
        Parameter:
        player: The current player. (player.Player)
        """
        # Skip players with no score.
        if not self.scores[player.name]:
            self.turns -= 1
            return False
        # Display the game state.
        if self.phase == 'start':
            self.dice.roll()
            self.last_roller = player
            self.reset()
            self.human.tell('\n{} starts a new round by rolling all five dice.'.format(player.name))
            player.tell('\nThe new roll to you is {}.'.format(self.dice))
            if self.thirteen:
                self.thirteen_check(player)
            if self.rolls_left:
                self.phase = 'reroll'
                self.rerolls = 5
            else:
                self.phase = 'claim'
        elif self.phase == 'reroll' and self.rolls_left == self.base_rolls:
            player.tell('\nThe roll passed to you is {}.'.format(self.dice))
        else:
            player.tell('\nYour roll is {}.'.format(self.dice))
        # Tell the player what they need to beat.
        if sum(self.claim):
            player.tell('You need to beat {}.'.format(self.poker_text(self.poker_score(self.claim))))
        # Get the player action
        if self.phase == 'claim':
            # Get the claimed value.
            query = 'Enter five numbers for your claim, or return to be honest: '
            claim = player.ask_int_list(query, low = 1, high = 6, valid_lens = [5],
                default = self.dice.values[:])
            # Handle other commands.
            if isinstance(claim, str):
                return self.handle_cmd(claim)
            # Validate the claim and check for a challenge.
            elif self.validate_claim(claim, player):
                self.challenge()
                return False
        elif self.phase == 'reroll':
            # Get the dice to reroll.
            query = 'Enter the numbers you would like to reroll: '
            rerolls = player.ask_int_list(query, valid = self.dice.values, valid_lens = range(6),
                default = [])
            # Handle other commands.
            if isinstance(rerolls, str):
                # Check for rerolling all of the dice
                if rerolls.lower() == 'all':
                    rerolls = self.dice.values[:]
                else:
                    return self.handle_cmd(rerolls)
            # Reroll the specified dice and move to making a claim.
            if isinstance(rerolls, list):
                self.reroll(player, rerolls)
        return True

    def poker_score(self, values):
        """
        Generate a poker hand score for a set of values. (list of int)
        The score is a list of integers. The first number is the type of hand, from 7
        for five of a kind to 0 for high card. The rest of the numbers are the dice
        values in comparison order for that type of hand. Therefore you can naively
        compare two poker_score integer lists to find out which is the higher hand.
        score[0] mapping:
            7 = five of a kind
            6 = four of a kind
            5 = full house
            4 = straight
            3 = three of a kind
            2 = two pair
            1 = pair
            0 = high card
        Parmeters:
        values: The claimed or rolled dice values. (lsit of int)
        """
        # Summarize the values.
        by_count = collections.defaultdict(list)
        for value in set(values):
            by_count[values.count(value)].append(value)
        # Account for ones being wild.
        if self.one_wild:
            by_count, values = self.one_wild_adjust(by_count, values)
        # Account for ones counting as sixes
        elif self.one_six:
            by_count = self.one_six_adjust(by_count, values)
            values = [(value if value != 1 else 6) for value in values]
        max_count = max(by_count)
        # Score by value.
        # Score a dummy hand.
        if 0 in values:
            score = [0] * 6
        # Score five of a kind.
        elif max_count == 5:
            score = [7] + by_count[5] * 5
        # Score four of a kind.
        elif max_count == 4:
            score = [6] + by_count[4] * 4 + by_count[1]
        # Score full house.
        elif max_count == 3 and 2 in by_count:
            score = [5] + by_count[3] * 3 + by_count[2] * 2
        # Score straight.
        elif max_count == 1 and (max(values) == 5 or min(values) == 2):
            score = [4] + sorted(values, reverse = True)
        # Score three of a kind.
        elif max_count == 3:
            score = [3] + by_count[3] * 3 + sorted(by_count[1], reverse = True)
        # Score high card (scored out of order to ensure 2 in by_count)
        elif max_count == 1:
            score = [0] + sorted(values, reverse = True)
        # Score two pair.
        elif len(by_count[2]) == 2:
            pairs = sorted(by_count[2], reverse = True)
            score = [2] + pairs[:1] * 2 + pairs[1:] * 2 + by_count[1]
        # Score a pair.
        else:
            score = [1] + by_count[2] * 2 + sorted(by_count[1], reverse = True)
        return score

    def poker_text(self, score):
        """
        Convert a poker score into text. (str)
        Parameters:
        score: A score returned by poker_score. (list of int)
        """
        # Get the hand name template.
        hand_name = self.hand_names[score[0]]
        # Fill in the template with the word versions of the numbers.
        # Five of a kind and straights need one word.
        if score[0] in (4, 7):
            hand_name = hand_name.format(num_text(score[1]))
        # Four of a kind and full house need the first and the last word.
        elif score[0] in (5, 6):
            hand_name = hand_name.format(num_text(score[1]), num_text(score[5]))
        # Three of a kind needs the first word and two trailing words.
        elif score[0] == 3:
            words = num_text(score[1]), num_text(score[4]), num_text(score[5])
            hand_name = hand_name.format(*words)
        # Two pair needs the odd numbered words.
        elif score[0] == 2:
            words = num_text(score[1]), num_text(score[3]), num_text(score[5])
            hand_name = hand_name.format(*words)
        # One pair needs the first word and three trailing words.
        elif score[0] == 1:
            trailers = ', '.join([num_text(value) for value in score[-3:]])
            hand_name = hand_name.format(num_text(score[1]), trailers)
        # High card needs the missing word.
        elif score[0] == 0:
            missing = [value for value in range(7) if value not in score][0]
            hand_name = hand_name.format(num_text(missing))
        # Return the hand name after fixing and six plural.
        return hand_name.replace('sixs', 'sixes')

    def reroll(self, player, rerolls):
        """
        Reroll the dice. (None)
        Paramters:
        player: The player rerolling. (player.Player)
        rerolls: The values to reroll. (list of int)
        """
        # Account for two-rerolls option.
        self.rerolls = max(self.rerolls, len(rerolls))
        # Announce the rerolls.
        if self.last_roller != player:
            line_feed = '\n'
        else:
            line_feed = ''
        self.last_roller = player
        reroll_text = num_text(len(rerolls), 'die', 'dice')
        self.human.tell('{}{} rerolled {}.'.format(line_feed, player.name, reroll_text))
        # Make the rerolls.
        for die_index, value in enumerate(self.dice.values):
            if value in rerolls:
                self.dice.roll(die_index)
                rerolls.remove(value)
        # Check for thirteens
        if self.thirteen and reroll_text != 'zero':
            self.thirteen_check(player)
        # Determine the next game phase.
        self.rolls_left -= 1
        if not self.rolls_left:
            self.phase = 'claim'

    def reset(self):
        """Reset the tracking variables. (None)"""
        self.claim = [0, 0, 0, 0, 0]
        self.history = []
        self.rerolls = 5
        self.rolls_left = self.base_rolls - 1

    def resolve_challenge(self, winner, loser):
        """
        Handle the result of a challenge. (None)
        Parameters:
        winner: The player who won the challenge. (player.Player)
        loser: The player who lost the challenge. (player.Player)
        """
        # Adjust and announce the loser's score.
        self.scores[loser.name] -= 1
        loser_score = self.scores[loser.name]
        if loser_score:
            plural = num_text(loser_score, 'token')
            self.human.tell('{} now has {}.'.format(loser.name, plural))
        if not self.scores[loser.name]:
            drop_message = '\n{} has lost all of their tokens and is out of the game.'
            self.human.tell(drop_message.format(loser.name))
        # Adjust and announce the winner's score.
        if self.betting:
            self.scores[winner.name] += 1
            plural = num_text(self.scores[winner.name], 'token')
            self.human.tell('{} now has {}.'.format(winner.name, plural))

    def set_options(self):
        """Set the game specific options. (None)"""
        # Set up the game options.
        self.option_set.add_option('betting', ['b'],
            question = 'Should lost tokens be given to the winner of the challenge? bool')
        self.option_set.add_option('two-rerolls', ['2r'], int, valid = (1, 2), target = 'base_rolls',
            default = 1, value = 2, question = 'How many rolls should you get (1 or 2, return for 1)? ')
        self.option_set.add_option('tokens', ['t'], int, check = lambda x: x > 0, default = 3,
            question = 'How many tokens should each player start with (return for 3)? ')
        self.option_set.add_option('one-six', ['16'], question = 'Should ones count as sixes? bool')
        self.option_set.add_option('one-wild', ['1w'], question = 'Should ones be wild? bool')
        # Set up the bot options.
        self.option_set.add_option('honest', ['abe'], action = 'bot', value = (), default = None)
        self.option_set.add_option('liar', ['lr'], action = 'bot', value = (), default = None)
        self.option_set.add_option('challenger', ['chal'], action = 'bot', value = (), default = None)
        self.option_set.add_option('double', ['dbl'], action = 'bot', value = (), default = None)
        # Set the default bots.
        self.option_set.default_bots = [(ABBot, ()), (Challenger, ()), (Liar, ()), (DoubleTrouble, ())]
        # Set the option groups.
        self.option_set.add_group('gonzo', ['gz'], 'betting tokens=1 two-rerolls')

    def set_up(self):
        """Set up the game. (None)"""
        # Mix up the players.
        random.shuffle(self.players)
        # Set up the scores.
        self.scores = {player.name: self.tokens for player in self.players}
        # Set up the dice.
        self.dice = dice.Pool([6] * 5)
        # Set up the tracking variables.
        self.reset()
        self.phase = 'start'
        self.thirteen = False

    def thirteen_check(self, player):
        """
        Check if there is a sum of dice equalling 13. (None)
        Parameters:
        player: The current player. (player.Player)
        """
        for size in range(3, 6):
            for sub_values in itertools.combinations(self.dice.values, size):
                if sum(sub_values) == 13:
                    self.thirteen = False
                    self.scores[player.name] += 1
                    sum_text = ' + '.join(str(value) for value in sub_values)
                    player.tell('{} = 13, you get an extra token.'.format(sum_text))
                    player.tell('You now have {} tokens.'.format(num_text(self.scores[player.name])))
                    break
            if not self.thirteen:
                break
        self.thirteen = False

    def validate_claim(self, claim, player):
        """
        Validate that a player's claim is higher than the previosu one. (bool)
        Parameters:
        claim: The current player's claimed roll. (list of int)
        player: The current player. (player.Player)
        """
        # Get the old and new scores.
        new_score = self.poker_score(claim)
        old_score = self.poker_score(self.claim)
        if new_score > old_score:
            # If new score is higher, update tracking and move on.
            self.human.tell('{} claims they have {}.'.format(player.name, self.poker_text(new_score)))
            self.history.append(self.claim)
            self.claim = claim
            return True
        else:
            # If the new score isn't higher, post a warning and ask again.
            new_text = self.poker_text(new_score)
            old_text = self.poker_text(old_score)
            message = 'Your claim of {} is not better than the previous claim of {}.'
            player.error(message.format(new_text, old_text))
            return False
