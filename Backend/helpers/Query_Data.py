from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core import ServiceContext,set_global_service_context,Settings,StorageContext,get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core.node_parser import (SentenceSplitter)
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from helpers.SimpleChat import simple_chat_pipeline

def GetQueryResponse(id:str,customer_query:str):
    GOOGLE_API_KEY = "AIzaSyDHLca8_D4lBazOgveuzP31cssj5ETaSaM" 
    model_name = "models/embedding-001"

    embed_model = GeminiEmbedding(model_name=model_name, api_key=GOOGLE_API_KEY, title="this is a document")
    llm=Gemini(model_name="models/gemini-pro", api_key=GOOGLE_API_KEY)
        
    # Setting model
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 512
    Settings.chunk_overlap = 64

    db = chromadb.PersistentClient(path='./Chroma_db')
    chroma_collection = db.get_collection(id)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    response,chat_history = simple_chat_pipeline(vector_store,customer_query,chat_uuid=id)
    
    return (str(response),chat_history)