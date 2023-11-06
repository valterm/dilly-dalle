import logging
from lib.globals import LOGLEVEL
logging.basicConfig(level=LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

import openai

class GPT:
    logging.debug('Entering: __init__')
    def __init__(self, api_key):
        logging.debug('Entering __init__')
        openai.api_key = api_key
    
    # Create a method to generate a dalle-promptable description of the submitted text prompt, that otherwise would not be dalle-promptable
    logging.debug('Entering: generate_description')
    def generate_description(self, prompt):
        logging.debug('Entering generate_description')
        '''
        Generates a description from a prompt.
        Returns the generated description.
        '''

        request = (
            "Reply only with the generated description, say nothing else and say no niceities and other sentences."
            "Do not under any circumstances use the names of real people, real brands, copyrighted or trademarked materials, or anything else that goes against the DALL-E API safety system. Do not ever use the actual name, brand, or anything of the sorts given."
            "Create an extremely detailed description usable for a DALL-E API prompt: \n"
            f"{prompt}"
            
        )
        
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=request,
            max_tokens=500,  # Adjust the number of tokens as needed
            temperature=0.5,  # Lower for more deterministic responses
            top_p=1,  # Typically 1, but can be reduced for less diversity
            frequency_penalty=1,  # Adjust based on how much repetition you want to avoid
            presence_penalty=1,
        )
        
        description = response.choices[0].text.strip()
        return(description)
    
    # Create a method to rephrase a submitted text prompt, that otherwise would not be dalle-promptable
    logging.debug('Entering: rephrase_prompt')
    def rephrase_prompt(self, prompt):
        logging.debug('Entering rephrase_prompt')
        '''
        Rephrases a prompt.
        Returns the rephrased prompt.
        '''
        request = (
            "Reply only with the generated description, say nothing else and say no niceities and other sentences. "
            "Do not under any circumstances use the names of real people, real brands, copyrighted or trademarked materials, or anything else that goes against the DALL-E API safety system. Do not ever use the actual name, brand, or anything of the sorts given."
            "Rephrase the following DALL-E prompt to be compliant with the DALL-E API Safety System:"
            f"{prompt}"
        )

        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=request,
            max_tokens=500,  # Adjust the number of tokens as needed
            temperature=0.5,  # Lower for more deterministic responses
            top_p=1,  # Typically 1, but can be reduced for less diversity
            frequency_penalty=1,  # Adjust based on how much repetition you want to avoid
            presence_penalty=1,
        )
        
        rephrased_prompt = response.choices[0].text.strip()
        return(rephrased_prompt)