"""
🕵️ DetectiveAI - Persistent Crime Investigation Assistant
Powered by Cognee Cloud Knowledge Graph
"""

import asyncio
import json
import urllib.request
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────
import os; TENANT_URL = os.getenv("COGNEE_TENANT_URL", "https://tenant-8461e652-619d-447a-8f3a-25048ea1535b.aws.cognee.ai")
API_KEY = os.getenv("COGNEE_API_KEY", "")

import cognee

# ─── COGNEE HELPERS ───────────────────────────────────────

def cognee_recall(query, dataset=None):
    """Query Cognee REST API"""
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
            answers = []
            for r in results:
                if r.get("text"):
                    answers.append(r["text"])
            return answers
    except Exception as e:
        return [f"Error: {e}"]


async def cognee_remember(text, dataset="default_dataset"):
    """Store data in Cognee"""
    await cognee.serve(url=TENANT_URL, api_key=API_KEY)
    await cognee.remember(text, dataset_name=dataset)
    await cognee.disconnect()


# ─── DISPLAY HELPERS ──────────────────────────────────────

def header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def section(title):
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print('─' * 40)

def menu(options):
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    print()


# ─── CASE MANAGEMENT ──────────────────────────────────────

def create_case():
    header("📁 CREATE NEW CASE")
    name = input("  Case Name: ").strip()
    location = input("  Location: ").strip()
    date = input(f"  Date [{datetime.now().strftime('%d %B %Y')}]: ").strip() or datetime.now().strftime('%d %B %Y')
    officer = input("  Officer Name: ").strip()

    case_text = f"""
CASE FILE: {name}
Location: {location}
Date: {date}
Officer: {officer}
Status: Active Investigation
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    dataset = name.lower().replace(" ", "-")

    print("\n  💾 Storing case in Cognee...")
    asyncio.run(cognee_remember(case_text, dataset=dataset))
    print(f"  ✅ Case '{name}' created! Dataset: '{dataset}'")
    return {"name": name, "dataset": dataset, "location": location, "date": date, "officer": officer}


def add_evidence(case):
    header(f"🔍 ADD EVIDENCE — {case['name']}")
    evidence_types = [
        "Witness Statement",
        "CCTV Report",
        "Fingerprint Report",
        "Call Records",
        "Document",
        "Audio Transcript",
        "Other"
    ]
    print("  Evidence Types:")
    menu(evidence_types)
    choice = input("  Select type [1-7]: ").strip()
    try:
        etype = evidence_types[int(choice) - 1]
    except:
        etype = "Other"

    print(f"\n  Enter {etype} (press Enter twice when done):")
    lines = []
    while True:
        line = input("  ")
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    content = "\n".join(lines).strip()

    evidence_text = f"""
