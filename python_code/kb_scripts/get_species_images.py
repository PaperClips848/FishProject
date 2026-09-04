import os
import logging
import requests

# 1. Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("get_species_images_log.txt"),
        logging.StreamHandler()
    ]
)

SPECIES_LIST = ['Etheostoma_radiosum', 'Lepomis_megalotis', 'Lepomis_macrochirus', 'Lepomis_gulosus', 'Lepomis_cyanellus', 'Lepomis_spp', 'Etheostoma_spectabile', 'Fundulus_notatus', 'Campostoma_spacideum', 'Campostoma_anomalum', 'Notropis_stramineus', 'Cyprinella_lutrensis', 'Pimephales_vigilax', 'Gambusia_affinis']

OUTPUT_DIR = "figures/rel_species_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_wikipedia_images(species):
    logging.info("Starting Wikipedia-based batch image download process...")
    
    headers = {
        'User-Agent': 'FishDataAnalysis (educational/research contact: kbrashears2@leomail.tamuc.edu)'
    }
    
    for specie in species:
        logging.info(f"Processing genus: {specie}...")
        
        # Correct Wikipedia REST API endpoint
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{specie}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)

            if response.status_code == 404:
                logging.error(f"FAILED: specie '{specie}' page not found on Wikipedia.")
                continue

            response.raise_for_status()
            data = response.json()

            # Extract image
            image_info = data.get('originalimage') or data.get('thumbnail')

            if image_info and 'source' in image_info:
                image_url = image_info['source']

                ext = ".jpg"
                if ".png" in image_url.lower():
                    ext = ".png"
                elif ".jpeg" in image_url.lower():
                    ext = ".jpeg"

                filename = os.path.join(OUTPUT_DIR, f"{specie}{ext}")

                img_response = requests.get(image_url, headers=headers, timeout=15)
                if img_response.status_code == 200:
                    with open(filename, 'wb') as handler:
                        handler.write(img_response.content)
                    logging.info(f"SUCCESS: Downloaded image for '{specie}'")
                else:
                    logging.warning(f"FAILED: Image download failed for '{specie}' with status {img_response.status_code}")
            else:
                logging.warning(f"FAILED: Wikipedia page for '{specie}' exists, but has no main profile image.")

        except requests.exceptions.RequestException as e:
            logging.error(f"FAILED: Network error fetching '{specie}'. Error details: {e}")

    logging.info("Batch download process completed.")

if __name__ == "__main__":
    download_wikipedia_images(SPECIES_LIST)
