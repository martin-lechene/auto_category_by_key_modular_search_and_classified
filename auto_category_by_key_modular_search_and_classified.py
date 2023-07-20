import requests
from bs4 import BeautifulSoup
import os

def check_category(site_html, categories_keywords):
    """
    Analyse le contenu d'un site web pour déterminer la catégorie en fonction des mots-clés spécifiés.
    :param site_html: Le contenu HTML du site web
    :param categories_keywords: Un dictionnaire qui contient les catégories comme clés et les mots-clés associés comme valeurs.
    :return: Un ensemble de catégories détectées pour le site web
    """
    soup = BeautifulSoup(site_html, "html.parser")
    keywords = soup.find_all(["h1","h2","h3","p"])
    categories = set()
    for keyword in keywords:
        for category, keywords in categories_keywords.items():
            for cat_keyword in keywords:
                if cat_keyword in keyword.text.lower():
                    categories.add(category)
    if not categories:
        categories.add("others")
    return categories

def create_directories(categories):
    """
    Crée des dossiers pour chaque catégorie spécifiée
    :param categories: Un ensemble de catégories
    """
    for cat in categories:
        if not os.path.exists(cat):
            os.mkdir(cat)

def classify_site(url, categories_keywords):
    """
    Classifie un site web en fonction de son contenu en utilisant les mots-clés spécifiés et en créant des dossiers pour chaque catégorie.
    :param url: L'URL du site web à classer
    :param categories_keywords: Un dictionnaire qui contient les catégories comme clés et les mots-clés associés comme valeurs.
    """
    response = requests.get(url)
    site_html = response.text
    categories = check_category(site_html, categories_keywords)
    create_directories(categories)
    for cat in categories:
        os.rename(url.split("/")[-1], f"{cat}/{url.split('/')[-1]}")

#Définir les catégories et les mots-clés associés
categories_keywords = {
    "front-end": ["javascript", "react", "angular", "vue"],
    "php": ["php"],
    "laravel": ["laravel"],
    "php8": ["php 8"],
    "npm": ["npm"],
	"web-development": ["web development", "webdev"]
}

url = "https://www.example.com"

# Classifiez le site web en utilisant la fonction classify_site
classify_site(url, categories_keywords)
