# Streamlit Web App for Web Scraper Chatbot

import streamlit as st
import os
from dotenv import load_dotenv
from web_scraper_chatbot.scraper import scrape_website_with_langchain, scrape_website_with_bs4
from web_scraper_chatbot.chatbot import WebpageChatbot

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    st.error("Error: OPENAI_API_KEY not found in environment variables. Please create a .env file with your OPENAI_API_KEY.")
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Web Scraper Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'url' not in st.session_state:
    st.session_state.url = ""
if 'method' not in st.session_state:
    st.session_state.method = "1"
if 'content_processed' not in st.session_state:
    st.session_state.content_processed = False
if 'chunks' not in st.session_state:
    st.session_state.chunks = 0

# Function to process the URL and initialize the chatbot
def process_url():
    with st.spinner(f"Scraping {st.session_state.url}..."):
        try:
            # Scrape the website based on the selected method
            if st.session_state.method == "1":
                content = scrape_website_with_langchain(st.session_state.url)
                method_name = "LangChain"
            else:
                content = scrape_website_with_bs4(st.session_state.url)
                method_name = "BeautifulSoup"
                
            if not content:
                st.error("Failed to scrape the website.")
                return
                
            st.success(f"Successfully scraped the website using {method_name}.")
            
            # Initialize chatbot
            with st.spinner("Initializing chatbot..."):
                st.session_state.chatbot = WebpageChatbot()
                
                # Process the scraped content
                st.session_state.chunks = st.session_state.chatbot.process_scraped_content(content)
                st.session_state.content_processed = True
                st.success(f"Processed {st.session_state.chunks} chunks of content.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Function to clear chat history
def clear_chat():
    if st.session_state.chatbot:
        st.session_state.chatbot.clear_memory()
    st.session_state.conversation_history = []
    st.success("Conversation history cleared.")

# Main app UI
st.title("Web Scraper Chatbot 🤖")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # URL input
    st.text_input("Enter the URL to scrape:", key="url")
    
    # Method selection
    st.radio(
        "Choose scraping method:",
        options=["1", "2"],
        format_func=lambda x: "LangChain (recommended)" if x == "1" else "BeautifulSoup",
        key="method",
        index=0
    )
    
    # Process button
    if st.button("Process URL"):
        process_url()
    
    # Clear chat button
    if st.button("Clear Chat History"):
        clear_chat()
    
    st.divider()
    st.markdown("### About")
    st.markdown(
        """This app scrapes web pages and allows interaction with the scraped data using Langchain and OpenAI. 
        Enter a URL, choose a scraping method, and then ask questions about the content."""
    )

# Main content area
if not st.session_state.content_processed:
    st.info("👈 Enter a URL in the sidebar and click 'Process URL' to get started.")
    
    # Display example questions
    st.markdown("### Example Questions You Can Ask After Processing a URL:")
    st.markdown(
        """
        - What is the main topic of this webpage?
        - Summarize the key points from this article.
        - What products or services are mentioned?
        - Who is the author of this content?
        - When was this content published?
        """
    )
else:
    # Chat interface
    st.header("Chat with the Website Content")
    
    # Display chat messages
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - using a different approach without on_submit
    user_question = st.chat_input("Ask a question about the website content...")
    
    # Process the user input when a message is submitted
    if user_question and st.session_state.content_processed:
        # Add user message to chat history
        st.session_state.conversation_history.append({"role": "user", "content": user_question})
        
        # Get answer from chatbot
        with st.spinner("Thinking..."):
            answer = st.session_state.chatbot.ask(user_question)
        
        # Add assistant message to chat history
        st.session_state.conversation_history.append({"role": "assistant", "content": answer})
        
        # Force a rerun to update the chat display
        st.rerun()

# Footer
st.divider()
st.caption("Powered by Langchain and OpenAI")