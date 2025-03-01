# Yugi-Django

## Description
Étant un passionné du jeu de cartes Yu-Gi-Oh!, je voulais avoir à ma disposition toutes les cartes sorties depuis le lancement du jeu, avec des filtres personnalisés.
Pouvoir partager avec la communauté de joueurs les decks crées par chacun.

## Outils utilisés
-   API: https://ygoprodeck.com/api-guide/
-   Django: v5.1.6
-   Vue.JS: v3.5.13
-   Bootstrap5

## 

## Installation
1. **Cloner le repo**
    ```bash
    git clone https://github.com/Macacul-accel/Dashboard.git
    cd Dashboard/backend
    ```

2. **Activer l'environnement virtuel (Optionnel)**
    ```bash
    python3.12 -m venv .env
    source .env/bin/activate  # Sur Windows: `.env\Scripts\activate`
    ```

3. **Installer les packages nécessaires**
    ```bash
    pip install -r requirements.txt
    ```

4. **Activer la base de données**
    ```bash
    python manage.py migrate
    ```

5. **Récupérer les données de l'API (!Les images occupent beaucoup d'espaces!)**
    ```bash
    python manage.py fecth_cards # Récupére les données de toutes les cartes qui ne sont pas dans la bdd
    ```
    Lorsque la récupération des données est terminée
    ```bash
    python manage.py fetch_images # Modifiez le fichier et choisissez l'option 2 pour éviter d'occuper trop d'espace
    ```

6. **Lancer le serveur**
    ```bash
    python manage.py runserver
    ```

7. **Accès au site**
    Ouvrez votre navigateur et rentrez dans la barre de recherche: `http://127.0.0.1:8000/`.