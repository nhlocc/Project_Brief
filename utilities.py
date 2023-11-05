import re
import time
from logger import Logger
from inputimeout import inputimeout, TimeoutOccurred


def user_input(message: str, pattern: str, max_attempts: int = 5):
    """
    Description:
        This function is designed to collect and validate user input with
        a specified pattern.
        It allows the user a limited number of attempts to provide valid input.
    Parameters:
        message(str): The message to display to the user, instructing what
                      input is expected.
        pattern(str): A regular expression pattern used to validate the
                      user's input.
        max_attempts(int): The maximum number of attempts allowed for valid
                           input. (Default is 5)
    Returns:
        user_input(str): The valid input of user within the allowed attempts.
    Raise:
        Exception: If an error occurs during input collection.
    """
    try:
        user_input = ''
        attempt = 0
        logger = Logger().logger
        while attempt < max_attempts:
            try:
                logger.info(f"{message}\n")
                user_input = inputimeout('', timeout=60).lower()
            except TimeoutOccurred:
                logger.error("Exceeded input timeout(60s). Exiting...\n")
                return user_input
            logger.info(f"User input: {user_input}\n")
            if re.match(pattern, user_input):
                return user_input
            else:
                attempt += 1
                logger.error("Input invalid..Please input again\n")
        else:
            logger.error(
                f"Exceeded maximum attempts({max_attempts} times).Exiting..\n")
        return user_input
    except Exception as exc:
        raise Exception(
            f"An error occurred during input collection and validation: {exc}")


def log_duration(context: str):
    """
    Description:
        This decorator function records the execution duration for the
        wrapper function.
        It records the start time, end time and duration of the function's
        execution.
    Parameters:
        context(str): The description of the context in which the function
                      is executed.
    Returns:
        result: the result of the wrapped function's execution.
    Raise:
        Exception: If this function cannot be record log duration with
                   the corresponding error.
    """
    try:
        logger = Logger().logger

        def decorator(func):
            def wrapper(*args):
                start_time = time.time()
                result = func(*args)
                end_time = time.time()
                duration = end_time - start_time
                logger.info(f"{context} duration: {duration:.2f} seconds\n")
                return result
            return wrapper
        return decorator
    except Exception as exc:
        raise Exception(
            "Cannot record log duration due to error: {}".format(exc))
