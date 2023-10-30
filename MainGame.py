import re
import utilities
from logger import Logger
from the_deck import the_deck


class NumberGuessingGame():
    WIN_THRESHOLD = 1000
    LOSE_THRESHOLD = 30
    COST_POINT = 25

    def __init__(self, player_name):
        self.player_points = 60
        self.logger = Logger().logger
        self.player_name = player_name

    def start_game(self):
        """
        Description:
            This function will start the Number Guessing Game.
        Parameters:
            None
        Returns:
            None: This function only executes the code and does not return any value.
        Raise:
           Exception: If the game cannot be started with the corresponding error.
        """
        try:
            self.logger.info(f"Welcome {self.player_name} to Number Guessing Game!, You are having {self.player_points} points\n")
            while self.LOSE_THRESHOLD < self.player_points <= self.WIN_THRESHOLD:
                user_input = utilities.validate_input("Are you ready to start a new match? (Yes/No)", r'\b(yes|y|no|n)\b')
                if re.match(r'\b(yes|y)\b', user_input):
                    self.player_points = self.start_match(self.player_points)
                else:
                    self.logger.info("Quitting the game\n")
                    break

            self.logger.info("Your current point is: {}\n".format(self.player_points))
            if self.player_points >= self.WIN_THRESHOLD:
                self.logger.info("Congratulations! You WONNNNN this game\n")
            elif self.player_points <= self.LOSE_THRESHOLD:
                self.logger.info("You lose this game\n")
            else:
                self.logger.info("Player stopped playing the game with {} points\n".format(self.player_points))
        except Exception as exc:
            raise Exception("The game cannot be started with an error: {}".format(exc))

    @utilities.log_duration('Match')
    def start_match(self, player_points: int):
        """
        Description:
            This function will start a new match in the Number Guessing Game.
        Parameters:
            player_points(int): the points of player.
        Returns:
            player_points(int): This function will return the player_points after the match completed.
        Raise:
            Exception: If the match cannot be started the game with the corresponding error.
        """
        try:
            self.logger.info(f'The cost points for a new match: {self.COST_POINT}\n')
            player_points -= self.COST_POINT
            reward_points = 20
            round_number = 1
            while reward_points > 0:
                user_input = utilities.validate_input(f'Current player points: {player_points} - Current reward: {reward_points}. '
                                                      'Do you want to continue playing? (Yes/No)\n', r'\b(yes|y|no|n)\b')
                if re.match(r'\b(yes|y)\b', user_input):
                    reward_points, round_number = self.start_round(reward_points, round_number)
                else:
                    return player_points + reward_points
            self.logger.info("You lost this match\n")
            return player_points + reward_points
        except Exception as exc:
            raise Exception("The match cannot be started with an error: {}".format(exc))

    @utilities.log_duration('Round')
    def start_round(self, reward_points: int, round_number: int):
        """
        Description:
            This function will start a new round in the match.
        Parameters:
            reward_points(int): the reward points of Player.
            round_number(int): the current round number.
        Returns:
            reward_points(int): This function will return the reward points after the round completed.
        Raise:
            Exception: If the round cannot be started the game with the corresponding error.
        """
        try:
            self.logger.info(
                "***** Starting round {} with your current reward: {} *****\n".format(round_number, reward_points))
            deck = the_deck().get_cards()
            house_card = deck("House")
            self.logger.info("House's card is {}\n".format(house_card))

            user_input = utilities.validate_input(
                "Please guess your card is Greater/Less than House's card\n", r"\b(greater|g|less|l)\b")
            player_card = deck("Player")
            greater_card = the_deck().compare_cards(house_card, player_card)

            self.logger.info("Your card is {}\n".format(player_card))
            if re.match(r"\b(greater|g)\b", user_input) and player_card is greater_card or \
                re.match(r"\b(less|l)\b", user_input) and house_card is greater_card:
                self.logger.info("Player won\n")
                reward_points *= 2
            else:
                self.logger.info("Player loses\n")
                reward_points = 0
            self.logger.info("Your current reward point after this round {} is: {}\n".format(round_number, reward_points))
            round_number += 1
            return reward_points, round_number
        except Exception as exc:
            raise Exception("The round cannot be started with an error: {}".format(exc))


if __name__ == '__main__':
    Player = NumberGuessingGame(player_name="Loc Huynh").start_game()
