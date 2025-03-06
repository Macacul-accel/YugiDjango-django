# Yugi-Django

## Nouvelle version
V2 de l'appli:

https://github.com/Macacul-accel/Dashboard.git

Dans cette nouvelle version, passage vers DRF.
Optimisation des queries (defer pour les champs 'effect' et 'image') pour une réponse plus rapide.
Simplification de l'authentification pour ne pas embêter l'utilisateur à confirmer son adresse mail.

## Changements apportés
1. **Passage vers DRF**
Transformation en API, ajout des serializers.

2. **Optimisation des query**
Indexation pour une réponse plus rapide de la base de données.
Ajout de defer au query de CardList pour un rendu plus rapide. Les champs 'effect' et 'image' chargeront au fur et à mesur sans impacter la performance de l'API.

3. **Refactorisation**
Réécriture du FilterSet pour une meilleure lisibilité. 
Simplification des views, plus besoin de formater manuellement les données en JSON.
Des class plus claires et un code plus maintenable.

4. **Simplification de l'authentification**
Plus besoin de confirmer son mail pour devenir utilisateur et construire ses decks.
Une simple inscription avec un nom d'utilisateur et un mot de passe.

5. **Complexification du mot de passe**
Ajout de validators qui forcent l'utilisateur à avoir un mot de passe plus robuste (une lettre minuscule, une lettre majuscule, un chiffre et un charactère spécial, avec une longueur de 8 charactères minimum).

## Profiter et explorer !