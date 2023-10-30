import random
from logger import Logger

class the_deck():
    def __init__(self):
        self.groups = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.suites = ["Spade", "Club", "Diamond", "Heart"]
        self.greatest_cards = ["Black Joker", "Red Joker"]
        self.logger = Logger().logger

    @property
    def create_deck(self):
        deck = []
        for i in self.groups:
            for n in self.suites:
                card = i + " " + n
                deck.append(card)
        deck.extend(self.greatest_cards)
        self.deck = deck
        return deck

    def get_cards(self):
        """
        Description:
            This function will get card in the deck.
        Parameters:
            None.
        Returns:
            received_card(str): This function will return the random card after the player receives.
        Raise:
            Exception: If player cannot get card with the corresponding error.
        """
        try:
            deck = self.create_deck
            def inner_function(name):
                if len(deck) == 0:
                    raise Exception(f"The current deck does not have any card for {name}")
                received_card = random.choice(deck)
                deck.remove(received_card)
                return received_card
            return inner_function
        except Exception as exc:
            raise Exception("Cannot get card with error: {}".format(exc))
    
    def compare_cards(self, first_card, second_card):
        """
        Description:
            This function will start a new round in the match.
        Parameters:
            reward_points(int): the reward points of Player.
        Returns:
            reward_points(int): This function will return the reward points after the round completed.
        Raise:
            Exception: If the cards cannot be compared the game with the corresponding error.
        """
        try:
            deck = self.create_deck
            if deck.index(first_card) > deck.index(second_card):
                return first_card
            else:
                return second_card
        except Exception as exc:
            raise Exception("Cannot compare cards with error: {}".format(exc))
