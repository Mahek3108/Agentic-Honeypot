Conversation opened. 1 unread message.

Skip to content
Using Gmail with screen readers
in:spam 
1 of 29
(no subject)
Spam
Rajesh Shitap
Attachments
23:32 (3 minutes ago)
to me

Why is this message in spam? You have blocked rajms1977@gmail.com.
Unblock senderMove to inbox

 One attachment
  •  Scanned by Gmail
# AI Conversational Honeypot API

## Description

This project implements an AI-driven conversational honeypot designed to detect scams, extract actionable intelligence, and maintain realistic engagement with fraudsters.

The system simulates a human persona in multi-turn SMS/WhatsApp-style conversations to:

Detect fraudulent intent

Sustain engagement to gather intelligence

Extract structured entities (phone numbers, bank accounts, UPI IDs, etc.)

Submit a final structured report for evaluation


The architecture is fully generic and does not rely on hardcoded scenario logic. It adapts dynamically to different scam types including bank fraud, UPI fraud, phishing, impersonation scams, and more.


---

## Tech Stack

### Language / Framework

Python 3.10+

FastAPI – API framework

Uvicorn – ASGI server


### Key Libraries

fastapi

uvicorn

pydantic

requests

re (regex-based extraction)

datetime

logging


### AI / LLM

OpenAI-compatible LLM API

Used for:

Persona-based reply generation

Agent notes summarization



The LLM is used strictly for conversational realism and analysis. Scam detection and intelligence extraction use rule-based and regex-based logic to avoid hardcoded responses.


---

## Setup Instructions

1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/honeypot-api.git
cd honeypot-api
```

---

2️⃣ Install Dependencies

Create virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

3️⃣ Set Environment Variables

Create a .env file based on .env.example.

Example:

```bash
OPENAI_API_KEY=your_llm_api_key
API_SECRET_KEY=your_x_api_key
GUVI_PRODUCTION_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

Never commit real API keys.


---

4️⃣ Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API will run at:

```bash
http://localhost:8000
```

Swagger docs available at:

```bash
http://localhost:8000/docs
```

---

##API Endpoint

URL

https://your-deployed-url.com/honeypot

Method

POST

Authentication

Header:

x-api-key: your-api-key


---

## Request Format

```python
{
  "sessionId": "uuid-v4-string",
  "message": {
    "sender": "scammer",
    "text": "URGENT: Your account has been compromised...",
    "timestamp": "2025-02-11T10:30:00Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```


---

## Response Format

```python
{
  "status": "success",
  "reply": "Human-like honeypot reply"
}
```

---

## Approach

1️⃣ Scam Detection Strategy

The system uses hybrid detection:

Keyword-based urgency detection

OTP/PIN/freeze/threat pattern detection

Repeated pressure detection

Impersonation signals

Suspicious link presence

Detection logic is generic and adaptable across different fraud types.

No scenario-specific hardcoding is used.


---

2️⃣ Intelligence Extraction Strategy

Extraction is rule-based using regex and contextual filtering.

### Extracted Entities

📞 Phone Numbers (mobile, toll-free, landline)

🏦 Bank Account Numbers (11–18 digits)

💳 UPI IDs

📧 Email Addresses

🔗 Phishing URLs

🆔 Case IDs

📄 Policy Numbers

📦 Order Numbers

🚨 Suspicious Keywords


### Context-aware extraction prevents:

Overlapping entity misclassification

False positives

Duplicate extraction


Extraction accumulates across conversation turns.


---

3️⃣ Engagement Strategy

### The honeypot persona:

Simulates a realistic middle-aged non-technical user

Gradually transitions from calm confusion to anxiety

Identifies red flags (urgency, threats, OTP demand)

Elicits information (ID, phone, website, case number, etc.)

Avoids revealing sensitive data (OTP, PIN, account)


### Conversation objectives:

Sustain ≥8 turns

Ask investigative questions

Trigger scammer to reveal intelligence

Maintain natural tone


### The LLM is guided via structured system prompts to:

Avoid repetition

Avoid robotic responses

Avoid explicit scam accusations

Maintain SMS-style brevity



---

4️⃣ Engagement Metrics

The system tracks:

Total messages exchanged

Engagement duration (real-time)

Conversation depth


These metrics align with evaluation scoring criteria.


---

5️⃣ Final Callback Submission

After conversation completion, a structured payload is sent:

```bash
{
  "sessionId": "...",
  "scamDetected": true,
  "totalMessagesExchanged": 18,
  "engagementDurationSeconds": 120,
  "extractedIntelligence": { ... },
  "agentNotes": "...",
  "scamType": "...",
  "confidenceLevel": 0.92
}
```

Callback is sent once per session after sufficient engagement.


---

## Project Structure

app/
├── main.py
├── gatekeeper.py
├── extractor.py
├── persona_agent.py
├── agent_notes_llm.py
├── callback.py
├── memory.py
├── schemas.py
└── utils.py

docs/
└── architecture.md

requirements.txt
.env.example
README.md


---

## Security & Compliance

No hardcoded scenario logic

No evaluation traffic detection

No sensitive data storage

No secret keys committed

Strict persona guardrails

Timeout-safe (<30 seconds per request)



---

## Future Enhancements

ML-based scam classification

Adaptive elicitation strategy

Persistent session database

Fraud risk scoring

Monitoring dashboard

Multi-language support



---

## Conclusion

This honeypot system combines:

Rule-based intelligence extraction

Heuristic scam detection

LLM-powered realistic engagement

Structured evaluation-compliant reporting


The architecture is modular, scalable, and fully aligned with hackathon evaluation requirements.
readme.md
Displaying readme.md.