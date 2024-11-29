import requests
import os
import zipfile
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

def download_google_fonts(font_name, output_dir='fonts'):
    """
    Télécharge les fichiers WOFF2 d'une police Google Font
    """
    font_dir = os.path.join(output_dir, font_name.lower().replace(' ', '-'))
    os.makedirs(font_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Première requête pour obtenir les variantes disponibles
    api_url = f'https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}&display=swap'
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Analyser le CSS pour trouver les variantes disponibles
        available_weights = set()
        css_content = response.text
        
        # Chercher tous les poids disponibles
        for line in css_content.split('\n'):
            if 'font-weight:' in line:
                weight = line.split('font-weight:')[1].strip().rstrip(';')
                available_weights.add(weight)
        
        if available_weights:
            # Construire l'URL pour les styles normal et italic
            variant_params = []
            for weight in available_weights:
                variant_params.extend([f"0,{weight}", f"1,{weight}"])
            
            final_url = f'https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}'
            final_url += ':ital,wght@' + ';'.join(variant_params)
            
            response = requests.get(final_url, headers=headers)
            response.raise_for_status()
            
            font_urls = set()
            css_content = response.text
            current_weight = None
            current_style = None
            
            for line in css_content.split('\n'):
                if 'font-weight:' in line:
                    current_weight = line.split('font-weight:')[1].strip().rstrip(';')
                elif 'font-style:' in line:
                    current_style = 'italic' if 'italic' in line else 'normal'
                elif 'src:' in line and 'url(' in line:
                    url = line.split('url(')[1].split(')')[0]
                    if current_weight and current_style:
                        font_urls.add((url, current_weight, current_style == 'italic'))
            
            for url, weight, is_italic in font_urls:
                font_response = requests.get(url, headers=headers)
                font_response.raise_for_status()
                
                new_filename = f"{font_name.lower().replace(' ', '-')}-{weight}"
                if is_italic:
                    new_filename += "-italic"
                new_filename += ".woff2"
                
                output_path = os.path.join(font_dir, new_filename)
                
                with open(output_path, 'wb') as f:
                    f.write(font_response.content)
            
            print(f"Téléchargement réussi pour {font_name}")
        else:
            print(f"Aucune variante trouvée pour {font_name}")
            
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de {font_name}: {e}")

# Exemple d'utilisation
fonts_to_download = [
    'Roboto',
    'Open Sans',
    'Lato'
]

for font in fonts_to_download:
    download_google_fonts(font)

print("Téléchargement des polices terminé.")