import requests
import openai

class Dalle:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_image(self, prompt, num_images=1, size="256x256"):
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
        return(img_url)
    
    def generate_image_variation(self, image):
        '''
        Generates an image variation from an image.
        Returns the generated image's url.
        '''

        r = openai.Image.create_variation(
            image=image,
            size="256x256"
        )
        image_url = r['data'][0]['url']
        return(img_url)