EVIDENCE — {case['name']}
Type: {etype}
Time Added: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Content:
{content}
"""
    print("\n  💾 Storing evidence in Cognee...")
    asyncio.run(cognee_remember(evidence_text, dataset=case["dataset"]))
    print(f"  ✅ {etype} stored in knowledge graph!")


def investigation_chat(case):
    header(f"💬 INVESTIGATION CHAT — {case['name']}")
    print("  Ask anything about this case. Type 'exit' to go back.\n")
    print("  Example questions:")
    print("  → Who is the suspect?")
    print("  → Explain the full timeline")
    print("  → List all evidence")
    print("  → What contradictions exist?")
    print("  → Show suspect confidence scores")
    print("  → Summarize the investigation")
    print("  → What were John's movements?")
    print("  → Generate final report\n")

    while True:
        query = input("  🔍 Your question: ").strip()
        if query.lower() in ["exit", "quit", "back"]:
            break
        if not query:
            continue

        print("\n  🧠 Querying Cognee knowledge graph...")
        answers = cognee_recall(query, dataset=case["dataset"])

        section("🤖 AI Answer")
        if answers:
            for ans in answers:
                print(f"\n  {ans}\n")
        else:
            print("  No results found. Try adding more evidence first.")

        # Special handlers
        if "contradiction" in query.lower():
            section("⚠️ Contradiction Analysis")
            contradictions = cognee_recall("What contradictions exist in the evidence?", dataset=case["dataset"])
            for c in contradictions:
                print(f"  {c}")

        if "confidence" in query.lower() or "score" in query.lower():
            section("📊 Suspect Confidence Scores (AI Estimate)")
            scores = cognee_recall("List all suspects and their likelihood", dataset=case["dataset"])
            for s in scores:
                print(f"  {s}")
            print("\n  ⚠️  Note: These are AI estimates, not legal proof.")

        if "report" in query.lower():
            generate_report(case)


def generate_report(case):
    header(f"📋 FINAL INVESTIGATION REPORT — {case['name']}")

    queries = [
        ("📌 Case Summary", "Summarize the entire case"),
        ("⏰ Timeline", "Reconstruct the full timeline of events"),
        ("🔍 Evidence", "List all evidence collected"),
        ("🕵️ Suspects", "Who are all the suspects and their roles?"),
        ("⚠️ Contradictions", "What contradictions exist in the evidence?"),
        ("💡 Recommendations", "What are the next steps for investigation?"),
    ]

    report_lines = [
        f"DETECTIVE AI — INVESTIGATION REPORT",
        f"Case: {case['name']}",
        f"Location: {case.get('location', 'N/A')}",
        f"Date: {case.get('date', 'N/A')}",
        f"Officer: {case.get('officer', 'N/A')}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
    ]

    for title, query in queries:
        section(title)
        print(f"  ⏳ Fetching...")
        answers = cognee_recall(query, dataset=case["dataset"])
        report_lines.append(f"\n{title}")
        report_lines.append("-" * 40)
        for ans in answers:
            print(f"  {ans}\n")
            report_lines.append(ans)

    # Save report
    report_file = f"report_{case['dataset']}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n  💾 Report saved: {report_file}")


def view_history(case):
    header(f"📜 INVESTIGATION HISTORY — {case['name']}")
    print("  🧠 Retrieving all stored knowledge...\n")
    answers = cognee_recall("Tell me everything about this investigation", dataset=case["dataset"])
    for ans in answers:
        print(f"  {ans}\n")


def search_cases():
    header("🔎 SEARCH PREVIOUS CASES")
    query = input("  Enter search query: ").strip()
    if not query:
        return
    print("\n  🧠 Searching across all Cognee memory...")
    answers = cognee_recall(query)
    section("Search Results")
    for ans in answers:
        print(f"  {ans}\n")


# ─── PRELOADED CASE ───────────────────────────────────────

PRELOADED_CASE = {
    "name": "Missing Diamond",
    "dataset": "detective-brain",
    "location": "Royal Mansion",
    "date": "5 July 2026",
    "officer": "Inspector Rahul"
}


# ─── MAIN DASHBOARD ───────────────────────────────────────

def main():
    header("🕵️  DETECTIVE AI — Powered by Cognee")
    print("  Persistent Crime Investigation Assistant")
    print(f"  Connected to: {TENANT_URL[:50]}...")

    # Active case tracker
    active_case = None

    while True:
        header("📊 DASHBOARD")
        print(f"  Active Case: {active_case['name'] if active_case else 'None'}\n")
        menu([
            "Create New Case",
            "Open Existing Case (Missing Diamond)",
            "Add Evidence to Active Case",
            "Investigation Chat",
            "View Investigation History",
            "Search Previous Cases",
            "Generate Final Report",
            "Exit"
        ])

        choice = input("  Select option [1-8]: ").strip()

        if choice == "1":
            active_case = create_case()

        elif choice == "2":
            active_case = PRELOADED_CASE
            print(f"\n  ✅ Opened case: '{active_case['name']}'")
            print(f"  📂 Dataset: {active_case['dataset']}")

        elif choice == "3":
            if not active_case:
                print("\n  ⚠️  No active case. Create or open a case first.")
            else:
                add_evidence(active_case)

        elif choice == "4":
            if not active_case:
                print("\n  ⚠️  No active case. Create or open a case first.")
            else:
                investigation_chat(active_case)

        elif choice == "5":
            if not active_case:
                print("\n  ⚠️  No active case. Create or open a case first.")
            else:
                view_history(active_case)

        elif choice == "6":
            search_cases()

        elif choice == "7":
            if not active_case:
                print("\n  ⚠️  No active case. Create or open a case first.")
            else:
                generate_report(active_case)

        elif choice == "8":
            print("\n  👋 Detective AI shutting down. Stay sharp!\n")
            break

        else:
            print("\n  ⚠️  Invalid option. Try again.")


if __name__ == "__main__":
    main()
