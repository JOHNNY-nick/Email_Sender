
import re
from .email_message import TextEmail

class EmailValidationError(Exception): 
    pass  
    

def is_valid_email(PotentialEmailAdress) :
        pattern = r'^[a-zA-Z0-9_.-]+@[a-z]{2,}.[a-z]{2,}'
        return bool(re.match(pattern,PotentialEmailAdress))


class EmailValidator() :
    """Cette classe sert à vérifier la validiter des emails"""

    def validate(self,TextEmailobject : TextEmail) :
        if not is_valid_email(TextEmailobject.to) :
            raise EmailValidationError("Adresse destinataire invalide : jean@")

        if len(TextEmailobject.body.strip()) == 0 :
            raise EmailValidationError("Le corps de l'email ne peut pas être vide")

        if len(TextEmailobject.cc) != 0 :
            for elt in TextEmailobject.cc :
                if  not is_valid_email(elt) :
                    raise EmailValidationError(f"Adresse {elt} n'est pas valide ")
        
        else :
            return True