import random
from logger import Logger


class The_Deck():
    CARD_RANK = {
            "Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5,
            "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13,
            "Black Joker": 14, "Red Joker": 15
            }

    def __init__(self):
        self.suites = ["Spade", "Club", "Diamond", "Heart"]
        self.logger = Logger().logger

    @property
    def create_deck(self):
        deck = []
        for group, group_rank in self.CARD_RANK.items():
            for suit in self.suites:
                if group in ["Black Joker", "Red Joker"]:
                    # Joker cards do not have suites.
                    card = (group, group_rank, '')
                else:
                    card = (group, group_rank, suit)
                deck.append(card)
        return list(set(deck))

    def get_cards(self, deck):
        """
        Description:
            This function will get card in the deck.
        Parameters:
            deck(list): The deck of cards from which a card will be taken.
        Returns:
            received_card(str): This function will return the random card
                                after the player receives.
        Raise:
            Exception: If player cannot get card with the corresponding error.
        """
        def inner_function():
            nonlocal deck
            if len(deck) == 0:
                deck = self.create_deck
            received_card = random.choice(deck)
            deck.remove(received_card)
            return received_card
        return inner_function

    def compare_cards(self, house_card, player_card):
        """
        Description:
            This function compares the player's card with the house's card in
            a round of the match.
        Parameters:
            house_card(tuple): The house's card to be compared.
            player_card(tuple): The player's card to be compared.
        Returns:
            result(str): The result of the card comparison, which can be
                         "player's card higher" "equal"or "player's card lower"
        Raise:
            Exception: If the cards cannot be compared with corresponding error
        """
        try:
            if player_card[1] > house_card[1]:
                return "player's card higher"
            elif player_card[1] == house_card[1]:
                return 'equal'
            else:
                return "player's card lower"
        except Exception as exc:
            raise Exception("Cannot compare cards with error: {}".format(exc))
