import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import re
import chromadb
from langchain_openai import OpenAIEmbeddings
from datetime import datetime

#lav en rag der giver et resume af en youtube video

load_dotenv() # Load environment variables from .env file

# Get environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize ChatGPT
chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)

def yt_transcript(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)

    if not match:
        return "could not find video id in url"
    
    videoId= match.group(1) # hent det fundne ID

    api = YouTubeTranscriptApi()
    
    # Prøv forskellige sprog i prioriteret rækkefølge
    try:
        result = api.fetch(videoId, languages=['en'])  # Prøv engelsk først
        print("Found English transcript")
    except:
        try:
            result = api.fetch(videoId, languages=['da'])  # derefter dansk
            print("Found Danish transcript")
        except:
            try:
                result = api.fetch(videoId, languages=['da', 'en'])  
                print("Found transcript in available language")
            except Exception as e:
                return f"Could not fetch transcript: {str(e)}"

    text = " ".join([snippet.text for snippet in result.snippets])  
    return text

def format_answer(data):
    """Format youtube transcript into resume based on the data"""
    prompt = f"""
    Based on this transcript text: {data}
    
    Provide a thoroughly resume and deliver the answer in English.
    """
    response = chat.invoke(prompt)
    return response.content

#Chat loop
while True:
    url = input("\nInsert Youtube URL(or type 'quit' to exit): ")
    if url.lower() == 'quit':
        break
    data = yt_transcript(url)
    answer = format_answer(data)
    print(f"Answer: {answer}")

#database
def setup_database():
    """"Setup ChromaDB for video caching"""
    client = chromadb.PersistentClient(path="./vhroma_db")
#tabel til mine videoer
    collection=client.get_or_create_collection(
        name="youtubr_videos",
        metadata={"description": "Cached Youtube video transcripts and summaries"}
    )

    return client, collection

client, collection = setup_database()
print(f"Database setup complete. Collection: {collection.name}")