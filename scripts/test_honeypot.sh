#!/usr/bin/env bash
URL="http://localhost:8000/honeypot"
cat <<'JSON' | curl -s -X POST "$URL" -H "Content-Type: application/json" -H "x-api-key: test-key" -d @-
{
  "sessionId": "local-test-123",
  "message": { "sender": "scammer", "text": "Send money to UPI abc@bank" },
  "conversationHistory": []
}
JSON
echo
