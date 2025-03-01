import re

from django.core.exceptions import ValidationError

"""
More custom validators so the password contain at least 1 digit, 1 upper, 1 lower and one special character
"""

class NumberValidator:
    def validate(self, password, user=None):
        if not re.search('\d', password):
            raise ValidationError(self.get_error_message(), code='password_no_digit')
        
    def get_error_message(self):
        return "Votre mot de passe ne contient aucun chiffre"
        
    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins un chiffre"
    
class UpperCaseValidator:
    def validate(self, password, user=None):
        if not re.search('[A-Z]', password):
            raise ValidationError(self.get_error_message(), code='password_no_upper')
        
    def get_error_message(self):
        return "Votre mot de passe ne contient aucune lettre majuscule"
        
    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins une lettre majuscule"
    
class LowerCaseValidator:
    def validate(self, password, user=None):
        if not re.search('[a-z]', password):
            raise ValidationError(self.get_error_message(), code='password_no_lower')
        
    def get_error_message(self):
        return "Votre mot de passe ne contient aucune lettre minuscule"
        
    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins une lettre minuscule"
    
class SpecialCaseValidator:
    def validate(self, password, user=None):
        if not re.search('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(self.get_error_message(), code='password_no_special')
        
    def get_error_message(self):
        return "Votre mot de passe ne contient aucun charactère spéciale"
        
    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins un charactère spéciale"