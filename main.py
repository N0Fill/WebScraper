import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Adds a title for website
st.title("AI Web Scraper")

# Adds a text input box to website for URL
url = st.text_input("Enter a Website URL: ")

# Adds a button to website and runs following code when pressed
if st.button("Scrape Site"):
    st.write("Scraping the website")

    # Gets the scarped content from website (html)
    result = scrape_website(url)
    
    # Filters the html to only have the body
    body_content = extract_body_content(result)

    # Looks inside the body and remove any scripts and styles
    cleaned_content = clean_body_content(body_content)

    # Stores the cleaned content so it doesn't get lost and we can access it later
    st.session_state.dom_content = cleaned_content

    # This is a button that will show/hide what is in it when clicked
    with st.expander("View DOM Content"):
        # Text area can be expanded to whatever size you want
        st.text_area("Dom Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    # Ask user what info they want to parse
    parse_description = st.text_area("Describe what you want to parse?")

    # If button is pressed and a parse_description wa given,
    # parse the content using LLM
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            # Split the content into chunks
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Send the chunks and parse_description to LLM and get result
            result = parse_with_ollama(dom_chunks, parse_description)

            # Display the LLM's result
            st.write(result)