import pytest

@pytest.fixture
def smtp():
    """Initialize and return SMTP client session object"""
    import smtplib
    return smtplib.SMTP("smtp.gmail.com")

def test_ehlo(smtp):
    """Test response from sending Extended Helo (EHLO) is 250."""
    response, msg = smtp.ehlo()
    assert response == 250
    # assert 0 