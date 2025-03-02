import re

from django.core.exceptions import ValidationError

"""
More custom validators so the password contain at least 1 digit, 1 upper, 1 lower and one special character
"""
    
class BasePaswordValidator:
    error_message = ""
    regex_pattern = ""

    def validate(self, password, user=None):
        if not re.search(self.regex_pattern, password):
            raise ValidationError(self.error_message, code=self.error_code)
        
    def get_help_text(self):
        return self.error_message
    
class NumberValidator(BasePaswordValidator):
    error_message = "Votre mot de passe ne contient aucun chiffre"
    error_code = 400
    regex_pattern = r'\d'

class UpperCaseValidator(BasePaswordValidator):
    error_message = "Votre mot de passe ne contient aucune lettre majuscule"
    error_code = 400
    regex_pattern = r'[A-Z]'

class LowerCaseValidator(BasePaswordValidator):
    error_message = "Votre mot de passe ne contient aucune lettre minuscule"
    error_code = 400
    regex_pattern = r'[a-z]'

class SpecialCaseValidator(BasePaswordValidator):
    error_message = "Votre mot de passe ne contient aucun charactère spéciale"
    error_code = 400
    regex_pattern = r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]'