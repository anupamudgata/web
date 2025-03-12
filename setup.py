from setuptools import setup, find_packages

setup(
    name="web_scraper_chatbot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "requests",
        "openai",
        "langchain",
        "langchain_openai",
        "python-dotenv",
        "faiss-cpu",
        "langchain_community",
        "streamlit",
    ],
) 