import requests
from gradio_client import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your actual Telegram Bot token
TELEGRAM_API_TOKEN = '8057329196:AAH_TLievIWa_ohGUbt4QwFsdTQPOjqwNys'

# Gradio model API URL (replace with your actual URL)
GRADIO_API_URL = "https://huggingface.co/spaces/aidevhund/chatbot"

# Create a Gradio client
client = Client("aidevhund/chatbot")

# Function to start the bot (optional, just sends a welcome message)
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm the HundAI Chatbot. Ask me anything about Hund Ecosystem!")

# Function to handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat.id

    try:
        # Send the user's message to the Gradio model via Client.predict
        result = client.predict(
            message=user_message,
            history=[],  # Start with an empty history
            api_name="/respond"  # Ensure you're using the correct API endpoint
        )

        # Log the raw response from Gradio
        print("Raw result from Gradio:", result)

        # Extract the model's response from the tuple
        if isinstance(result, tuple) and len(result) > 0:
            # First element of the tuple is the actual response list
            response_list = result[0]
            
            if isinstance(response_list, list) and len(response_list) > 0:
                # Extract the inner response list
                inner_response = response_list[0]  # Get the first item of the response list
                
                if isinstance(inner_response, list) and len(inner_response) > 1:
                    # Get the second item as the actual answer
                    model_response = inner_response[1]
                else:
                    model_response = "I couldn't extract the proper response from the model."
            else:
                model_response = "The response format from the model was unexpected."
        else:
            model_response = "I couldn't understand the response from the model."

        # Send the cleaned response back to the user
        await update.message.reply_text(model_response)
    except Exception as e:
        # Log the error and return a generic response
        print(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

# Main function to set up the bot and handlers
def main():
    # Create an Application object with your bot's API token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Command handler for the /start command
    application.add_handler(CommandHandler('start', start))

    # Message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
