import unittest
from unittest.mock import patch
from utilities import validate_input
from inputimeout import TimeoutOccurred


class TestValidateInput(unittest.TestCase):

    @patch('utilities.inputimeout', side_effect=['yes'])
    def test_valid_input(self, mock_inputimeout):
        pattern = r'yes|no'
        user_input = validate_input("Are you ready to start?", pattern)
        self.assertEqual(user_input, 'yes')

    @patch('utilities.inputimeout', side_effect=["invalid1", "invalid2"])
    def test_invalid_input_list(self, mock_input):
        pattern = r'yes|no'
        result = validate_input("Enter a valid input: ", pattern, max_attempts=2)
        self.assertEqual(result, "invalid2")

    @patch('utilities.inputimeout', side_effect=TimeoutOccurred)
    def test_timeout(self, mock_input):
        pattern = r'yes|no'
        result = validate_input("Enter a valid input: ", pattern)
        self.assertEqual(result, "")

    @patch('utilities.inputimeout', side_effect=Exception("An error occurred"))
    def test_validate_input_with_errorr(self, mock_input):
        pattern = r'yes|no'
        with self.assertRaises(Exception) as context:
            validate_input("Enter a valid input:", pattern)
        expected_message = 'Cannot validate input due to error: An error occurred'
        self.assertEqual(str(context.exception), expected_message)
