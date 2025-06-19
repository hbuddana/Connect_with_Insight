import os
from typing import Tuple, Optional
from newspaper import Article
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

def extract_blog_content(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract content from a blog URL using newspaper3k with fallback to requests+BeautifulSoup.
    Returns tuple of (content, error_message).
    """
    try:
        # Try newspaper3k first
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            return article.text, None
            
        # Fallback to requests + BeautifulSoup
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        if text:
            return text, None
            
        return None, "Could not extract content from the URL"
        
    except Exception as e:
        return None, f"Error extracting content: {str(e)}"

def generate_summary(content: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate a concise summary of the blog content using Gemini.
    Returns tuple of (summary, error_message).
    """
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that summarizes technical blog posts. "
                      "Extract the main insight or learning that would be valuable for a developer. "
                      "Keep it to 1-2 lines maximum."),
            ("user", "Here's the blog content to summarize:\n\n{content}")
        ])
        
        chain = prompt | model | StrOutputParser()
        summary = chain.invoke({"content": content})
        return summary.strip(), None
        
    except Exception as e:
        return None, f"Error generating summary: {str(e)}"

def generate_connection_message(
    author_name: str,
    summary: str,
    message_type: str = "standard"
) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate a personalized LinkedIn connection request message.
    Returns tuple of (message, error_message).
    """
    try:
        max_length = 200 if message_type == "short" else 300
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a professional networking assistant. "
                      f"Generate a personalized LinkedIn connection request message. "
                      f"Keep it under {max_length} characters. "
                      f"Use this template but make it natural:\n"
                      f"'Hi [Author], I recently read your blog and found it insightful. "
                      f"I learned [summary] and I'm planning to use it in [my projects]. "
                      f"Would love to connect!'"),
            ("user", "Author name: {author}\nSummary: {summary}")
        ])
        
        chain = prompt | model | StrOutputParser()
        message = chain.invoke({
            "author": author_name,
            "summary": summary
        })
        
        # Ensure message is within character limit
        if len(message) > max_length:
            message = message[:max_length-3] + "..."
            
        return message.strip(), None
        
    except Exception as e:
        return None, f"Error generating message: {str(e)}" 