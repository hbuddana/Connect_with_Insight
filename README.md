# Connect_with_Insight

Build a Streamlit web app called "ConnectWith Insight".

🧠 Purpose:
The app takes the URL of a blog post and the name of the blog author as input. It then:
1. Loads and extracts the blog content from the URL
2. Summarizes the main idea or insight a developer can learn from the blog (in 1–2 lines)
3. Formats a personalized LinkedIn connection request message in this style:

   > "Hi [Author], I recently read your blog and found it insightful. I learned [summary] and I’m planning to use it in [my projects]. Would love to connect!"

4. Gives the user an option to choose:
   - A short version (≤200 characters)
   - A standard version (≤300 characters)

⚙️ Tech stack:
- Python
- Streamlit (for frontend)
- `newspaper3k` (for blog content extraction)
- Google Gemini API using LangChain's `ChatGoogleGenerativeAI` wrapper
- `.env` file for storing the API key
- Optional: `python-dotenv` to load environment variables

📄 Project structure:
- `app.py` – main Streamlit UI
- `rag_utils.py` – backend logic for content extraction, summarization, and message generation
- `.env` – contains `GEMINI_API_KEY`
- `requirements.txt` – lists dependencies

✅ Additional behavior:
- Show spinner during processing
- Display the generated message inside a preview box
- Add a download button to copy the message as `.txt`
- Show error if content can't be fetched or summarized

Optional: Use `User-Agent` header if needed for sites that block scraping.

Make sure the app stays within character limits and doesn't crash if the blog content can't be extracted.
