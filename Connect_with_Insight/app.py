import streamlit as st
from rag_utils import extract_blog_content, generate_summary, generate_connection_message
import os
from dotenv import load_dotenv
#from streamlit_copy_to_clipboard import st_copy_to_clipboard

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ GEMINI_API_KEY not found in .env file. Please add your API key to continue.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="ConnectWith Insight",
    page_icon="🤝",
    layout="centered"
)

# App title and description
st.title("🤝 ConnectWith Insight")
st.markdown("""
Generate personalized LinkedIn connection requests based on blog posts you've read.
Simply enter the blog URL and author's name, and we'll help you craft a meaningful connection message.
""")

# Input fields
url = st.text_input("Blog Post URL", placeholder="https://example.com/blog-post")
author_name = st.text_input("Author's Name", placeholder="John Doe")

# Message type selection
message_type = st.radio(
    "Message Length",
    options=["short", "standard"],
    format_func=lambda x: "Short (≤200 chars)" if x == "short" else "Standard (≤300 chars)",
    horizontal=True
)

# Process button
if st.button("Generate Connection Message", type="primary"):
    if not url or not author_name:
        st.error("Please provide both the blog URL and author's name.")
    else:
        with st.spinner("Processing..."):
            # Extract content
            content, content_error = extract_blog_content(url)
            if content_error:
                st.error(content_error)
                st.stop()
                
            # Generate summary
            summary, summary_error = generate_summary(content)
            if summary_error:
                st.error(summary_error)
                st.stop()
                
            # Generate connection message
            message, message_error = generate_connection_message(
                author_name=author_name,
                summary=summary,
                message_type=message_type
            )
            if message_error:
                st.error(message_error)
                st.stop()
            
            # Display results
            st.success("✨ Message generated successfully!")
            
            # Show summary
            st.subheader("📝 Key Insight")
            st.info(summary)
            
            # Show generated message
            st.subheader("💌 Connection Message")
            st.text_area(
                "Preview",
                value=message,
                height=100,
                disabled=True
            )

            # Copy button 
            st.download_button("📋 Copy Message as .txt", data=message, file_name="linkedin_message.txt")
            

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ by ConnectWith Insight | "
    "Powered by Google Gemini AI"
)