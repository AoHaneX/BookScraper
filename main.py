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


def extract_data(url : str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = []
         # Trouver tous les articles de livres
        book_elements = soup.find_all('article', class_='product_pod')
        for book in book_elements:
            # Extraire le titre
            title = book.h3.a['title']
            # Extraire le prix
            price = book.find('p', class_='price_color').text.strip()
            # Extraire la disponibilité
            availability = book.find('p', class_='instock availability').text.strip()
            # Extraire le lien de l'image
            image_url = book.find('img', class_='thumbnail')['src']
            # Ajouter les données dans la liste
            books.append({
                'title': title,
                'price': price,
                'availability': availability,
                'image_url': image_url
            })
        return books
    
    
        return soup
    else:
        print(f"Erreur lors de la requête: {response.status_code}")
        return None


def afficher_livres(books):
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
    liste_livres =extract_data("http://books.toscrape.com/")
    afficher_livres(liste_livres)
    
    
    
if __name__ == "__main__":
    main()

