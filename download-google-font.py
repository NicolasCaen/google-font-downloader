import requests
import os
import zipfile
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

# Ajouter au début du fichier, après les imports
popular_fonts = [
    "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins", "Source Sans Pro", "Roboto Condensed", 
    "Oswald", "Raleway", "Inter", "Ubuntu", "Roboto Mono", "Nunito", "Playfair Display", 
    "Noto Sans", "Rubik", "PT Sans", "Merriweather", "Work Sans", "Mukta", "Noto Sans JP", 
    "Lora", "Fira Sans", "Noto Serif", "PT Serif", "Titillium Web", "DM Sans", "Quicksand", 
    "Nunito Sans", "Heebo", "IBM Plex Sans", "Barlow", "Karla", "Josefin Sans", "Source Code Pro", 
    "Cairo", "Mulish", "Crimson Text", "Nanum Gothic", "Abel", "Arimo", "Dancing Script", 
    "Bitter", "Dosis", "Libre Franklin", "Exo 2", "Manrope", "Oxygen", "Libre Baskerville", 
    "Inconsolata", "Prompt", "Cabin", "Comfortaa", "Assistant", "Maven Pro", "Kanit", 
    "Archivo Narrow", "Pacifico", "Merriweather Sans", "Hind Siliguri", "Varela Round", 
    "Arvo", "Lobster", "Teko", "Asap", "Overpass", "Signika", "Hind", "Rajdhani", 
    "Urbanist", "Indie Flower", "Yanone Kaffeesatz", "Catamaran", "Archivo", "Caveat", 
    "Barlow Condensed", "Cardo", "Bebas Neue", "Questrial", "Amatic SC", "Vollkorn", 
    "Encode Sans", "Outfit", "Noto Sans KR", "Zilla Slab", "Spectral", "Alegreya", 
    "Cormorant Garamond", "Domine", "Chivo", "Satisfy", "Russo One", "Lexend", "Prata", 
    "Martel", "Cinzel", "Jost", "Noto Sans TC", "Fira Code", "Secular One", "Righteous", 
    "Tajawal", "Alata", "Advent Pro", "Yantramanav", "Orbitron", "Chakra Petch", 
    "Philosopher", "Saira", "Sarabun", "Quattrocento Sans", "Kalam", "Courgette", 
    "Permanent Marker", "Noticia Text", "Crete Round", "Tinos", "Shadows Into Light", 
    "Patua One", "Alfa Slab One", "Passion One", "Amiri", "Nanum Myeongjo", "Acme", 
    "Didact Gothic", "Signika Negative", "Barlow Semi Condensed", "Josefin Slab", 
    "Saira Condensed", "Antic Slab", "Fredoka One", "Gelasio", "Noto Serif JP", 
    "Alegreya Sans", "Bree Serif", "Cuprum", "Cantarell", "Staatliches", "Pathway Gothic One", 
    "Balsamiq Sans", "Playfair Display SC", "Paytone One", "Abril Fatface", "Vidaloka", 
    "Montserrat Alternates", "Sorts Mill Goudy", "Yeseva One", "Ropa Sans", "Poiret One", 
    "Rokkitt", "Gudea", "Marck Script", "Neuton", "Khand", "Istok Web", "Playball", 
    "Sawarabi Mincho", "Unica One", "Neucha", "Economica", "Allura", "Fugaz One", 
    "Arapey", "Glegoo", "Sintony", "Covered By Your Grace", "Allerta", "Tenor Sans"
]

print("Liste des 150 polices Google Fonts les plus populaires:")
for i, font in enumerate(popular_fonts, 1):
    print(f"{i}. {font}")
print("\n" + "="*50 + "\n")

def download_google_fonts(font_name, output_dir='fonts', font_format='woff2'):
    """
    Télécharge les fichiers de police Google Font dans le format spécifié
    Args:
        font_name (str): Nom de la police
        output_dir (str): Répertoire de sortie
        font_format (str): Format de police ('woff2', 'woff', 'ttf', etc.)
    """
    font_dir = os.path.join(output_dir, font_name.lower().replace(' ', '-'))
    os.makedirs(font_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Utilisation de l'API Google Fonts pour obtenir toutes les variantes
    weights = ['100', '200', '300', '400', '500', '600', '700', '800', '900']
    styles = ['normal', 'italic']
    
    base_url = f'https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}&display={font_format}'
    
    font_urls = set()
    for weight in weights:
        for style in styles:
            url = f"{base_url}:ital,wght@{1 if style == 'italic' else 0},{weight}"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200 and 'url(' in response.text:
                    css_content = response.text
                    for line in css_content.split('\n'):
                        if 'src:' in line and 'url(' in line:
                            font_url = line.split('url(')[1].split(')')[0]
                            font_urls.add((font_url, weight, style == 'italic'))
            except requests.RequestException:
                continue

    # Téléchargement des fichiers
    for url, weight, is_italic in font_urls:
        try:
            font_response = requests.get(url, headers=headers)
            font_response.raise_for_status()
            
            new_filename = f"{font_name.lower().replace(' ', '-')}-{weight}"
            if is_italic:
                new_filename += "-italic"
            new_filename += f".{font_format}"
            
            output_path = os.path.join(font_dir, new_filename)
            
            with open(output_path, 'wb') as f:
                f.write(font_response.content)
                
            print(f"Téléchargé: {new_filename}")
            
        except requests.RequestException as e:
            print(f"Erreur lors du téléchargement de {url}: {e}")

    print(f"Téléchargement terminé pour {font_name}")

# Obtenir le chemin du script actuel
script_dir = os.path.dirname(os.path.abspath(__file__))

# Interaction utilisateur avec le chemin relatif au script
font_name = input("Quelle police souhaitez-vous télécharger ? ")
font_format = input("Dans quel format souhaitez-vous télécharger la police ? (par défaut: woff2) ") or "woff2"
default_output = os.path.join(script_dir, "fonts")
output_dir = input("Dans quel dossier souhaitez-vous sauvegarder la police ? (par défaut: dossier courant) ") or default_output

download_google_fonts(font_name, output_dir=output_dir, font_format=font_format)

print("Téléchargement de la police terminé.")