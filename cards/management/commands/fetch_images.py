import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from cards.models import Card
import re

"""
Commande permettant de récupérer les images via l'api 'ygoprodeck'.
En cas d'image manquante, dû à une erreur quelconque, la commande peut détecter les cartes ayant l'image par défaut.
Ainsi récupérer les images seulement pour ces cartes et éviter le traitement inutiles des autres cartes.
"""
class Command(BaseCommand):
        help = "Insertion des images pour les cartes"

        def handle(self, *args, **kwargs):
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            image_data = response.json().get('data')

            missing_image_cards = Card.objects.filter(image='card_images/default.jpg')
            card_data_dict = {card_data['name']: card_data for card_data in image_data}
            
            def download_and_save_img(self, missing_list, field_name, url_key):
                for card in missing_list:
                    card_data = card_data_dict.get(card.name)
                    try:
                        if card_data.get('card_images'):
                            image_url = card_data['card_images'][0][url_key]
                            self.stdout.write(f"Traitement de l'image pour la carte {card.name}")
                            if image_url:
                                image_response = requests.get(image_url, timeout=120, stream=True)
                                image_response.raise_for_status()

                                image_name = re.sub(r'[^a-zA-Z0-9_-]', '', card.name) + '.jpg'
                                image_content = ContentFile(image_response.content)
                                getattr(card, field_name).save(image_name, image_content, save=True)
                                self.stdout.write(f"✅ {field_name.capitalize()} pour la carte {card.name} a bien été enregistré")
                            else:
                                self.stderr.write(f"❌ Il n'y a pas d'url disponible pour {card.name}")
                        else:
                            self.stderr.write(f"❌ Il n'y pas de {field_name} pour {card.name}")
                    except Exception as error:
                        self.stderr.write(f"❌ Erreur dans le téléchargement {field_name} de la carte {card.name}: {error}")
                    
                self.stdout.write("✅ Les images ont bien été enregistrées")

            #Option 1 (par défaut):
            download_and_save_img(self, missing_image_cards, 'image', 'image_url')

            #Option 2:
            #download_and_save_img(self, missing_image_cards, 'image', 'image_url_small')

