import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
import time

# --- 1. Improved Multi-Backend Search Tool ---
def robust_free_search(query):
    """Tries multiple DuckDuckGo backends to ensure results are found."""
    backends = ["api", "html", "lite"]  # Cycle through different ways to get data
    results = []
    
    for backend in backends:
        try:
            with DDGS() as ddgs:
                # Add a 'human-like' region and moderate safesearch
                search_gen = ddgs.text(
                    keywords=query,
                    region='in-en',
                    safesearch='moderate',
                    backend=backend
                )
                
                # Fetch first 10 results
                for i, r in enumerate(search_gen):
                    if i >= 10: break
                    results.append({
                        "Name": r.get('title'),
                        "Snippet": r.get('body'),
                        "Link": r.get('href')
                    })
                
                if results:
                    return results  # Stop if we found something
        except Exception:
            continue # Try next backend if one fails
    return []

# --- 2. UI Setup ---
st.set_page_config(page_title="Pro Scout AI", layout="wide")
st.title("🎓 Institute Scout AI (Free & Unlimited)")

with st.sidebar:
    st.header("🔑 Free API Key")
    groq_key = st.text_input("Groq API Key", type="password")

# --- 3. Execution Logic ---
if prompt := st.chat_input("e.g., JEE coaching in Patna"):
    if not groq_key:
        st.warning("Please enter your Groq API Key!")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            status = st.status("🔍 Searching...")
            
            try:
                llm = ChatGroq(groq_api_key=groq_key, model_name="llama-3.3-70b-versatile")
                
                # Step 1: Broad Search
                status.update(label=f"📡 Searching for: {prompt}")
                raw_data = robust_free_search(prompt)
                
                # Step 2: If empty, try a simpler "Direct Search"
                if not raw_data:
                    status.update(label="🔄 First search failed. Trying simpler query...")
                    raw_data = robust_free_search(f"{prompt} contact details list")

                if raw_data:
                    status.update(label="📊 Extracting Table...", state="running")
                    
                    extract_prompt = (
                        f"From these search snippets, extract a markdown table with 'Name', 'Phone', and 'Address'. "
                        f"If data is missing, put 'N/A'. Use ONLY the provided data:\n\n{raw_data}"
                    )
                    table_content = llm.invoke(extract_prompt).content
                    
                    status.update(label="✅ Success!", state="complete")
                    st.markdown(table_content)
                    
                    # CSV Download
                    df = pd.DataFrame(raw_data)
                    st.download_button("📥 Download Results", data=df.to_csv(index=False).encode('utf-8'), file_name="results.csv")
                else:
                    status.update(label="❌ No results found.", state="error")
                    st.error("DuckDuckGo is blocking the request. Try again in 2 minutes or use a broader search.")
                    
            except Exception as e:
                status.update(label="🛑 Error", state="error")
                st.error(f"Error: {e}")