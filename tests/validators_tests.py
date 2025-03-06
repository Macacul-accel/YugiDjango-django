import pytest
from rest_framework.test import APIClient


@pytest.mark.parametrize(
        'username, email, password, password2, expected_error',
        [
            ('user1', 'test@user.com', 'Validator@', 'Validator@', 'Votre mot de passe ne contient aucun chiffre'),
            ('user2', 'test@user.com', 'validator1@', 'validator1@', 'Votre mot de passe ne contient aucune lettre majuscule'),
            ('user4', 'test@user.com', 'VALIDATOR1@', 'VALIDATOR1@', 'Votre mot de passe ne contient aucune lettre minuscule'),
            ('user3', 'test@user.com', 'ValidatorR1', 'ValidatorR1', 'Votre mot de passe ne contient aucun charactère spéciale'),
            ('user5', 'test@user.com', 'ValidatorR1@', 'validator', 'Les mots de passe ne sont pas similaires'),
        ]
)
@pytest.mark.django_db
def test_custom_password_validator(username, email, password, password2, expected_error):
    client = APIClient()
    url = '/api/v2/register/'
    data = {
        'username': username,
        'email': email,
        'password': password,
        'password2': password2,
    }
    response = client.post(url, data)

    assert response.status_code == 400

    error_messages = []

    if "password" in response.data:
        error_messages.extend(response.data["password"])

    assert expected_error in error_messages