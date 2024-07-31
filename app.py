import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import os
from llama_index.core import StorageContext, Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core.node_parser import SentenceSplitter
import random
import string
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer

GOOGLE_API_KEY = "AIzaSyDHLca8_D4lBazOgveuzP31cssj5ETaSaM" 
model_name = "models/embedding-001"

embed_model = GeminiEmbedding(model_name=model_name, api_key=GOOGLE_API_KEY, title="this is a document")
llm = Gemini(model_name="models/gemini-pro", api_key=GOOGLE_API_KEY)

def generate_random_string_id(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Setting model
Settings.embed_model = embed_model
Settings.llm = llm
Settings.chunk_size = 512
Settings.chunk_overlap = 64
splitter = SentenceSplitter()

st.title("Welcome to ChatTube!")

# Initialize session state variables
if 'collection_id' not in st.session_state:
    st.session_state.collection_id = None

upload_youtube_link = st.text_input("Paste the Youtube Link Here!")

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

if st.button("Upload Video"):
    if upload_youtube_link:
        extracted_txt = extract_transcript_details(upload_youtube_link)

        with open("Extracted_Text.txt", "w", encoding="utf-8") as file:
            file.write(extracted_txt)
        
        documents = SimpleDirectoryReader(input_files=['Extracted_Text.txt']).load_data()

        db1 = chromadb.PersistentClient(path='./Chroma_db')

        id = generate_random_string_id()

        # Save the generated ID to session state
        st.session_state.collection_id = id

        chroma_collection = db1.get_or_create_collection(id)

        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model, storage_context=storage_context, transformations=[splitter])

        st.write("Video has been Processed Successfully!")

    else:
        st.write("Please paste a YouTube link before clicking 'Upload Video'.")

query_video_text = st.text_input("Enter your query here!")

if st.button("Send Query"):
    if query_video_text:
        if st.session_state.collection_id is not None:
            db = chromadb.PersistentClient(path='./Chroma_db')
            chroma_collection = db.get_collection(st.session_state.collection_id)

            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)

            chat_store = SimpleChatStore()

            chat_memory = ChatMemoryBuffer.from_defaults(
                chat_store=chat_store,
                chat_store_key="user1",
            )

            chat_engine = index.as_chat_engine()
            response = chat_engine.chat(query_video_text)

            st.write("Response from the query:")
            st.write(response.response)
        else:
            st.write("Please upload a video first.")
    else:
        st.write("Please enter a query before clicking 'Send Query'.")