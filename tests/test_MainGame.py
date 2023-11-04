import unittest
from unittest.mock import patch, call
from MainGame import NumberGuessingGame


class TestNumberGuessingApp(unittest.TestCase):

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'yes'])
    @patch('MainGame.Logger')
    def test_start_game_with_player_win(self, mock_logger, mock_input):
        game = NumberGuessingGame("Player")
        with patch('MainGame.NumberGuessingGame.start_match') as mock_start_match:
            mock_start_match.side_effect = [60, 1040]
            game.start_game()
            last_logger_message = mock_logger.mock_calls[-1]
            expected_logger_message = call().logger.info(
                'Congratulations! You won this game\n')
            assert last_logger_message == expected_logger_message
        self.assertEqual(game.player_points, 1040)

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'yes'])
    @patch('MainGame.Logger')
    def test_start_game_with_player_lose(self, mock_logger, mock_input):
        game = NumberGuessingGame("Player")
        with patch('MainGame.NumberGuessingGame.start_match') as mock_start_match:
            mock_start_match.side_effect = [35, 0]
            game.start_game()
            last_logger_message = mock_logger.mock_calls[-1]
            expected_logger_message = call().logger.info(
                'Game Over. You lost this game\n')
            assert last_logger_message == expected_logger_message
        self.assertEqual(game.player_points, 0)

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'no'])
    @patch('MainGame.Logger')
    def test_start_game_with_player_stop(self, mock_logger, mock_input):
        game = NumberGuessingGame("Player")
        with patch('MainGame.NumberGuessingGame.start_match') as mock_start_match:
            mock_start_match.side_effect = [520]
            game.start_game()
            last_logger_message = mock_logger.mock_calls[-1]
            expected_logger_message = call().logger.info(
                'Player stopped playing the game with 520 points\n')
            assert last_logger_message == expected_logger_message
        self.assertEqual(game.player_points, 520)

    @patch('MainGame.utilities.user_input', side_effect=[None])
    def test_start_game_with_error(self, mock_input):
        game = NumberGuessingGame("Player")
        with patch('MainGame.NumberGuessingGame.start_match') as mock_start_match:
            mock_start_match.side_effect = ['invalid']
            with self.assertRaises(Exception) as context:
                game.start_game()
            # Check the expected error message fails when re.match with return None value.
            expected_error_message = "The game cannot be started with an error: "\
                                     "expected string or bytes-like object"
            self.assertEqual(str(context.exception), expected_error_message)

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'yes', 'yes', 'no'])
    def test_start_match_with_player_stop(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.NumberGuessingGame.start_round') as mock_start_round:
            mock_start_round.side_effect = [(20, 1), (40, 2), (80, 3), (160, 4)]
            player_points = game.start_match(60)
            self.assertEqual(player_points, 195)

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'yes'])
    @patch('MainGame.Logger')
    def test_start_match_with_player_lose(self, mock_logger, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.NumberGuessingGame.start_round') as mock_start_round:
            mock_start_round.side_effect = [(20, 1), (40, 2), (0, 3)]
            player_points = game.start_match(35)
            last_logger_message = mock_logger.mock_calls[-1]
            expected_logger_message = call().logger.info('You lost this match\n')
            assert last_logger_message == expected_logger_message
        self.assertEqual(player_points, 10)

    @patch('MainGame.utilities.user_input', side_effect=['yes', 'yes'])
    def test_start_match_with_error(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.NumberGuessingGame.start_round') as mock_start_round:
            mock_start_round.side_effect = [(20, 1), ('invalid', 2)]
            with self.assertRaises(Exception) as context:
                game.start_match(100)
            # Check the expected error message fails when start_round returns an invalid value.
            expected_error_message = "The match cannot be started with an error: "\
                                     "'>' not supported between instances of 'str' and 'int'"
            self.assertEqual(str(context.exception), expected_error_message)

    @patch('MainGame.utilities.user_input', side_effect=['higher'])
    def test_start_round_with_player_win(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.The_Deck.get_cards') as mock_get_card:
            deck_instance = mock_get_card.return_value
            house_card, player_card = [('2', 2, 'Heart'), ('King', 13, 'Heart')]
            deck_instance.side_effect = [house_card, player_card]
            reward, number_round = game.start_round(80, 3)
            self.assertEqual((reward, number_round), (160, 4))

    @patch('MainGame.utilities.user_input', side_effect=['higher'])
    def test_start_round_with_player_lose(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.The_Deck.get_cards') as mock_get_card:
            deck_instance = mock_get_card.return_value
            house_card, player_card = [('7', 7, 'Diamond'), ('Ace', 1, 'Club')]
            deck_instance.side_effect = [house_card, player_card]
            reward, number_round = game.start_round(160, 4)
            self.assertEqual((reward, number_round), (0, 5))

    @patch('MainGame.utilities.user_input', side_effect=['lower'])
    def test_start_round_with_equal_results(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.The_Deck.get_cards') as mock_get_card:
            deck_instance = mock_get_card.return_value
            house_card, player_card = [('Jack', 11, 'Club'), ('Jack', 11, 'Heart')]
            deck_instance.side_effect = [house_card, player_card]
            reward, number_round = game.start_round(160, 5)
            self.assertEqual((reward, number_round), (160, 6))

    @patch('MainGame.utilities.user_input', side_effect=['lower'])
    def test_start_round_with_error(self, mock_input):
        game = NumberGuessingGame('Player')
        with patch('MainGame.The_Deck.get_cards') as mock_get_card:
            deck_instance = mock_get_card.return_value
            house_card, player_card = [('Queen', 12), ('4', 4, 'Diamond')]
            deck_instance.side_effect = [house_card, player_card]
            with self.assertRaises(Exception) as context:
                reward, number_round = game.start_round(0, 5)
            # Check the expected error message fails when printing the received card.
            expected_error_message = "The round cannot be started with an error:"\
                                     " tuple index out of range"
            self.assertEqual(str(context.exception), expected_error_message)


if __name__ == '__main':
    unittest.main()
