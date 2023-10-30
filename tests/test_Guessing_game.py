import unittest
from unittest.mock import patch
from MainGame import NumberGuessingGame

class TestNumberGuessingApp(unittest.TestCase):

    @patch('MainGame.utilities.validate_input', return_value='no')
    def test_start_game(self, mock_input):
        game = NumberGuessingGame("Player")
        game.start_game()
        self.assertEqual(game.player_points, 60)


    @patch('MainGame.utilities.validate_input', return_value='yes')
    @patch('MainGame.NumberGuessingGame.start_round')
    def test_start_match(self, mock_start_round, mock_input):
        game = NumberGuessingGame('Player')
        mock_start_round.return_value = (0, 2)
        player_points = game.start_match(60)
        self.assertEqual(player_points, 35)


    @patch('MainGame.the_deck.get_cards')
    @patch('MainGame.utilities.validate_input', return_value='greater')
    def test_start_round(self, mock_input, mock_deck):
        deck_instance = mock_deck.return_value
        deck_instance.return_value = "Red Joker"

        game = NumberGuessingGame('Player')
        reward, number_round = game.start_round(20, 1)

        self.assertEqual(reward, 40)
        self.assertEqual(number_round, 2)


if __name__ == '__main':
    unittest.main()
