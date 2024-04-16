import pytest
import unicodedata

#######
# Function we would like to test should be defined in package code, not here.
########
def drop_diacritics(text: str) -> str:
    """
    Strip accents from input String.
    
    :param text: The input string.
    :returns: The processed string.
    """
    if not isinstance(text, str):
        raise TypeError(f'Input text should be a string, not %s', type(text))
    
    # Return the normal form for the Unicode string
    # 'NFKD' stands for the normal form KD  
    text = unicodedata.normalize('NFKD',text)
    output = ''
    
    for char in text:
        if not unicodedata.combining(char):
            output += char
            
    return output
#### 


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
    
@pytest.mark.parametrize(
    'original,output',
    [
        ('řeřicha', 'rericha'),
        ('čeština', 'cestina')
    ]
) 
def test_drop_diacritics(original:str, output:str) -> None:
    assert drop_diacritics(original) == output
    