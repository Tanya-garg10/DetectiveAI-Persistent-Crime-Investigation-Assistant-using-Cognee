"""
🕵️ DetectiveAI - Streamlit Web App
Powered by Cognee Cloud Knowledge Graph
"""

import streamlit as st
import json
import urllib.request
from datetime import datetime

# ─── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="🕵️ DetectiveAI",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CONFIG ───────────────────────────────────────────────
import os
TENANT_URL = st.secrets.get("COGNEE_TENANT_URL", os.getenv("COGNEE_TENANT_URL", "https://tenant-8461e652-619d-447a-8f3a-25048ea1535b.aws.cognee.ai"))
API_KEY = st.secrets.get("COGNEE_API_KEY", os.getenv("COGNEE_API_KEY", ""))

PRELOADED_CASE = {
    "name": "Missing Diamond",
    "dataset": "detective-brain",
    "location": "Royal Mansion",
    "date": "5 July 2026",
    "officer": "Inspector Rahul"
}

# ─── COGNEE HELPER ────────────────────────────────────────
def cognee_recall(query, dataset=None):
    url = f"{TENANT_URL}/api/v1/recall"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }
    body = {"query": query}
    if dataset:
        body["dataset_name"] = dataset
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            results = json.loads(res.read().decode())
            return [r["text"] for r in results if r.get("text")]
    except Exception as e:
        return [f"❌ Error: {e}"]


def cognee_remember(text, dataset="default_dataset"):
    import asyncio
    import cognee as cg
    async def _store():
        await cg.serve(url=TENANT_URL, api_key=API_KEY)
        await cg.remember(text, dataset_name=dataset)
        await cg.disconnect()
    asyncio.run(_store())


# ─── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/126177848?s=200&v=4", width=80)
    st.title("🕵️ DetectiveAI")
    st.caption("Powered by Cognee Cloud")
    st.divider()

    page = st.radio("Navigation", [
        "🏠 Dashboard",
        "📁 Create Case",
        "🔍 Add Evidence",
        "💬 Investigation Chat",
        "📋 Final Report",
        "🔎 Search Cases"
    ])

    st.divider()
    st.caption(f"🟢 Connected to Cognee Cloud")
    st.caption(f"📂 Active Case: {st.session_state.get('active_case', {}).get('name', 'None')}")


# ─── SESSION STATE ────────────────────────────────────────
if "active_case" not in st.session_state:
    st.session_state.active_case = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ══════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.title("🕵️ DetectiveAI — Crime Investigation Assistant")
    st.caption("Persistent Memory powered by Cognee Knowledge Graph")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Memory", "Cognee Cloud", "Active")
    with col2:
        st.metric("📂 Active Case", 
                  st.session_state.active_case["name"] if st.session_state.active_case else "None", "")
    with col3:
        st.metric("💬 Chat Messages", len(st.session_state.chat_history), "")

    st.divider()

    st.subheader("Quick Start")
    col1, col2 = st.columns(2)

    with col1:
        st.info("**📂 Missing Diamond Case**\nPre-loaded case with full evidence")
        if st.button("🔓 Open Missing Diamond Case", use_container_width=True):
            st.session_state.active_case = PRELOADED_CASE
            st.session_state.chat_history = []
            st.success(f"✅ Case opened: Missing Diamond")
            st.rerun()

    with col2:
        st.info("**➕ New Case**\nCreate a fresh investigation")
        if st.button("📁 Create New Case", use_container_width=True):
            st.switch_page if hasattr(st, 'switch_page') else None
            st.info("👈 Go to 'Create Case' in sidebar")

    st.divider()
    st.subheader("🕵️ About This Case")
    if st.session_state.active_case:
        case = st.session_state.active_case
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Case:** {case['name']}")
            st.write(f"**Location:** {case.get('location', 'N/A')}")
        with col2:
            st.write(f"**Date:** {case.get('date', 'N/A')}")
            st.write(f"**Officer:** {case.get('officer', 'N/A')}")
    else:
        st.warning("No active case. Open or create a case to begin.")


