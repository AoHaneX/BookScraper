README - BookScraper

========================================
Description
----------------------------------------
BookScraper est un programme Python permettant de scraper le site https://books.toscrape.com/ afin de récupérer les informations de tous les livres (ou d'une catégorie précise) et de les enregistrer dans un ou plusieurs fichiers CSV. 
Les images des couvertures sont également téléchargées dans un dossier local "IMG".
Les informations récupérer sont , pour chaque livre:
    - Le code universel / UPC
    - Le titre
    - La catégorie
    - La note
    - La description
    - Le prix TTC
    - Le prix HTTC
    - Le nombre d'exemplaire disponible à l'instant T
    - L'URL de la page du produit
    - L'URL de l'image

========================================
Fonctionnalités principales
----------------------------------------
- Extraction des informations de tout les livres d'une catégorie précises 
- Extraction des informations de tout les livres du site, triées par catégorie dans plusieurs fichiers CSV.
- Génération d'un dossier "IMG" et téléchargement automatique des images de couverture dans ce dossier.
- Génération d'un fichier CSV avec toutes les informations collectées.
- Affichage ,  dans la console, des informations des livres.
========================================
Prérequis
----------------------------------------
- Python 3.x
- Les modules suivants doivent être installés :
    - requests
    - beautifulsoup4

Pour installer les dépendances :
    pip install requests beautifulsoup4

========================================
Utilisation
----------------------------------------
1. Placez-vous dans le dossier du projet.
2. Lancez le script principal :
    python main.py

Le script va :
- Scraper toutes les catégories et tous les livres du site.
- Télécharger les images dans un dossier "IMG".
- Générer un fichier .csv pour chaque catégorie avec toutes les informations des livres appartenant à cette dite catégorie.

Pour ne scraper qu'une seule catégorie, commentez avec les lignes  227 à 235 avec """ au début et à la fin, puis modifiez la variable `categorie` dans la fonction `main()` avec le nom de la catégorie voulue.

========================================
Structure des fichiers/dossiers générés
----------------------------------------
- livres_(Nom de la catégorie)_(Numéro de la catégorie).csv : Fichier CSV contenant toutes les informations des livre d'une catégorie.
- IMG/ : Dossier contenant toutes les images de couverture téléchargées.

========================================
Auteurs:
Adrian STALIN--RENAULT
----------------------------------------
