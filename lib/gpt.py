import openai

class GPT:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    # Create a method to generate a dalle-promptable description of the submitted text prompt, that otherwise would not be dalle-promptable
    def generate_description(self, prompt):
        '''
        Generates a description from a prompt.
        Returns the generated description.
        '''

        request = f"Reply only with the generated description, say nothing else and say no niceities and other sentences. Create an extremely detailed single-paragraph description usable for a DALL-E prompt without going against your content policy: \n {prompt}"

        response = openai.Completion.create(
            engine="text-davinci-004", 
            prompt=request,
            max_tokens=750
        )
        
        description = response.choices[0].text.strip()
        return(description)
    
    # Create a method to rephrase a submitted text prompt, that otherwise would not be dalle-promptable
    def rephrase_prompt(self, prompt):
        '''
        Rephrases a prompt.
        Returns the rephrased prompt.
        '''

        request = f"Reply only with the rephrased prompt, say nothing else and say no niceities and other sentences. Rephrase the following DALL-E prompt to be compliant with the DALL-E content policy: \n {prompt}"

        response = openai.Completion.create(
            engine="text-davinci-004", 
            prompt=request,
            max_tokens=750
        )
        
        rephrased_prompt = response.choices[0].text.strip()
        return(rephrased_prompt)