import re
import utilities
from logger import Logger
from the_deck import The_Deck


class NumberGuessingGame():
    WIN_THRESHOLD = 1000
    LOSE_THRESHOLD = 30
    COST_POINT = 25

    def __init__(self, player_name):
        self.player_name = player_name
        self.player_points = 60
        self.reward_points = 0
        self.deck = None
        self.logger = Logger().logger

    def start_game(self) -> None:
        """
        Description:
            This function will start the Number Guessing Game.
        Parameters:
            None
        Returns:
            None: Function only executes the code and does not return any value
        Raise:
           Exception: If the game cannot be started with corresponding error.
        """
        try:
            self.logger.info(
                f"Welcome {self.player_name} to Number Guessing Game!"
                f" You are having {self.player_points} points\n")

            while self.LOSE_THRESHOLD < self.player_points <= self.WIN_THRESHOLD:
                user_input = utilities.user_input(
                    "Are you ready to start a new match? (Yes/No)",
                    r'\b(yes|y|no|n)\b')
                if re.match(r'\b(yes|y)\b', user_input):
                    # Refresh the deck after every match.
                    self.deck = The_Deck().create_deck
                    self.player_points = self.start_match(self.player_points)
                else:
                    self.logger.info("Quitting the game\n")
                    break

            self.logger.info(f"Your current point is: {self.player_points}\n")
            if self.player_points >= self.WIN_THRESHOLD:
                self.logger.info("Congratulations! You won this game\n")
            elif self.player_points <= self.LOSE_THRESHOLD:
                self.logger.info("Game Over. You lost this game\n")
            else:
                self.logger.info(
                    f"Player stopped playing with {self.player_points} points")
        except Exception as exc:
            raise Exception(f"The game cannot be started with an error: {exc}")

    @utilities.log_duration('Match')
    def start_match(self, player_points: int) -> int:
        """
        Description:
            This function will start a new match in the Number Guessing Game.
        Parameters:
            player_points(int): the points of player.
        Returns:
            player_points(int): The player points after the match completed.
        Raise:
            Exception: If the match cannot be started with corresponding error.
        """
        try:
            self.logger.info(
                f'The cost points for a new match: {self.COST_POINT}\n')
            player_points -= self.COST_POINT
            round_number = 1
            reward_points, round_number = self.start_round(
                self.reward_points, round_number)

            while reward_points > 0:
                user_input = utilities.user_input(
                    f'Player points: {player_points} - Reward: {reward_points}'
                    '. Do you want to continue playing? (Yes/No)\n',
                    r'\b(yes|y|no|n)\b')

                if re.match(r'\b(yes|y)\b', user_input):
                    reward_points, round_number = self.start_round(
                        reward_points, round_number)
                else:
                    return player_points + reward_points
            self.logger.info("You lost this match\n")
            return player_points + reward_points
        except Exception as exc:
            raise Exception(
                f"The match cannot be started with an error: {exc}")

    @utilities.log_duration('Round')
    def start_round(self, reward_points: int, round_number: int) -> int:
        """
        Description:
            This function will start a new round in the match.
        Parameters:
            reward_points(int): the reward points of Player.
            round_number(int): the current round number.
        Returns:
            reward_points(int): The reward points after the round completed.
        Raise:
            Exception: If the round cannot be started with corresponding error.
        """
        try:
            self.logger.info(f"*** Starting round {round_number} with"
                             f" your current reward: {reward_points} ***\n")

            get_card = The_Deck().get_cards(self.deck)
            house_card = get_card()
            self.logger.info(
                f"House's card is '{house_card[0]} {house_card[2]}'\n")

            player_guess = utilities.user_input(
                "Please guess your card is higher/lower than House's card\n",
                r"\b(higher|lower)\b")
            player_card = get_card()

            result = The_Deck().compare_cards(house_card, player_card)
            self.logger.info(
                f"Your card is '{player_card[0]} {player_card[2]}'\n")

            if re.search(fr'\b({player_guess})\b', result):
                self.logger.info("Player won\n")
                reward_points = reward_points * 2 if round_number > 1 else 20
            elif re.match(r'\b(equal)\b', result):
                self.logger.info(
                    "Your card and House'card are equal in this round\n")
            else:
                self.logger.info("Player loses\n")
                reward_points = 0

            self.logger.info("Your current reward point after this "
                             f"round {round_number} is: {reward_points}\n")
            round_number += 1
            return reward_points, round_number
        except Exception as exc:
            raise Exception(
                f"The round cannot be started with an error: {exc}")


if __name__ == '__main__':
    Player = NumberGuessingGame(player_name="Player").start_game()
