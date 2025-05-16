import requests
import json
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
                        'product_page_url': product_page_url,
                        'universal_product_code': universal_product_code,
                        'title': title,
                        'price_including_tax': price_including_tax,
                        'price_excluding_tax': price_excluding_tax,
                        'number_available': availability,
                        'product_description': product_description,
                        'category': category,
                        'review_rating': review_rating,
                        'image_url': image_url
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
    print(f"  URL de la page produit : {book['product_page_url']}")
    print(f"  Code produit universel (UPC) : {book['universal_product_code']}")
    print(f"  Titre                  : {book['title']}")
    print(f"  Prix TTC               : {book['price_including_tax']}")
    print(f"  Prix HT                : {book['price_excluding_tax']}")
    print(f"  Disponibilité          : {book['number_available']}")
    print(f"  Description            : {book['product_description']}")
    print(f"  Catégorie              : {book['category']}")
    print(f"  Note                   : {book['review_rating']}")
    print(f"  URL de l'image         : {book['image_url']}")
    print("-" * 40)
    
def affichage_livres(books):
    if not books:
        print("Aucun livre à afficher.")
        return None

    for index, book in enumerate(books, start=1):
        print(f"Livre {index}:")
        print(f"  Titre         : {book['title']}")
        print(f"  Prix          : {book['price']}")
        print(f"  Disponibilité : {book['availability']}")
        print(f"  Lien de l'image : {book['image_url']}")
        print("-" * 40)

#TRANSFORM



#LOAD




def main():
    liste_livres =extraction_livres("http://books.toscrape.com/")
    #affichage_livres(liste_livres)
    affichage_livre(liste_livres[4])
    
    
if __name__ == "__main__":
    main()

