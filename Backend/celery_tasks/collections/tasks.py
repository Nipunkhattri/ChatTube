from celery import shared_task
from logger import logger
from database import db
import os
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
from pydub.silence import split_on_silence
import shutil
from models.Ytube_text import Ytube_text
import yt_dlp
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext,Settings,VectorStoreIndex,SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core.node_parser import (SentenceSplitter)
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer

r = sr.Recognizer()

def split_text(text, max_length):
    # Split the text into chunks of max_length characters
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

GOOGLE_API_KEY = "AIzaSyDHLca8_D4lBazOgveuzP31cssj5ETaSaM" 
model_name = "models/embedding-001"

embed_model = GeminiEmbedding(model_name=model_name, api_key=GOOGLE_API_KEY, title="this is a document")
llm=Gemini(model_name="models/gemini-pro", api_key=GOOGLE_API_KEY)

# Setting model
Settings.embed_model = embed_model
Settings.llm = llm
Settings.chunk_size = 512
Settings.chunk_overlap = 64
splitter = SentenceSplitter()

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        
        # Fetch list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to fetch the English transcript, fallback to other languages if needed
        try:
            transcript_text = transcript_list.find_transcript(['en']).fetch()
        except NoTranscriptFound:
            print("No English transcript found, attempting to retrieve other available transcripts...")
            for transcript in transcript_list:
                print(f"Trying {transcript.language}...")
                try:
                    transcript_text = transcript.fetch()
                    break
                except:
                    continue
            else:
                raise NoTranscriptFound("No transcripts found in any available language.")
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        
        return transcript

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    
@shared_task
def extract_text_and_create_embeddings(random_string_id : str,user_id : int,Youtube_link : str):
    extracted_txt = extract_transcript_details(Youtube_link)

    with open("Extracted_Text.txt", "w", encoding="utf-8") as file:
        file.write(extracted_txt)
    
    output = os.path.join(os.getcwd(), "Extracted_Text.txt")

    with open(output, "r") as file:
        extracted_txt_data = file.read()

    documents = SimpleDirectoryReader(input_files=['Extracted_Text.txt']).load_data()
    
    data = Ytube_text.query.filter_by(id=random_string_id).first()

    if data:
        data.extracted_text = extracted_txt_data
        data.in_process = False
        db.session.commit()
    
    collection_Name = data.id

    db1 = chromadb.PersistentClient(path='./Chroma_db')
    chroma_collection = db1.get_or_create_collection(collection_Name)

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents,embed_model=embed_model,storage_context=storage_context,transformations=[splitter])
    
    chat_store = SimpleChatStore()
    chat_memory = ChatMemoryBuffer.from_defaults(
        chat_store=chat_store,
        chat_store_key=collection_Name,
    )
    chat_store.persist(persist_path="chat_store.json")

    return True