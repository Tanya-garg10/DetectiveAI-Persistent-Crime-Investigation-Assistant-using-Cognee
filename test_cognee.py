import os`nimport urllib.request, json

url = "https://tenant-8461e652-619d-447a-8f3a-25048ea1535b.aws.cognee.ai/api/v1/recall"
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": os.getenv("COGNEE_API_KEY", "")
}
data = json.dumps({"query": "What do you know from cognee?"}).encode()
req = urllib.request.Request(url, data=data, headers=headers, method="POST")

with urllib.request.urlopen(req) as res:
    results = json.loads(res.read().decode())
    print("=" * 60)
    print("🧠 COGNEE MEMORY — What do you know?")
    print("=" * 60)
    for r in results:
        dataset = r["dataset_name"]
        answer = r["text"]
        print(f"\n📂 Dataset: {dataset}")
        print(f"💬 {answer}")
        print("-" * 50)
