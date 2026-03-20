import logging
from .validator import EmailValidator, EmailValidationError
from .email_message import TextEmail
from .connector import  SMTPConnector, SMTPConnectionError


logging.basicConfig(
    filename='email_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailService:

    def __init__(self):
        self.validator = EmailValidator()
        self.logger    = logging.getLogger(__name__)

    def send(self, message: TextEmail) -> bool:
        try:
            self.validator.validate(message)
            with SMTPConnector() as conn:
                conn.send(message)
            self.logger.info(f"Email envoyé avec succès à {message.to}")
            return True

        except EmailValidationError:
            self.logger.error(f"Validation échouée : {message.to}")
            return False

        except SMTPConnectionError:
            self.logger.error(f"Connexion échouée : {message.to}")
            return False

        except Exception as e:
            self.logger.error(f"Erreur inattendue : {e}")
            return False

    def send_bulk(self, objList: list) -> dict:
        resultat = {"succes": 0, "failed": 0}
        with SMTPConnector() as conn:
            for elt in objList:
                try:
                    self.validator.validate(elt)
                    conn.send(elt)
                    resultat["succes"] += 1
                    self.logger.info(f"Email envoyé avec succès à {elt.to}")

                except EmailValidationError:
                    resultat["failed"] += 1
                    self.logger.error(f"Echec validation : {elt.to}")
                    continue

                except SMTPConnectionError:
                    resultat["failed"] += 1
                    self.logger.error(f"Echec connexion : {elt.to}")
                    continue

                except Exception as e:
                    resultat["failed"] += 1
                    self.logger.error(f"Erreur inattendue : {e}")
                    continue

        return resultat