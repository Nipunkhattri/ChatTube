from llama_index.core import VectorStoreIndex
from llama_index.llms.gemini import Gemini
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.core.llms import ChatMessage
from llama_index.core.prompts import PromptTemplate

def format_chat_history(chat_history):
    formatted_history = []
    for i in range(0, len(chat_history), 2):
        if i + 1 < len(chat_history):
            user_message = chat_history[i]
            ai_message = chat_history[i + 1]
            formatted_history.append({
                "user_content": user_message.content,
                "ai_answer": ai_message.content
            })
    return formatted_history

def simple_chat_pipeline(vector_store, customer_query: str, chat_uuid: str, model: str = "models/gemini-pro"):
    GOOGLE_API_KEY = "AIzaSyDHLca8_D4lBazOgveuzP31cssj5ETaSaM"
    
    loaded_chat_store = SimpleChatStore.from_persist_path(
        persist_path="chat_store.json"
    )
    chat_memory = ChatMemoryBuffer.from_defaults(
        chat_store=loaded_chat_store,
        chat_store_key=chat_uuid
    )
    chat_history = chat_memory.get()

    prompt_str = (
        "We have provided context information below. \n"
        "---------------------\n"
        "{relevant_context}"
        "\n---------------------\n"
        "Chat History:\n{chat_history}\n"
        "Given this information, please answer the question: {query_str}\n"
    )
    prompt_tmpl = PromptTemplate(prompt_str)

    # Initialize components
    llm = Gemini(model_name=model, api_key=GOOGLE_API_KEY)
    index = VectorStoreIndex.from_vector_store(vector_store)
    retriever = index.as_retriever(similarity_top_k=2)
    input_component = InputComponent()


    # Define the query pipeline
    p = QueryPipeline(verbose=True)
    p.add_modules(
        {
            "input": input_component,
            "llm": llm,
            "prompt_tmpl": prompt_tmpl,
            "retriever": retriever
        }
    )
    p.add_link("input", "prompt_tmpl", src_key="query_str", dest_key="query_str")
    p.add_link("input","prompt_tmpl",src_key="chat_history",dest_key="chat_history")
    p.add_link("input", "retriever", src_key="query_str", dest_key="input")
    p.add_link("retriever", "prompt_tmpl", src_key="output", dest_key="relevant_context")
    p.add_link("prompt_tmpl", "llm")

    # Run the pipeline with the customer query
    response = p.run(query_str=customer_query,chat_history=chat_history)
    print("Pipeline Response:", response) 

    chat_memory.put(ChatMessage(role="user", content=customer_query))
    chat_memory.put(ChatMessage(role="assistant", content=str(response)))

    chat_history = chat_memory.get()
    loaded_chat_store.persist(persist_path="chat_store.json")

    chat_history = format_chat_history(chat_history)
    return (response,chat_history)