import requests
from typing import List, Dict, Union
import time


def get_meals(letters: Union[str,List[str]], timeout: int =1 , sleep: int = 1) -> Dict:

    """
    Given a single letter or a list of letters, requests meals starting with each letter
    and returns a dictionary with the raw response data.

    Args:
        letters (Union[str, List[str]]): A single letter or a list of letters to request meals for.
        timeout (int, optional): The number of seconds to wait for a response before timing out.
            Defaults to 1 second.
        sleep (int, optional): The number of seconds to wait between requests. Defaults to 1 second.

    Returns:
        Dict: A dictionary with the raw response data for each letter requested.
    """

    meals_raw = {}
    for l in letters:
        meals_raw[l] = request_meals_starting_w_letter(l, timeout = timeout)
        time.sleep(sleep)
    return meals_raw

def process_meals(meals_raw: Dict) -> Dict:
    """
    Process a dictionary of meals returned by `get_meals`, converting the attribute names of each
    meal from camel case to snake case, and returning the processed dictionary.

    Args:
        meals_raw: A dictionary where each key is a letter, and each value is a list of meals
            starting with that letter. Each meal is represented as a dictionary, with attribute
            names in camel case.

    Returns:
        A new dictionary with the same structure as `meals_raw`, but with the attribute names cleaned
        of type-hints.
    """
    meals_processed = {}

    for letter, meals in meals_raw.items():
        meals_processed[letter] = []
        for meal in meals:
            meals_processed[letter].append(clear_meal_attribute_names(meal))

    return meals_processed

def request_meals_starting_w_letter(letter: str, timeout: int = 1) -> List:
    """
    Retrieves a list of meals that start with the specified letter from the meal database API.

    Args:
        letter (str): The letter to search for in the meal names.
        timeout (int, optional): The timeout for the API request in seconds. Defaults to 1.

    Returns:
        List: A list of meals that start with the specified letter.

    Raises:
        requests.exceptions.HTTPError: If the API request returns an HTTP error status code.
        requests.exceptions.RequestException: If the API request encounters an error.
    """
    try:
        r = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?f={letter}', timeout = timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error")
        print(errh.args[0])
    except requests.exceptions.RequestException as errex:
        print("Exception request")

    return r.json()['meals']

def clear_meal_attribute_names(meal: Dict) -> Dict:
    """
        Given a dictionary representing a meal with attribute names in camel case,
        returns a new dictionary with attribute names converted to lowercase with underscores,
        until the first capital letter is encountered.

        Args:
            meal (Dict): A dictionary representing a meal with attribute names in camel case.

        Returns:
            Dict: A new dictionary with attribute names converted to lowercase with underscores,
            until the first capital letter is encountered.
        """
    return {remove_prefix_until_capital_letter(k):v for k,v in meal.items()}

def remove_prefix_until_capital_letter(s: str) -> str:
    """
    Removes all characters from the start of the string `s` until the first capital letter is found,
    while keeping the capital letter. If no capital letter is found, the original string is returned.

    Args:
        s (str): The input string.

    Returns:
        str: The resulting string with all characters removed from the start until the first capital letter.

    Examples:
        >>> s = "helloWorld"
        >>> remove_prefix_until_capital_letter(s)
        'World'

        >>> s = "alllowercase"
        >>> remove_prefix_until_capital_letter(s)
        'alllowercase'

        >>> s = "ALLUPPERCASE"
        >>> remove_prefix_until_capital_letter(s)
        'ALLUPPERCASE'
    """
    for i, char in enumerate(s):
        if char.isupper():
            return s[i:]
    return s
