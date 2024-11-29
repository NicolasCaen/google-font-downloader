import requests
import os
import zipfile
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

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

# Exemple d'utilisation modifié
fonts_to_download = [
    'Lora',
    'Fira Sans',
    'Noto Serif',
    'Merriweather',
    'PT Serif',
    'Nunito Sans',
    'DM Sans',
    'Quicksand',
    'Barlow',
    'Mulish',
    'Inconsolata',
    'Heebo',
    'Source Code Pro',
    'Karla',
    'Josefin Sans',
    'Cairo',
    'Dancing Script',
    'Abel',
    'Crimson Text',
    'Bitter',
    'Arimo',
    'Libre Baskerville',
    'Source Serif Pro',
    'Dosis',
    'Oxygen',
    'Libre Franklin',
    'Manrope',
    'IBM Plex Sans',
    'Prompt',
    'Titillium Web'
]

for font in fonts_to_download:
    download_google_fonts(font, output_dir='fonts-tttf', font_format='ttf')  # ou 'ttf', 'woff', etc.

print("Téléchargement des polices terminé.")