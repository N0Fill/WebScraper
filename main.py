import streamlit as st
from scrape import scrape_website

# Adds a title for website
st.title("AI Web Scraper")

# Adds a text input box to website for URL
url = st.text_input("Enter a Website URL: ")

# Adds a button to website and runs following code when pressed
if st.button("Scarpe Site"):
    st.write("Scraping the website")

    result = scrape_website(url)
    print(result)