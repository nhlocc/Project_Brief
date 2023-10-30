import unittest
from unittest.mock import patch
from the_deck import the_deck

class TestTheDeck(unittest.TestCase):

    @patch('the_deck.random.choice')
    def test_get_cards(self, mock_random_choice):
        mock_random_choice.side_effect = ["2 Spade", "3 Club"]
        deck = the_deck()
        get_card = deck.get_cards()
        card1 = get_card("Player 1")
        card2 = get_card("Player 2")
        self.assertEqual(card1, "2 Spade")
        self.assertEqual(card2, "3 Club")

    @patch('the_deck.the_deck.create_deck')
    def test_get_cards_with_empty_deck(self, mock_create_deck):
        deck = the_deck()
        mock_create_deck.return_value = []
        with self.assertRaises(Exception) as context:
            get_card_function = deck.get_cards()
            get_card_function("Player")
        expected_message = "The current deck does not have any card for Player"
        self.assertEqual(str(context.exception), expected_message)

    def test_compare_cards(self):
        deck = the_deck()
        first_card = "5 Diamond"
        second_card = "5 Club"
        result = deck.compare_cards(first_card, second_card)
        self.assertEqual(result,first_card )

    def test_compare_cards_with_error(self):
        deck = the_deck()
        first_card = "10 invalid"
        second_card = "10 Club"
        with self.assertRaises(Exception) as context:
            deck.compare_cards(first_card, second_card)
        # Check the error message in the raised exception
        expected_message = "Cannot compare cards with error: '10 invalid' is not in list"
        self.assertEqual(str(context.exception), expected_message)


