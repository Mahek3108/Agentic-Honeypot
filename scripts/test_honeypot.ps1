$url = "http://localhost:8000/honeypot"
$body = @{
    sessionId = "local-test-123"
    message = @{ sender = "scammer"; text = "Please transfer to UPI ID abc@bank" }
    conversationHistory = @()
} | ConvertTo-Json -Depth 5

Write-Host "Posting to $url:`n$body"

Invoke-RestMethod -Uri $url -Method POST -Body $body -ContentType "application/json" -Headers @{ "x-api-key" = "test-key" }
