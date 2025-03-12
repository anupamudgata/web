# Web Scraper Chatbot

This project scrapes web pages and allows interaction with the scraped data using Langchain and OpenAI. It provides a simple command-line interface for users to input a URL, scrape its content, and then ask questions about the scraped information.

## Features

- Web scraping using either LangChain or BeautifulSoup
- Conversational AI interface powered by OpenAI
- Text chunking and vector storage for efficient retrieval
- Conversation memory to maintain context during chat

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key (see `.env.example`)

## Usage

Run the main application:

```
python main.py
```

Follow the prompts to:
1. Enter a URL to scrape
2. Choose a scraping method (LangChain or BeautifulSoup)
3. Ask questions about the scraped content

## Commands

During the chat session, you can use these special commands:
- `exit`: End the chat session
- `clear`: Clear the conversation history

## Project Structure

- `main.py`: Entry point for the application
- `web_scraper_chatbot/`
  - `scraper.py`: Web scraping functionality
  - `chatbot.py`: Conversational AI interface
  - `utils.py`: Utility functions
- `tests/`: Test cases for the application

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in `requirements.txt`