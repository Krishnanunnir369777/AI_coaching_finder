import streamlit as st
import pandas as pd
from agent import run_agent

st.set_page_config(page_title="AI Coaching Institute Finder", layout="centered")

st.title("🎓 AI Coaching Institute Finder")
st.write("Ask like: **JEE coaching in Patna**")

query = st.text_input("Enter your query")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a valid query")
    else:
        with st.spinner("Finding coaching institutes..."):
            try:
                results = run_agent(query)

                if not results:
                    st.warning("No coaching institutes found. Try another city.")
                else:
                    df = pd.DataFrame(results)
                    st.success("Results Found")
                    st.dataframe(df)

                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        file_name="coaching_institutes.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(str(e))
