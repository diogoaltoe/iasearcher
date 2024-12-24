import streamlit as st

from backend.iasearcher import ia_search_for
from output_parsers.summary import Summary

st.title("AI Country Searcher")

country_name = st.text_input("Country", placeholder="Enter the country name here...")

if country_name:
    with st.spinner("Generating response..."):
        generated_response = ia_search_for(country_name)

        if isinstance(generated_response, Summary):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(generated_response.flag, caption="Country flag", use_container_width=True)
            
            st.write(f"**Summary:** {generated_response.summary}")
            st.write("**Interesting Facts:**")
            for fact in generated_response.facts:
                st.write(f" - {fact}")
        else:
            st.write("**Sorry, we were unable to find the details for the country you entered.**")
        