# ══════════════════════════════════════════════════════════
# PAGE: CREATE CASE
# ══════════════════════════════════════════════════════════
elif page == "📁 Create Case":
    st.title("📁 Create New Case")
    st.divider()

    with st.form("create_case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_name = st.text_input("Case Name", placeholder="Missing Diamond")
            location = st.text_input("Location", placeholder="Royal Mansion")
        with col2:
            date = st.text_input("Date", value=datetime.now().strftime("%d %B %Y"))
            officer = st.text_input("Officer Name", placeholder="Inspector Rahul")

        description = st.text_area("Initial Case Description", 
                                   placeholder="Describe what happened...", height=150)

        submitted = st.form_submit_button("🚀 Create Case", use_container_width=True)

        if submitted and case_name:
            dataset = case_name.lower().replace(" ", "-")
            case_text = f"""
CASE FILE: {case_name}
Location: {location}
Date: {date}
Officer: {officer}
Description: {description}
Status: Active Investigation
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            with st.spinner("💾 Storing case in Cognee Knowledge Graph..."):
                cognee_remember(case_text, dataset=dataset)

            st.session_state.active_case = {
                "name": case_name,
                "dataset": dataset,
                "location": location,
                "date": date,
                "officer": officer
            }
            st.success(f"✅ Case '{case_name}' created and stored in Cognee!")
            st.balloons()


# ══════════════════════════════════════════════════════════
# PAGE: ADD EVIDENCE
# ══════════════════════════════════════════════════════════
elif page == "🔍 Add Evidence":
    st.title("🔍 Add Evidence")

    if not st.session_state.active_case:
        st.warning("⚠️ No active case. Please open or create a case first.")
    else:
        case = st.session_state.active_case
        st.caption(f"Case: **{case['name']}**")
        st.divider()

        evidence_type = st.selectbox("Evidence Type", [
            "Witness Statement",
            "CCTV Report",
            "Fingerprint Report",
            "Call Records",
            "Document",
            "Audio Transcript",
            "Other"
        ])

        evidence_content = st.text_area("Evidence Content", height=200,
                                        placeholder="Enter evidence details here...")

        if st.button("💾 Store Evidence in Cognee", use_container_width=True):
            if evidence_content:
                evidence_text = f"""
EVIDENCE — {case['name']}
Type: {evidence_type}
Time Added: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Content:
{evidence_content}
"""
                with st.spinner("🧠 Storing in Cognee Knowledge Graph..."):
                    cognee_remember(evidence_text, dataset=case["dataset"])
                st.success(f"✅ {evidence_type} stored in knowledge graph!")
            else:
                st.error("Please enter evidence content.")

        st.divider()
        st.subheader("📋 Pre-loaded Evidence (Missing Diamond)")
        with st.expander("View existing evidence"):
            st.markdown("""
- 🕐 **8:50 PM** — John seen near mansion
- 📹 **8:55 PM** — Unknown person enters back door (CCTV)
- 💎 **9:00 PM** — Safe opened, diamond missing
- 🏃 **9:05 PM** — Guard sees person running
- 🚪 Back door was unlocked
- 🔕 No alarm triggered
- 🔑 Only John, Manager, Owner had access
            """)


# ══════════════════════════════════════════════════════════
# PAGE: INVESTIGATION CHAT
# ══════════════════════════════════════════════════════════
elif page == "💬 Investigation Chat":
    st.title("💬 Investigation Chat")

    if not st.session_state.active_case:
        st.warning("⚠️ No active case. Please open or create a case first.")
    else:
        case = st.session_state.active_case
        st.caption(f"Case: **{case['name']}** | Ask anything about this investigation")

        # Quick question buttons
        st.subheader("Quick Questions")
        cols = st.columns(3)
        quick_questions = [
            "Who is the suspect?",
            "Explain the full timeline",
            "List all evidence",
            "What contradictions exist?",
            "Show suspect confidence scores",
            "What were John's movements?",
            "Summarize the investigation",
            "What is the motive?",
            "Who had access to the safe?"
        ]
        for i, q in enumerate(quick_questions):
            with cols[i % 3]:
                if st.button(q, use_container_width=True, key=f"q{i}"):
                    st.session_state.pending_question = q

        st.divider()

        # Chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle quick question
        if "pending_question" in st.session_state:
            question = st.session_state.pending_question
            del st.session_state.pending_question

            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("🧠 Querying Cognee knowledge graph..."):
                    answers = cognee_recall(question, dataset=case["dataset"])
                answer_text = "\n\n".join(answers) if answers else "No results found."
                st.markdown(answer_text)
                st.session_state.chat_history.append({"role": "assistant", "content": answer_text})

        # Chat input
        if prompt := st.chat_input("Ask anything about the investigation..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🧠 Querying Cognee knowledge graph..."):
                    answers = cognee_recall(prompt, dataset=case["dataset"])
                answer_text = "\n\n".join(answers) if answers else "No results found."
                st.markdown(answer_text)
                st.session_state.chat_history.append({"role": "assistant", "content": answer_text})

        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


# ══════════════════════════════════════════════════════════
# PAGE: FINAL REPORT
# ══════════════════════════════════════════════════════════
elif page == "📋 Final Report":
    st.title("📋 Final Investigation Report")

    if not st.session_state.active_case:
        st.warning("⚠️ No active case. Please open or create a case first.")
    else:
        case = st.session_state.active_case
        st.caption(f"Case: **{case['name']}**")

        if st.button("🚀 Generate Full Report", use_container_width=True, type="primary"):
            report_sections = [
                ("📌 Case Summary", "Summarize the entire case"),
                ("⏰ Timeline", "Reconstruct the full chronological timeline of events"),
                ("🔍 Evidence", "List all evidence collected in the case"),
                ("🕵️ Suspects", "Who are all the suspects and their roles?"),
                ("⚠️ Contradictions", "What contradictions exist in the evidence?"),
                ("📊 Confidence Scores", "What are the suspect confidence scores?"),
                ("💡 Recommendations", "What are the next investigation steps?"),
            ]

            report_text = f"""# 🕵️ DETECTIVE AI — INVESTIGATION REPORT
**Case:** {case['name']}
**Location:** {case.get('location', 'N/A')}
**Date:** {case.get('date', 'N/A')}
**Officer:** {case.get('officer', 'N/A')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
---
"""
            for title, query in report_sections:
                st.subheader(title)
                with st.spinner(f"Fetching {title}..."):
                    answers = cognee_recall(query, dataset=case["dataset"])
                answer = "\n\n".join(answers) if answers else "No data available."
                st.markdown(answer)
                report_text += f"\n## {title}\n{answer}\n"
                st.divider()

            st.download_button(
                "📥 Download Report",
                data=report_text,
                file_name=f"report_{case['dataset']}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════
# PAGE: SEARCH CASES
# ══════════════════════════════════════════════════════════
elif page == "🔎 Search Cases":
    st.title("🔎 Search Across All Cases")
    st.divider()

    query = st.text_input("Search query", placeholder="Search anything across all cases...")

    if st.button("🔍 Search", use_container_width=True) and query:
        with st.spinner("🧠 Searching Cognee memory..."):
            answers = cognee_recall(query)

        if answers:
            for i, ans in enumerate(answers, 1):
                with st.expander(f"Result {i}", expanded=True):
                    st.markdown(ans)
        else:
            st.info("No results found.")
