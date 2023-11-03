from telegram import Update,User
from telegram.ext import Updater,CallbackContext
import .dalle
from .globals import *
import threading
import requests
from io import BytesIO

# Create RequestHandler class
class RequestHandler:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def __strip_input(self, input: str, experssions: list):
        # Strip input
        for e in experssions:
            input = input.replace(e, "")
        return input
    
    def __get_username(self, update: Update):
        # Get user
        user = update.effective_user
        if not user.username:
            return(f"{user.last_name} {user.first_name}")
        else
            return (user.username)

    def __download_image_into_memory(url):
        headers = {
            "User-Agent": "Chrome/51.0.2704.103",
        }
        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            byte_stream = BytesIO(response.content)
            byte_array = byte_stream.getvalue()
            return byte_array
        else:
            return 1
    
    def __send_text_message(self, update: Update, context: CallbackContext, message: str):
        # Send message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    
    def __send_image_message(self, update: Update, context: CallbackContext, image: bytes):
        # Send image
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image
        )
        
   def __get_image_from_message(self, update: Update):
        # Get image from message
        message = update.effective_message
        photo = message.photo[-1]
        image = photo.get_file()
        return image

    def __generate_handler(self, update: Update, context: CallbackContext):
        prompt = update.message.text
        prompt = self.__strip_input(prompt, ['picgen', f"@{bot_username}"])

        # Generate image with Dalle class
        dalle = Dalle(self.openai_api_key)
        image_url = dalle.generate_image(prompt)

        # Download image into memory
        image = self.__download_image_into_memory(image_url)

        # Send image
        self.__send_image_message(update, context, image)

    def __variation_handler(self, update: Update, context: CallbackContext):
        # Get image from message
        image = self.__get_image_from_message(update)

        # Generate image variation with Dalle class
        dalle = Dalle(self.openai_api_key)
        image_url = dalle.generate_image_variation(image)

        # Download image into memory
        image = self.__download_image_into_memory(image_url)

        # Send image
        self.__send_image_message(update, context, image)
    
    # Create generate command handler
    def generate_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__generate_handler, args=(update, context)).start()
    
    def variation_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__variation_handler, args=(update, context)).start()

        