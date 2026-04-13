import os
import json
import requests

# Load environment variables
CREWAI_API_URL = os.getenv('CREWAI_API_URL', 'https://api.cowork.example/v1/complete')
CREWAI_API_KEY = os.getenv('CREWAI_API_KEY', '')
DEMO_MODE = CREWAI_API_URL == 'https://api.cowork.example/v1/complete' or not CREWAI_API_KEY.strip() or 'your_api_key' in CREWAI_API_KEY

# Load configs
with open('config/agents.json', 'r') as f:
    agents = json.load(f)

with open('config/workflow.json', 'r') as f:
    workflow = json.load(f)

def build_prompt(agent, context):
    pieces = []
    pieces.append(f"Agent: {agent['name']}")
    pieces.append(f"Model: {agent['model']}")
    pieces.append(f"Role: {agent['role']}")
    pieces.append(f"Instructions: {agent['promptTemplate']}")

    if 'ticketText' in context:
        pieces.append(f"Ticket: {context['ticketText']}")
    if 'ticketCategory' in context:
        pieces.append(f"Category: {context['ticketCategory']}")
    if 'ticketSummary' in context:
        pieces.append(f"Summary: {context['ticketSummary']}")
    if 'draftReply' in context:
        pieces.append(f"Draft reply: {context['draftReply']}")

    return '\n\n'.join(pieces)

def demo_output(agent_name):
    if agent_name == 'triage-agent':
        return 'Priority: High; Category: Billing issue'
    elif agent_name == 'extract-agent':
        return 'Customer: Alex, Product: Cloud Backup, Issue: unexpected billing charge after plan upgrade.'
    elif agent_name == 'draft-agent':
        return 'Hi Alex, sorry for the confusion. I reviewed your Cloud Backup plan and the charge is related to the upgraded tier. I will issue a refund for the overcharge and confirm next steps immediately.'
    elif agent_name == 'review-agent':
        return 'Approved. The reply is empathetic, clear, and aligned with support policy.'
    else:
        return 'Demo output: no response available.'

def run_model(agent_name, model, prompt, max_tokens=512):
    if DEMO_MODE:
        print('Running in demo mode because CREWAI_API_URL or CREWAI_API_KEY is not configured.')
        return demo_output(agent_name)

    response = requests.post(CREWAI_API_URL, headers={
        'Authorization': f'Bearer {CREWAI_API_KEY}',
        'Content-Type': 'application/json'
    }, json={
        'model': model,
        'prompt': prompt,
        'max_tokens': max_tokens,
        'temperature': 0.2
    })

    if not response.ok:
        raise Exception(f'CrewAI/CoWork request failed ({response.status_code}): {response.text}')

    data = response.json()
    normalized = data.get('output') or data.get('text') or data.get('result') or data.get('data')
    if not normalized:
        raise Exception('CrewAI/CoWork returned an unexpected response structure.')
    return str(normalized).strip()

def run_agent(agent, context):
    prompt = build_prompt(agent, context)
    output = run_model(agent['name'], agent['model'], prompt)
    return output

def run_workflow(workflow, agents, initial_context):
    context = dict(initial_context)
    for step in workflow['steps']:
        agent = next((a for a in agents if a['name'] == step['agent']), None)
        if not agent:
            raise Exception(f"Agent not found: {step['agent']}")
        print(f"\n[{step['name']}] -> {step['agent']} (model={agent['model']})")
        output = run_agent(agent, context)
        context[step['outputKey']] = output
        print(output)
    return context

def main():
    ticket_text = "Hi, I just upgraded my Cloud Backup plan and I was charged again even though the confirmation email said it was a free trial. Please fix this."
    print('=== Support ticket automation started ===')
    print(ticket_text)
    result = run_workflow(workflow, agents, {'ticketText': ticket_text})
    print('\n=== Final automation result ===')
    print(result.get('finalReply', 'No final reply generated.'))
    print('\n=== Full context ===')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()