import unittest
from unittest.mock import patch
from the_deck import The_Deck


class TestTheDeck(unittest.TestCase):

    @patch('the_deck.random.choice')
    def test_get_cards(self, mock_random_choice):
        mock_random_choice.side_effect = [
            ('2', 2, 'Diamond'), ('3', 3, 'Spade')]
        the_deck = The_Deck()
        create_deck = the_deck.create_deck
        get_card = the_deck.get_cards(create_deck)
        card1 = get_card()
        card2 = get_card()
        self.assertEqual(card1, ('2', 2, 'Diamond'))
        self.assertEqual(card2, ('3', 3, 'Spade'))

    @patch('the_deck.random.choice')
    def test_get_cards_with_empty_deck(self, mock_random_choice):
        the_deck = The_Deck()
        get_card = the_deck.get_cards(deck=[])
        mock_random_choice.side_effect = [('7', 7, 'Heart')]
        card = get_card()
        self.assertEqual(card, ('7', 7, 'Heart'))

    def test_compare_cards(self):
        the_deck = The_Deck()
        player_card = ('Ace', 1, 'Club')
        house_card = ('King', 12, 'Diamond')
        result = the_deck.compare_cards(house_card, player_card)
        self.assertEqual(result, "player's card lower")

        player_card = ('10', 10, 'Spade')
        house_card = ('2', 2, 'Diamond')
        result = the_deck.compare_cards(house_card, player_card)
        self.assertEqual(result, "player's card higher")

    def test_compare_cards_equal_result(self):
        the_deck = The_Deck()
        player_card = ('9', 9, 'Spade')
        house_card = ('9', 9, 'Diamond')
        result = the_deck.compare_cards(house_card, player_card)
        self.assertEqual(result, "equal")

    def test_compare_cards_with_error(self):
        the_deck = The_Deck()
        first_card = ('8', 'invalid')
        second_card = ('Jack', 8, 'invalid')
        with self.assertRaises(Exception) as context:
            the_deck.compare_cards(first_card, second_card)
        # Check the error message in the raised exception
        expected_message = "Cannot compare cards with error: '>' not " \
                           "supported between instances of 'int' and 'str'"
        self.assertEqual(str(context.exception), expected_message)
