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
    client = chromadb.PersistentClient(path="./chroma_db")
#tabel til mine videoer
    collection=client.get_or_create_collection(
        name="youtube_videos",
        metadata={"description": "Cached Youtube video transcripts and summaries"}
    )

    return client, collection

client, collection = setup_database()
print(f"Database setup complete. Collection: {collection.name}")

def check_video_exists(collection, video_id):
    try:
        results = collection.get(ids=[video_id])

        if results['ids']:
            return True, results
        else:
            return False, None
    except:
        return False, None
    
def get_cached_video(collection, video_id):
    exists, results = check_video_exists(collection, video_id)

    if exists:
        data = results['metadatas'][0]

        return{
            'transcript': data['transcript'],
            'resume': data.get('resume', None),  
            'title': data.get('title', ''),
            'url': data['url'],
            'created_at': data['created_at']
        }
    else:
        return None
    
def save_video_to_cache(collection, video_id, url, transcript, resume=None, title=""):
    """Gem video data til cache"""
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    transcript_embedding = embeddings.embed_query(transcript)

    # Data to store 
    metadata = {
        'url': url,
        'transcript': transcript,
        'resume': resume or "",  # Tom string hvis None
        'title': title,
        'created_at': datetime.now().isoformat(),
        'language': 'unknown'  # Vi kan opdatere dette senere
    }

    collection.add(
        ids=[video_id],
        embeddings=[transcript_embedding],
        metadatas=[metadata],
        documents=[transcript]
    )
    print(f"✅ Cached video {video_id} to database")