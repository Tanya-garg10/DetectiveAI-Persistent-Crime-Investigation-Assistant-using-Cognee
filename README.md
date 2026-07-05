# 🕵️ DetectiveAI — Persistent Crime Investigation Assistant

Powered by **Cognee** Knowledge Graph

## Features
- 📁 Create & manage crime cases
- 🔍 Add evidence (CCTV, Witnesses, Fingerprints, Documents)
- 🧠 AI-powered investigation chat — ask anything
- ⏰ Timeline reconstruction
- ⚠️ Contradiction detection
- 📊 Suspect confidence scores
- 📋 Final report generation
- 💾 Persistent memory via Cognee Cloud

## Setup

```bash
pip install cognee
```

Create a `.env` file:
```
COGNEE_API_KEY=your_api_key
COGNEE_TENANT_URL=https://your-tenant.aws.cognee.ai
```

## Run

```bash
python detective_ai.py
```

## Usage Flow
1. Open Dashboard
2. Create New Case or Open Existing
3. Add Evidence
4. Chat with AI — ask any question
5. Generate Final Report

## Tech Stack
- Python 3.11
- Cognee Cloud (Knowledge Graph)
- REST API
