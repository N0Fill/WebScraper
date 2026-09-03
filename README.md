# AI Web Scraper

This is a Streamlit application that uses a local LLM (via Ollama) to intelligently scrape and parse content from any website.

The user provides a URL and a natural language instruction (e.g., "Extract all links and their text"), and the app returns the requested information.

# Features

Dynamic Scraping: Uses Selenium to scrape content from modern, JavaScript-heavy websites.

Intelligent Parsing: Connects to a local Ollama instance (e.g., Llama 3.1) to understand user requests and parse HTML.

Clean Output: Automatically removes <script>, <style>, and other non-visible tags to provide clean text to the LLM.

Chunking: Splits large websites into smaller chunks to fit within the LLM's context window.

Robust Prompting: Uses LangChain to create a specific prompt template, ensuring the LLM only returns the requested data.

# How It Works

Enter URL: The user provides a website URL.

Scrape Site: The app uses Selenium and webdriver-manager to launch a headless Chrome browser, load the page, and wait for the content to be present.

Clean Content: The raw HTML is passed to BeautifulSoup, which extracts the <body> and removes all <script> and <style> tags. The remaining text is cleaned of blank lines.

Enter Prompt: The user is shown the cleaned text and prompted to describe what information they want to extract (e.g., "List all job titles and their locations").

Parse Content: The cleaned text is split into chunks and, along with the user's prompt, is sent to the local LLM via LangChain.

Display Results: The LLM's response, containing only the extracted information, is displayed to the user.

# Setup & Installation

Follow these steps to run the project locally.

1. Ollama (Required)

You must have Ollama installed and running on your machine.

Once Ollama is running, pull the LLM model this app uses (e.g., llama3.1 or llama3):

ollama pull llama3.1


(Note: You can change the model by updating the model variable in parse.py)

2. Python Project

Clone the repository:

git clone [https://github.com/N0Fill/WebScraper](https://github.com/N0Fill/WebScraper)
cd your-repo-name


Create and activate a virtual environment:

# Windows
1: python -m venv venv
2: .\venv\Scripts\activate

# macOS / Linux
1: python3 -m venv venv
2: source venv/bin/activate


Install dependencies:
Create a requirements.txt file with the following content:

streamlit 
langchain 
langchain_ollama
selenium
beautifulsoup4
lxml 
html5lib
python-dotenv
webdriver-manager


Then, install the requirements:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run main.py


Your app will be available at http://localhost:8501.

# Deploying to Streamlit Cloud

This app is ready to be deployed to Streamlit Cloud. Because it uses Selenium, you must provide a packages.txt file to tell Streamlit to install Google Chrome.

requirements.txt: Ensure this file exists (as shown in Step 3 above).

packages.txt: Create a file named packages.txt in the root of your repository with this single line:

google-chrome-stable


Push both files to GitHub and deploy your app.

# File Structure

main.py: The main Streamlit application file. Handles the UI and app flow.

scrape.py: Contains all functions related to web scraping (Selenium, BeautifulSoup, cleaning, and chunking).

parse.py: Contains all functions related to LLM interaction (LangChain prompts and the Ollama connection).

requirements.txt: A list of all Python packages required for the project.

packages.txt: (For deployment) A list of OS-level packages to install.
