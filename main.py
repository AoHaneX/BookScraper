import requests
import json
import csv
import os
from bs4 import BeautifulSoup


def download_image(url_image, nom_fichier=None):
    """
    Télécharge une image depuis une URL et la sauvegarde dans le dossier 'IMG'.
    :param url_image: URL de l'image à télécharger
    :param nom_fichier: Nom du fichier local (optionnel). Si None, le nom sera extrait de l'URL.
    """
    # Créer le dossier IMG s'il n'existe pas
    dossier = "IMG"
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    # Déterminer le nom du fichier
    if not nom_fichier:
        nom_fichier = url_image.split('/')[-1]
    chemin_fichier = os.path.join(dossier, nom_fichier)
    # Télécharger l'image
    try:
        response = requests.get(url_image, stream=True)
        if response.status_code == 200:
            with open(chemin_fichier, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Téléchargé : {chemin_fichier}")
        else:
            print(f"Erreur lors du téléchargement de {url_image} : {response.status_code}")
    except Exception as e:
        print(f"Erreur : {e}")
        

def extraction_livres(url: str):
    request = requests.get(url)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        books_list = []  # Liste pour stocker les informations des livres
        # Trouver tous les articles de livres
        book_elements = soup.find_all('article', class_='product_pod')
        for book in book_elements:
            # Extraire le lien vers la page du livre
            link = book.h3.a['href']
            book_url = "http://books.toscrape.com/"
            if link.startswith('../../../'):
                link = 'catalogue/' + link.replace('../../../', '')
            book_link = book_url + link
            print("Le lien du livre est " + book_link)
            # Faire une requête vers la page du livre
            request = requests.get(book_link)
            if request.status_code == 200:
                soup = BeautifulSoup(request.content, 'html.parser')
                try:
                    product_page_url = book_link
                    universal_product_code = soup.find('table', class_='table').find('tr').find('td').text
                    title = soup.find('h1').text

                    # Vérifier si les éléments existent avant d'utiliser find_next
                    price_incl_tax_row = soup.find('th', string='Price (incl. tax)')
                    price_including_tax = price_incl_tax_row.find_next('td').text if price_incl_tax_row else None

                    price_excl_tax_row = soup.find('th', string='Price (excl. tax)')
                    price_excluding_tax = price_excl_tax_row.find_next('td').text if price_excl_tax_row else None

                    availability_row = soup.find('th', string='Availability')
                    availability = availability_row.find_next('td').text.strip() if availability_row else None

                    product_description = soup.find('meta', {'name': 'description'})['content'].strip() if soup.find('meta', {'name': 'description'}) else None
                    category = soup.find('ul', class_='breadcrumb').find_all('li')[-2].text.strip()
                    review_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else None
                    image_url = soup.find('div', id='product_gallery').find('img')['src']
                    image_url = "http://books.toscrape.com/" + image_url.replace('../../', '')
                    download_image(image_url)
                    # Ajouter les données dans la liste books_list
                    books_list.append({
                        'Code universel des produits / UPC': universal_product_code,
                        'Titre': title,
                        'Categorie': category,
                        'Note': review_rating,
                        'Description': product_description,
                        'Prix TTC': price_including_tax,
                        'Prix HTTC': price_excluding_tax,
                        'Nombre disponible': availability,
                        'Irl du produit': product_page_url,
                        "Url Image": image_url
                    })
                except AttributeError as e:
                    print(f"Erreur lors de l'extraction des données : {e}")
        else:
            print(f"Erreur lors de la requête vers la page du livre : {request.status_code}")
        return books_list
    else:
        print(f"Erreur lors de la requête : {request.status_code}")
        return None

def extraction_par_categorie(nom_categorie):
    base_url = "https://books.toscrape.com/catalogue/category/books/"
    url_page_1 = f"{base_url}{nom_categorie}/index.html"
    books_list = []
    page = 1
    while True:
        url = url_page_1.replace('index.html', f'page-{page}.html')
        print("L'url est "+ url)
        books_page = extraction_livres(url)
        print(books_page)
        if not books_page or len(books_page) == 0:
            break
        books_list.extend(books_page)
        page += 1
    return books_list

def extraction_all(liste_categories):
    """
    Extrait tous les livres de toutes les catégories passées en paramètre.
    :param liste_categories: Liste des noms de catégories (ex: ['travel_2', 'mystery_3', ...])
    :return: Liste de tous les livres de toutes les catégories (liste de dictionnaires)
    """
    all_books = []
    for categorie in liste_categories:
        print(f"Extraction de la catégorie : {categorie}")
        livres_categorie = extraction_par_categorie(categorie)
        if livres_categorie:
            all_books.extend(livres_categorie)
    return all_books



def extraction_one(nom_categorie):
    """
    Extrait tous les livres de toutes les catégories passées en paramètre.
    :param liste_categories: Liste des noms de catégories (ex: ['travel_2', 'mystery_3', ...])
    :return: Liste de tous les livres de toutes les catégories (liste de dictionnaires)
    """
    all_books = []
    print(f"Extraction de la catégorie : {nom_categorie}")
    livres_categorie = extraction_par_categorie(nom_categorie)
    if livres_categorie:
        all_books.extend(livres_categorie)
    return all_books


def get_categories():
    """
    Récupère les noms de toutes les catégories présentes dans le sous-menu "Books" de la page d'accueil.
    :return: Liste des noms de catégories au format utilisé dans les URLs (ex: 'sequential-art_5')
    """
    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur lors de la requête :", response.status_code)
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    categories = []
    # Le menu des catégories est dans <ul class="nav nav-list">, les sous-catégories dans les <li> enfants
    nav_list = soup.find('ul', class_='nav-list')
    if nav_list:
        for li in nav_list.find_all('li'):
            a = li.find('a')
            if a and 'category/books/' in a['href']:
                # On récupère le nom de la catégorie tel qu'il apparaît dans l'URL
                href = a['href']
                # Exemple : 'catalogue/category/books/sequential-art_5/index.html'
                # On extrait 'sequential-art_5'
                parts = href.split('/')
                if len(parts) > 4:
                    categories.append(parts[3])
    return categories


def affichage_livre(book):
    if not book:
        print("Aucune information sur le livre à afficher.")
        return
    print("Informations du livre :")
    print(f"  Irl du produit                : {book['Irl du produit']}")
    print(f"  Code universel des produits / UPC : {book['Code universel des produits / UPC']}")
    print(f"  Titre                        : {book['Titre']}")
    print(f"  Prix TTC                     : {book['Prix TTC']}")
    print(f"  Prix HTTC                    : {book['Prix HTTC']}")
    print(f"  Nombre disponible            : {book['Nombre disponible']}")
    print(f"  Description                  : {book['Description']}")
    print(f"  Catégorie                    : {book['Categorie']}")
    print(f"  Note                         : {book['Note']}")
    print(f"  URL de l'image         : {book['Url Image']}")
    print("-" * 40)
    
def affichage_livres(liste_livres):
    taille_livres = len(liste_livres)
    for livre in range(taille_livres) :
        affichage_livre(liste_livres[livre])
#TRANSFORM

#def create

#LOAD
def creer_csv(nom_fichier, liste_livres):
    """
    Crée un fichier CSV et écrit les données dedans.
    :param nom_fichier: Nom du fichier CSV à créer (ex: 'livres.csv')
    :param en_tete: Liste des noms de colonnes (ex: ['titre', 'prix'])
    :param donnees: Liste de dictionnaires contenant les données à écrire
    """
    
    en_tete = ['Code universel des produits / UPC',
               'Titre',
               'Categorie',
               'Note',
               'Description',
               'Prix TTC',
               'Prix HTTC',
               'Nombre disponible',
               'Irl du produit',
               'Url Image']
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=en_tete,delimiter=';')
        writer.writeheader()
        writer.writerows(liste_livres)




def main():
    #Création du fichier CSV toute catégories
    liste_livres=extraction_all(get_categories())
    
    #Création du fichier CSV une catogorie
    categorie=""
    if categorie != "":
        liste_livres=extraction_one(categorie)
    creer_csv("livres.csv", liste_livres)
 
    
    

if __name__ == "__main__":
    main()

