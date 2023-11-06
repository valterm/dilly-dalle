import logging
from .globals import LOGLEVEL
logging.basicConfig(level=LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

import requests
import openai

class Dalle:
    logging.debug('Entering: __init__')
    def __init__(self, api_key):
        logging.debug('Entering __init__')
        openai.api_key = api_key

    logging.debug('Entering: generate_image')
    def generate_image(self, prompt, num_images=1, size="256x256"):
        logging.debug('Entering generate_image')
        '''
        Generates an image from a prompt.
        Returns the generated image's url.
        '''
        r = openai.Image.create(
            prompt=prompt,
            n=num_images,
            size=size
        )
        image_url = r['data'][0]['url']
        logging.debug(f"Image URL: {image_url}")
        return(image_url)
    
    logging.debug('Entering: generate_image_variation')
    def generate_image_variation(self, image):
        logging.debug('Entering generate_image_variation')
        '''
        Generates an image variation from an image.
        Returns the generated image's url.
        '''

        r = openai.Image.create_variation(
            image=image,
            size="256x256"
        )
        image_url = r['data'][0]['url']
        logging.debug(f"Image URL: {image_url}")
        return(image_url)