import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import re

#lav en rag der giver et resume af en youtube video

load_dotenv() # Load environment variables from .env file

# Get environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize ChatGPT
chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)


# Chat loop
#while True:
  #  question = input("\nInsert Youtube URL to generate content(or 'quit'): ")
   # if question.lower() == 'quit':
       # break
   # answer = xxxx(question)
  #  print(f"Answer: {answer}")

def yt_transcript(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)

    if not match:
        return "could not find video id in url"
    
    videoId= match.group(1) # hent det fundne ID

    api = YouTubeTranscriptApi()
    result = api.fetch(videoId)

    text = " ".join([snippet.text for snippet in result.snippets])  # ✅ Virker!
    print(text)
    return text

yt_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")