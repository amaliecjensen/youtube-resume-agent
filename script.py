import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#lav en rag der giver et resume af en youtube video

load_dotenv() # Load environment variables from .env file

# Get environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize ChatGPT
chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)


# Chat loop
while True:
    question = input("\nAsk about youtube content (or 'quit'): ")
    if question.lower() == 'quit':
        break
    answer = xxxx(question)
    print(f"Answer: {answer}")

