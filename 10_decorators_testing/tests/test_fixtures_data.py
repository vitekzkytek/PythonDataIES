import pytest 

@pytest.fixture
def data_names():
    import pandas as pd
    df = pd.read_csv('tests/data/test_data_names.csv')
    return df

def test_addressing(data_names):
    df = data_names
    titles = df['Title']
    surnames = df['Surname']
    expected = df['Addressing']
    assert (titles + ' ' + expected == surnames).all()