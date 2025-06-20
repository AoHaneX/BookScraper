README - BookScraper

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
- Extraction des informations de tout les livres du site, triées par catégorie
- Génération d'un dossier "IMG" et téléchargement automatique des images de couverture dans ce dossier.
- Génération de fichiers CSV pour chaque catégories contenant toutes les informations collectées .
- Affichage possible,  dans la console, des informations des livres colléctés.
=======================================
Prérequis:
- Python 3.x
========================================
Installation de l'environnement virtuel
----------------------------------------
Voici les étapes à suivre pour créer un environnement virtuel et lancer ce programme :

1)Ouvrir le terminal
2)Lancer un invite de commandes

3)Se Placer dans le dossier du projet avec la commande:
cd "chemin du_du_repertoire"

4)Créer l’environnement virtuel en tapant la commande suivante:
python -m venv venv

Cela va créer un dossier venv contenant l’environnement virtuel.

5)Active l’environnement virtuel avec la commande:
.venv/bin/activate

6)Installer les dépendances du projet avec la commande:
pip install -r requirements.txt
Cela va installer automatiquement les modules nécessaires (requests et beautifulsoup4).

6)Executer le programme avec votre IDE ou avec la commande:
python main.py
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
