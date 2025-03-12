# Chatbot logic for interacting with scraped web content

# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Try to import FAISS, with a helpful error message if it fails
try:
    from langchain_community.vectorstores import FAISS
except ImportError:
    raise ImportError(
        "Could not import faiss python package. "
        "Please install it with `pip install faiss-cpu` "
        "or `pip install faiss-gpu` (for CUDA supported GPU)."
    )

# Also try to import faiss directly as it's needed by langchain
try:
    import faiss
except ImportError:
    # This is handled by the FAISS import above, so we can pass silently
    pass

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# Check if API key is available
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OPENAI_API_KEY.")

class WebpageChatbot:
    def __init__(self, model_name="gpt-3.5-turbo"):
        """
        Initialize the chatbot with the specified model.
        
        :param model_name: The OpenAI model to use for chat completion.
        """
        self.model_name = model_name
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation_chain = None
        self.vector_store = None
        
    def process_scraped_content(self, content):
        """
        Process the scraped content and prepare it for question answering.
        
        :param content: List of text content scraped from a website.
        """
        # Join the content if it's a list
        if isinstance(content, list):
            text = "\n\n".join(content)
        else:
            text = content
            
        # Split text into chunks for better processing
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # Create vector store
        self.vector_store = FAISS.from_texts(chunks, self.embeddings)
        
        # Create conversation chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory
        )
        
        return len(chunks)
    
    def ask(self, question):
        """
        Ask a question about the processed web content.
        
        :param question: The question to ask.
        :return: The answer from the AI.
        """
        if not self.conversation_chain:
            return "Please process some web content first using process_scraped_content()"
        
        try:
            response = self.conversation_chain({"question": question})
            return response["answer"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_memory(self):
        """
        Clear the conversation memory.
        """
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        if self.vector_store:
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(),
                memory=self.memory
            )