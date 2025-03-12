# Main application for Web Scraper Chatbot

import os
import sys
from dotenv import load_dotenv
from web_scraper_chatbot.scraper import scrape_website_with_langchain, scrape_website_with_bs4
from web_scraper_chatbot.chatbot import WebpageChatbot

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OPENAI_API_KEY.")
    sys.exit(1)

def main():
    print("\n===== Web Scraper Chatbot =====\n")
    
    # Get URL from user
    url = input("Enter the URL to scrape: ")
    
    # Choose scraping method
    print("\nChoose scraping method:")
    print("1. LangChain (recommended for most websites)")
    print("2. BeautifulSoup (alternative method)")
    method_choice = input("Enter your choice (1 or 2): ")
    
    # Scrape the website
    print(f"\nScraping {url}...")
    try:
        if method_choice == "1":
            content = scrape_website_with_langchain(url)
            method_name = "LangChain"
        else:
            content = scrape_website_with_bs4(url)
            method_name = "BeautifulSoup"
            
        if not content:
            print("Error: Failed to scrape the website.")
            return
            
        print(f"Successfully scraped the website using {method_name}.")
        
        # Initialize chatbot
        print("\nInitializing chatbot...")
        chatbot = WebpageChatbot()
        
        # Process the scraped content
        chunks = chatbot.process_scraped_content(content)
        print(f"Processed {chunks} chunks of content.")
        
        # Chat loop
        print("\n===== Chat Mode =====")
        print("You can now ask questions about the website content.")
        print("Type 'exit' to quit or 'clear' to clear conversation history.")
        
        while True:
            # Get user question
            question = input("\nYour question: ")
            
            # Check for exit command
            if question.lower() == "exit":
                break
                
            # Check for clear command
            if question.lower() == "clear":
                chatbot.clear_memory()
                print("Conversation history cleared.")
                continue
                
            # Get answer from chatbot
            answer = chatbot.ask(question)
            print(f"\nAnswer: {answer}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()