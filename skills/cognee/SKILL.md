# Cognee Memory Skill

## Overview
This skill enables your agent to store and retrieve information from Cognee Cloud knowledge graph using the REST API.

## Credentials
- **Base URL**: https://tenant-8461e652-619d-447a-8f3a-25048ea1535b.aws.cognee.ai
- **API Key**: 208fc4fad45e506c83d40742095987910da7d73b5894a2e041be88112744007f

## Available Operations

### 1. Remember (Store data)
Store new information into Cognee memory:
```
POST /api/v1/remember
Headers:
  Content-Type: application/json
  X-Api-Key: 208fc4fad45e506c83d40742095987910da7d73b5894a2e041be88112744007f
Body:
  {"text": "<your content>", "dataset_name": "default_dataset"}
```

### 2. Recall (Query memory)
Retrieve information from Cognee knowledge graph:
```
POST /api/v1/recall
Headers:
  Content-Type: application/json
  X-Api-Key: 208fc4fad45e506c83d40742095987910da7d73b5894a2e041be88112744007f
Body:
  {"query": "<your question>"}
```

### 3. Forget (Delete data)
Remove a dataset from memory:
```
DELETE /api/v1/forget
Headers:
  X-Api-Key: 208fc4fad45e506c83d40742095987910da7d73b5894a2e041be88112744007f
Body:
  {"dataset_name": "default_dataset"}
```

## Usage Instructions
1. Use `remember` to store facts, documents, or case data
2. Use `recall` to query and retrieve stored knowledge
3. Always attach data to `default_dataset` unless a specific dataset is needed
4. Responses come from the knowledge graph — richer than simple vector search

## Example — Detective Use Case
- Store: Crime case details → `remember`
- Query: "Who is the suspect?" → `recall`
- Result: AI-generated answer from knowledge graph
