# CrewAI / CoWork Demo

## Use case
Automate customer support ticket handling using 4 open-source LLM agents.

Agents:
- `triage-agent`: categorize incoming tickets and assign priority.
- `extract-agent`: pull the key issue, customer name, and product from the ticket.
- `draft-agent`: draft a support response.
- `review-agent`: verify tone, correctness, and alignment with support policy.

## Structure
- `config/agents.json`: agent definitions and open-source model references.
- `config/workflow.json`: workflow steps using a CrewAI/CoWork-style orchestration.
- `src/agents.js`: prompt assembly logic.
- `src/crewaiClient.js`: generic CrewAI/CoWork HTTP client.
- `src/pipeline.js`: orchestration and agent execution.
- `src/index.js`: sample execution with a support ticket.

## Setup
1. Install Node.js 18+.
2. Copy `.env.example` to `.env`.
3. Set `CREWAI_API_KEY` and optionally `CREWAI_API_URL`.

## Run
```powershell
cd C:\Users\USER\crewai-cowork-demo
node src/index.js
```

## Configure CrewAI / CoWork
The integration uses `src/crewaiClient.js` and expects a JSON POST body:
- `model`
- `prompt`
- `max_tokens`
- `temperature`

If your provider uses a different request shape, update `src/crewaiClient.js` accordingly.

## Demo mode
If `CREWAI_API_KEY` is empty or `.env` still uses the placeholder key, the demo will run in local stub mode and simulate agent outputs instead of calling a real API.

## Notes
- This demo is ready for real CrewAI/CoWork-style execution once your endpoint and API key are configured.
- If your provider returns a different field name, the client normalizes `output`, `text`, and `result`.
- You can extend the workflow by adding more agents or saving final replies to a ticket system.
