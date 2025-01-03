import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL:")

if st.button("Scrape Site"):
    st.write("Scraping the website...")
    result = scrape_website(url)

    if result is None:
        st.error("Failed to scrape the website. Please check the URL.")
    else:
        try:
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            st.session_state.body_content = cleaned_content  # Store in session state

            with st.expander("View DOM content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

# Fix the session state key check
if "body_content" in st.session_state:  # Check for the correct key
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Process the body content stored in session state
            dom_chunks = split_dom_content(st.session_state.body_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)