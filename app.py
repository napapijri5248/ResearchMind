import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research System")
st.caption("Search Agent → Reader Agent → Writer → Critic")

# ---------------------------------------------------------------------------
# Session state (keeps results visible after reruns / button clicks)
# ---------------------------------------------------------------------------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
1. **Search Agent** finds recent, reliable sources  
2. **Reader Agent** scrapes the most relevant URL  
3. **Writer** drafts the research report  
4. **Critic** reviews the report and gives feedback
        """
    )
    st.divider()
    if st.button("🗑️ Clear results", use_container_width=True):
        st.session_state.state = None
        st.session_state.topic = ""
        st.rerun()


# ---------------------------------------------------------------------------
# Pipeline (same logic as pipeline.py, with live UI progress)
# ---------------------------------------------------------------------------
def run_pipeline_with_ui(topic: str) -> dict:
    state = {}

    with st.status("Running research pipeline...", expanded=True) as status:
        # Step 1 - Search agent
        st.write("🔍 **Step 1:** Search agent is working...")
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {
                "messages": [
                    ("user", f"Find recent, reliable and detailed information about {topic}")
                ]
            }
        )
        state["search_results"] = search_result["messages"][-1].content
        st.write("✅ Search complete")

        # Step 2 - Reader agent
        st.write("📖 **Step 2:** Reader agent is scraping top resources...")
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about {topic}, "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n,"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        st.write("✅ Scraping complete")

        # Step 3 - Writer
        st.write("✍️ **Step 3:** Writer is drafting the report...")
        research_combined = (
            f"SEARCH RESULTS : \n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT : \n{state['scraped_content']}\n\n"
        )
        state["report"] = writer_chain.invoke(
            {"topic": topic, "research": research_combined}
        )
        st.write("✅ Report drafted")

        # Step 4 - Critic
        st.write("🧐 **Step 4:** Critic is reviewing the report...")
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        st.write("✅ Review complete")

        status.update(label="Research complete!", state="complete", expanded=False)

    return state


# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
with st.form("research_form"):
    topic_input = st.text_input(
        "Enter a research topic",
        placeholder="e.g. Latest advances in quantum computing",
    )
    submitted = st.form_submit_button("🚀 Start Research", type="primary")

if submitted:
    if not topic_input.strip():
        st.warning("Please enter a topic first.")
    else:
        try:
            st.session_state.topic = topic_input.strip()
            st.session_state.state = run_pipeline_with_ui(st.session_state.topic)
        except Exception as e:
            st.session_state.state = None
            st.error(f"Something went wrong while running the pipeline: {e}")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
state = st.session_state.state
if state:
    st.subheader(f"Results for: {st.session_state.topic}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown(state["report"])
        st.download_button(
            "⬇️ Download report (.md)",
            data=state["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(state["feedback"])

    with tab_search:
        st.markdown(state["search_results"])

    with tab_scraped:
        st.markdown(state["scraped_content"])
