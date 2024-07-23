from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_exponential

import requests
import os

from extract_data_from_news_site.Logging import Logging as logging

class ImageDownloader:
    def __init__(self, output_dir, max_workers=5):
        self.output_dir = output_dir
        self.max_workers = max_workers

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def download_image(self, url, file_name):
        """Download an image from the given URL and save it to the specified path with retry."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            with open(file_name, 'wb') as file:
                file.write(response.content)
            logging.info(f"Image successfully downloaded and saved to {file_name}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading the image from {url}: {e}")
            raise  # Reraise exception to trigger retry

    def download_images_in_parallel(self, image_src_paths):
        """Download multiple images in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for url, file_name in image_src_paths:
                futures.append(executor.submit(self.download_image, url, f"{self.output_dir}/{file_name}"))
            
            for future in futures:
                try:
                    future.result()  # Wait for all downloads to complete
                except Exception as e:
                    logging.error("Image not downloadeds")
