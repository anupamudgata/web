# Web scraping logic for extracting content from websites

# Import necessary libraries

import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import time
import re

# Try to import FAISS, with a helpful error message if it fails
try:
    import faiss
except ImportError:
    raise ImportError(
        "Could not import faiss python package. "
        "Please install it with `pip install faiss-cpu` "
        "or `pip install faiss-gpu` (for CUDA supported GPU)."
    )

def scrape_website_with_bs4(url, elements=None):
    """
    Uses BeautifulSoup to scrape the given website URL.
    
    :param url: The URL of the website to scrape.
    :param elements: Optional dictionary of HTML elements to extract specifically.
                    Format: {'tag_name': {'class': 'class_name'}, ...}
    :return: The content of the web page as a dictionary.
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # If specific elements are requested
        if elements:
            result = {}
            for tag, attrs in elements.items():
                found_elements = soup.find_all(tag, attrs)
                result[tag] = [elem.get_text(strip=True) for elem in found_elements]
            return result
        
        # Otherwise, extract all text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up the text
        # Remove extra whitespace and newlines
        clean_text = re.sub(r'\s+', ' ', text)
        clean_text = re.sub(r'\n+', '\n', clean_text)
        
        return clean_text
    except Exception as e:
        print(f"An error occurred with BeautifulSoup scraping: {e}")
        return None

def scrape_website_with_langchain(url):
    """
    Uses Langchain's WebBaseLoader to scrape the given website URL.
    
    :param url: The URL of the website to scrape.
    :return: The content of the web page.
    """
    try:
        # Initialize the WebBaseLoader with the URL
        loader = WebBaseLoader(url)
        
        # Load the content
        documents = loader.load()
        
        # Process the documents as needed
        # For example, you can extract text or other elements
        content = [doc.page_content for doc in documents]
        
        return content
    except Exception as e:
        print(f"An error occurred with LangChain scraping: {e}")
        return None

def scrape_multiple_pages(urls, method="langchain", delay=1):
    """
    Scrape multiple web pages with a delay between requests to avoid rate limiting.
    
    :param urls: List of URLs to scrape.
    :param method: Scraping method to use ('langchain' or 'bs4').
    :param delay: Delay in seconds between requests.
    :return: Dictionary mapping URLs to their content.
    """
    results = {}
    
    for url in urls:
        print(f"Scraping {url}...")
        
        if method.lower() == "langchain":
            content = scrape_website_with_langchain(url)
        elif method.lower() == "bs4":
            content = scrape_website_with_bs4(url)
        else:
            raise ValueError(f"Unknown scraping method: {method}. Use 'langchain' or 'bs4'.")
            
        results[url] = content
        
        # Add delay between requests
        if delay > 0 and url != urls[-1]:  # No need to delay after the last URL
            time.sleep(delay)
    
    return results