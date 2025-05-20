import requests
import json
import csv
from bs4 import BeautifulSoup


"""1)Préparer le github&Premier commit
Partie 2!
)Choisir une page dont extraire les données
2)Ecrire une fonction permettant d'extraire les données de la pages et qui renvoi une liste de dictionnaire
3)Ecrire une fonction permettant d'afficher cette liste



4)Faireune fonction avec une boucle pour afficher le contenu du fichier CSV
"""

#EXTRACT

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
            book_link = book_url + book.h3.a['href']

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

                    # Ajouter les données dans la liste principale
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
        return books_list
    else:
        print(f"Erreur lors de la requête : {request.status_code}")
        return None


def affichage_livre(book):
    """
    Affiche toutes les informations d'un livre.
    :param book: Un dictionnaire contenant les informations d'un livre.
    """
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
    liste_livres=extraction_livres("http://books.toscrape.com/")
    affichage_livres(liste_livres)
    #print(liste_livres)
    creer_csv("livres.csv", liste_livres)
 
    
    

if __name__ == "__main__":
    main()

