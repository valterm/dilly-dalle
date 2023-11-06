from telegram import Update, User
from telegram.ext import Updater,CallbackContext
from .dalle import *
from .gpt import *
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
        else:
            return (user.username)

    def __download_image_into_memory(self, *args, url=None):
        if not url and args:
            url = args[0]
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
            text=message,
            # parse_mode="MarkdownV2"
            # parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
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
        prompt = self.__strip_input(prompt, ['picgen', f"@{BOT_USERNAME}"])

        # Generate image with Dalle class
        dalle = Dalle(self.openai_api_key)
        image_url = dalle.generate_image(prompt)

        # Download image into memory
        print(image_url)
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
    
    def __description_handler(self, update: Update, context: CallbackContext):
        prompt = update.message.text
        prompt = self.__strip_input(prompt, ['describe', f"@{BOT_USERNAME}"])

        # Generate description with GPT class
        gpt = GPT(self.openai_api_key)
        description = gpt.generate_description(prompt)

        # Send description
        self.__send_text_message(update, context, description)
    
    def __rephrase_handler(self, update: Update, context: CallbackContext):
        prompt = update.message.text
        prompt = self.__strip_input(prompt, ['rephrase', f"@{BOT_USERNAME}"])

        # Rephrase prompt with GPT class
        gpt = GPT(self.openai_api_key)
        rephrased_prompt = gpt.rephrase_prompt(prompt)

        # Send rephrased prompt
        self.__send_text_message(update, context, rephrased_prompt)
    
    def __help_handler(self, update: Update, context: CallbackContext):
        # Create help message describing the commands
        help_message = f"Hi @{self.__get_username(update)}! I'm {BOT_USERNAME} and I can generate images from text prompts. Here are the commands I understand:\n\n"
        help_message += f"1. /picgen <text prompt> - Generates an image from a text prompt.\n"
        help_message += f"2. /variation <image> - Generates an image variation from an image.\n"
        help_message += f"3. /describe <text prompt> - Generates a description from a text prompt.\n"
        help_message += f"4. /rephrase <text prompt> - Rephrases a text prompt.\n"
        help_message += f"5. /help - Displays this help message.\n\n"
        help_message += f"Please note that I'm still in beta and I may not work as expected. If you encounter any issues, please report them to on the github {GITHUB_REPO}.\n"
        
        # Send help message
        self.__send_text_message(update, context, help_message)
    
    def __start_handler(self, update: Update, context: CallbackContext):
        # Create start message
        start_message = f"Hi @{self.__get_username(update)}! I'm {BOT_USERNAME} and I can generate images from text prompts. Send /help to see the commands I understand.\n\n"
        start_message += f"Please note that I'm still in beta and I may not work as expected. If you encounter any issues, please report them to on the github {GITHUB_REPO}.\n"

        # Send start message
        self.__send_text_message(update, context, start_message)

    def __unknown_handler(self, update: Update, context: CallbackContext):
        # Create unknown message
        unknown_message = f"Sorry {self.__get_username(update)}, I didn't understand that command. Send /help to see the commands I understand.\n\n"

        # Send unknown message
        self.__send_text_message(update, context, unknown_message)

    def __prototype_handler(self, update: Update, context: CallbackContext):
        # Create prototype message
        prototype_message = f"Sorry, but that command is still in unavailable. Please send /help to see the list of available commands."
        # Send prototype message
        self.__send_text_message(update, context, prototype_message)

    # Create command handlers
    def start_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__start_handler, args=(update, context)).start()

    def help_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__help_handler, args=(update, context)).start()

    def picgen_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__generate_handler, args=(update, context)).start()
    
    def variation_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__variation_handler, args=(update, context)).start()

    def description_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__description_handler, args=(update, context)).start()

    def rephrase_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__rephrase_handler, args=(update, context)).start()
    
    def unknown_command_handler(self, update: Update, context: CallbackContext):
        threading.Thread(target=self.__unknown_handler, args=(update, context)).start()