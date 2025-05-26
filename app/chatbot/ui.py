import asyncio
import gradio as gr

from dotenv import load_dotenv
from app.chatbot.chatbot import Chatbot


async def main():
    # Create an instance of the Support Ticket ChatBot
    bot = Chatbot.create_support_ticket_chatbot()
    title = "Sam, your Support Ticket Assistant"

    welcome_message: gr.MessageDict = gr.MessageDict(
        content=await bot.chat(""), role="assistant"
    )

    # Create Support Ticket Management interface
    chat_interface = gr.ChatInterface(
        type="messages",
        fn=bot.chat,
        chatbot=gr.Chatbot(
            type="messages",
            value=[welcome_message],
            scale=1),
        title=title,
        description="I can help you create and manage support tickets and action items.",
        theme="default",
        fill_height=True,
        fill_width=True,
    )

    chat_interface.launch()


# Run the main function
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
