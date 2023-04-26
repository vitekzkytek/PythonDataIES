import pytest

from src.processing import remove_prefix_until_capital_letter

def test_lowercase_and_uppercase_letters():
    # Test case 1: string with lowercase and uppercase letters
    s = "helloWorld"
    assert remove_prefix_until_capital_letter(s) == "World"


def test_lowercase_letters_only():
    # Test case 2: string with only lowercase letters
    s = "alllowercase"
    assert remove_prefix_until_capital_letter(s) == "alllowercase"


def test_uppercase_letters_only():
    # Test case 3: string with only uppercase letters
    s = "ALLUPPERCASE"
    assert remove_prefix_until_capital_letter(s) == "ALLUPPERCASE"


def test_no_capital_letters():
    # Test case 4: string with no capital letters
    s = "n0c@p!t@ll3tt3rs"
    assert remove_prefix_until_capital_letter(s) == "n0c@p!t@ll3tt3rs"


def test_empty_string():
    # Test case 5: empty string
    s = ""
    assert remove_prefix_until_capital_letter(s) == ""


def test_one_capital_letter():
    # Test case 6: string with only one capital letter
    s = "C"
    assert remove_prefix_until_capital_letter(s) == "C"


def test_special_characters():
    # Test case 7: string with special characters
    s = "!@#$%HelloWorld"
    assert remove_prefix_until_capital_letter(s) == "HelloWorld"


def test_numbers():
    # Test case 8: string with numbers
    s = "123HelloWorld"
    assert remove_prefix_until_capital_letter(s) == "HelloWorld"
