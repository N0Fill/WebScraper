import streamlit as st # Import streamlit for error display

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager  # For dowloading the Chrome Web Driver

# Libraries for WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser...")

    # Specifies how the web driver should operate (settings for it)
    options = Options()
    options.add_argument("--headless")  # Run headless (no GUI)
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("window-size=1920x1080") # Specify window size

    # Sets up the Chrome webdriver
    # This is an application that allows us to control chrome
    # This now automatically downloads and uses the correct driver
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
    except Exception as e:
        # Display an error in the Streamlit app if driver fails
        st.error(f"Error initializing Chrome driver: {e}")
        print(f"Error initializing Chrome driver: {e}")
        return None

    try:
        # Uses webdriver to go to website
        driver.get(website) 

        print("Page loaded...")

        # Set a max wait time (e.g., 10 seconds)
        timeout = 10

        # Define what you are waiting for.
        # This is just a generic example. You should wait for an element
        # that you know must load, like a main content <div> or <h1>.
        # Here, we'll just wait for the <body> tag to be present.
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("Page has loaded (or timeout was reached).")

        # Gets the website's html
        html = driver.page_source 

        return html
    
    except Exception as e:
        st.error(f"Error during scraping: {e}")
        print(f"Error during scraping: {e}")
        return None
    finally:
        # Ensure the driver is quit even if errors occur
        if 'driver' in locals() and driver:
            driver.quit()
            print("Chrome browser closed.")

def extract_body_content(html_content):
    # Parses the content we scraped
    soup = BeautifulSoup(html_content, "html.parser")

    # Gest the body from scraped content
    body_content = soup.body
    
    # Returns the body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    # Parses content again
    soup = BeautifulSoup(body_content, "html.parser")

    # Looks inside the parsed content (soup) and remove any scripts and styles
    for script_or_style in soup(["script","style"]):
        script_or_style.extract()

    # Gets all of the new cleaned content and separates it with a new line
    cleaned_content = soup.get_text(separator="/n")

    # Removes all blank lines and strips leading/trailing whitespace from the rest
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

# Splits the text into "batches" for the LLM,
# as LLMs same a token limit (usually around 8000 characters).
# We then feed the LLM 1 batch at a time
def split_dom_content(dom_content, max_length=6000):
    # i starts at 0, so it will return first 6000 characters
    # i is then increased my max_length (6000) and the next characters start from 6000 and go up to 12000
    # this loop repeats until i reaches the length of dom_content
    return {
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    }