from core.nlp import ContentAnalyzer
from core.fetcher import RSSFetcher
import streamlit as st
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

# Loading user personas from config


def load_config():
    with open('configs/config.json') as f:
        return json.load(f)


# UI Sidebar
st.sidebar.title("Choose a Persona")
config = load_config()
user_names = list(config['user_personas'].keys())
selected_user = st.sidebar.selectbox("Select User", user_names)

fetcher = RSSFetcher()
analyzer = ContentAnalyzer()

st.title("AI-Powered Personalized Newsletter Generator")

if selected_user:
    prefs = config['user_personas'][selected_user]
    articles = fetcher.fetch_feeds(prefs['sources'], config['rss_feeds'])

    st.subheader(f" Newsletter for {selected_user}")
    st.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}")

    markdown_newsletter = f"# {selected_user}'s Personalized Newsletter\n\n"
    markdown_newsletter += f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n"

    if not articles:
        st.warning("No articles fetched for this user.")
    else:
        for i, article in enumerate(articles[:5]):
            highlighted_title = analyzer.highlight_keywords(
                article['title'], prefs['interests'])
            highlighted_summary = analyzer.highlight_keywords(
                article['summary'], prefs['interests'])

            st.markdown(f"### {highlighted_title}")
            st.markdown(f"*Source: {article['source']}*")
            st.markdown(highlighted_summary)
            st.markdown(f"[Read more]({article['link']})")

            markdown_newsletter += f"## {highlighted_title}\n"
            markdown_newsletter += f"*Source: {article['source']}*\n"
            markdown_newsletter += f"{highlighted_summary}\n"
            markdown_newsletter += f"[Read more]({article['link']})\n\n"

        os.makedirs("outputs", exist_ok=True)
        md_path = f"outputs/{selected_user.replace(' ', '_')}_newsletter.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_newsletter)

        st.download_button(" Download Newsletter (.md)",
                           markdown_newsletter, file_name=os.path.basename(md_path))
