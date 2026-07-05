"""
Detective Brain - Cognee Cloud Script
Crime Case: Missing Diamond

Steps:
1. Connect to Cognee Cloud
2. Add crime case data (remember)
3. Run queries (recall)
"""

import asyncio
import cognee

# ─── CONFIG ───────────────────────────────────────────────
import os; API_KEY = os.getenv("COGNEE_API_KEY", "")
TENANT_URL = os.getenv("COGNEE_TENANT_URL", "https://tenant-8461e652-619d-447a-8f3a-25048ea1535b.aws.cognee.ai")  # Update if you have a custom tenant URL
DATASET_NAME = "detective-brain"

# ─── CRIME CASE DATA ──────────────────────────────────────
CRIME_CASE = """
Crime Case: Missing Diamond

Crime happened at 9 PM in mansion. Safe was opened without damage. Diamond is missing.

John was near house at 8:50 PM. Unknown person seen on CCTV entering back door at 8:55 PM.
Security guard saw someone running at 9:05 PM.

Back door was unlocked. No alarm triggered. Only John, manager, owner had access.
John claims he was at home but CCTV conflicts.
"""

# ─── QUERIES ──────────────────────────────────────────────
QUERIES = [
    "Who is the suspect?",
    "Explain full timeline",
    "List all evidence",
]


async def main():
    print("=" * 60)
    print("🧠 DETECTIVE BRAIN - Powered by Cognee")
    print("=" * 60)

    # STEP 1: Connect to Cognee Cloud
    print("\n📡 Connecting to Cognee Cloud...")
    try:
        await cognee.serve(
            url=TENANT_URL,
            api_key=API_KEY,
        )
        print("✅ Connected!")
    except Exception as e:
        print(f"⚠️  serve() not available or already local mode: {e}")
        print("   Trying local mode with API key...")
        cognee.config.set_llm_api_key(API_KEY)

    # STEP 2: Add crime case data
    print(f"\n📦 Adding crime case data to dataset: '{DATASET_NAME}'...")
    try:
        await cognee.remember(
            CRIME_CASE,
            dataset_name=DATASET_NAME,
        )
        print("✅ Data added & knowledge graph built!")
    except Exception as e:
        print(f"❌ remember() failed: {e}")
        print("   Trying legacy add + cognify flow...")
        await cognee.add(CRIME_CASE, dataset_name=DATASET_NAME)
        await cognee.cognify(datasets=[DATASET_NAME])
        print("✅ Data added via legacy flow!")

    # STEP 3: Run queries
    print("\n" + "=" * 60)
    print("🔍 RUNNING QUERIES")
    print("=" * 60)

    for i, query in enumerate(QUERIES, 1):
        print(f"\n❓ Query {i}: {query}")
        print("-" * 40)
        try:
            results = await cognee.recall(
                query_text=query,
                dataset_name=DATASET_NAME,
            )
            if results:
                for result in results:
                    print(f"   {result}")
            else:
                print("   (No results returned)")
        except Exception as e:
            # Try legacy search if recall fails
            try:
                results = await cognee.search(
                    query_text=query,
                    datasets=[DATASET_NAME],
                )
                if results:
                    for result in results:
                        print(f"   {result}")
                else:
                    print("   (No results returned)")
            except Exception as e2:
                print(f"   ❌ Query failed: {e2}")

    # Cleanup
    try:
        await cognee.disconnect()
    except Exception:
        pass

    print("\n" + "=" * 60)
    print("✅ Detective Brain session complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
