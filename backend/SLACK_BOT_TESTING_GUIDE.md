# 🤖 Slack Chatbot Testing Guide

## Overview

Your Slack bot can respond to messages using Azure OpenAI. Here's how to set it up and test it.

---

## 📋 Prerequisites

Before testing, you need:
- ✅ Slack workspace (free tier works)
- ✅ Azure OpenAI configured in your app
- ✅ Slack app credentials configured

---

## Part 1: Create Slack App

### Step 1: Create Slack App

1. **Go to:** https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. **App Name:** `AI Agent Bot` (or your choice)
5. **Workspace:** Select your workspace
6. Click **"Create App"**

---

### Step 2: Configure Bot User

1. In left sidebar, click **"OAuth & Permissions"**

2. Scroll to **"Scopes"** section

3. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**

4. Add these scopes:
   - ✅ `chat:write` - Send messages
   - ✅ `chat:write.public` - Send to channels bot isn't in
   - ✅ `channels:history` - Read channel messages
   - ✅ `channels:read` - View channel info
   - ✅ `groups:history` - Read private channel messages
   - ✅ `im:history` - Read DM messages
   - ✅ `im:write` - Send DMs
   - ✅ `users:read` - View user info
   - ✅ `app_mentions:read` - See when bot is mentioned

5. Scroll up to **"OAuth Tokens for Your Workspace"**

6. Click **"Install to Workspace"**

7. Review permissions and click **"Allow"**

8. **Copy the "Bot User OAuth Token"**
   - Starts with `xoxb-`
   - Example: `xoxb-XXXX-XXXX-XXXX`
   - **Save this!**

---

### Step 3: Get Signing Secret

1. In left sidebar, click **"Basic Information"**

2. Scroll to **"App Credentials"** section

3. Under **"Signing Secret"**, click **"Show"**

4. **Copy the Signing Secret**
   - Random string like: `abc123def456ghi789jkl012mno345pq`
   - **Save this!**

---

### Step 4: Enable Events (For Real-time Bot)

1. In left sidebar, click **"Event Subscriptions"**

2. Toggle **"Enable Events"** to **ON**

3. **Request URL:** 
   - For local testing, you'll need ngrok or similar
   - We'll start with simpler testing first (see Part 3)
   - You can skip this for now

---

## Part 2: Configure in Your App

### Step 1: Go to Settings

1. Open your app: http://localhost:3000
2. Login
3. Go to **Settings** page

### Step 2: Configure Slack Credentials

1. Scroll to **"Slack Configuration"** section

2. **Fill in the form:**
   - **Bot Token:** `xoxb-your-token-here` (paste from Slack)
   - **Signing Secret:** `your-signing-secret` (paste from Slack)
   - **App Token:** Leave empty (optional for socket mode)

3. Click **"Save Credentials"**

4. Wait for success message

5. Click **"Test Connection"**

6. Should see: ✅ **"Connected to workspace: [Your Workspace Name]"**

---

## Part 3: Testing Methods

### Method 1: Test via Portal Messages (Easiest)

This tests the AI functionality without Slack's event system:

1. **Go to Messages** page in your app

2. **Type a message:**
   ```
   Hello! Can you help me summarize a document?
   ```

3. **Click Send**

4. **AI responds** using Azure OpenAI ✅

5. **Check Dashboard** to see token usage

**What this tests:**
- ✅ Azure OpenAI integration
- ✅ Message storage
- ✅ Token tracking
- ✅ Response generation

**What it doesn't test:**
- ❌ Actual Slack message events
- ❌ Slack channel posting

---

### Method 2: Test Slack Messaging Directly

Test sending messages to Slack channels:

#### Using the Backend API:

**Via API Docs:**
1. Go to: http://localhost:8000/docs
2. Find **POST `/api/agent/message`**
3. Click "Try it out"
4. Enter:
   ```json
   {
     "message": "Test message from AI bot",
     "channel_id": "C1234567890"
   }
   ```
   (Replace with your actual Slack channel ID)
5. Click "Execute"

**How to get Channel ID:**
1. Open Slack in browser or desktop
2. Right-click on a channel
3. Click "View channel details"
4. Scroll down - the Channel ID is at the bottom
5. Example: `C05XXXXXXXX`

---

### Method 3: Direct Slack API Test

Test if your bot can post to Slack:

**Using curl (PowerShell):**
```powershell
# Get your token from Settings or database
$token = "xoxb-your-bot-token-here"
$channel = "C1234567890"  # Your channel ID

# Send a test message
$body = @{
    channel = $channel
    text = "Hello from AI Bot! 🤖"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://slack.api/chat.postMessage" -Method POST -Headers @{Authorization = "Bearer $token"} -Body $body -ContentType "application/json"
```

---

### Method 4: Test with Slack Events (Advanced)

For real-time bot responses in Slack, you need to expose your local server:

#### Option A: Using ngrok

1. **Install ngrok:**
   - Download from: https://ngrok.com/download
   - Or: `npm install -g ngrok`

2. **Start ngrok:**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL:**
   ```
   Forwarding: https://abc123.ngrok.io → http://localhost:8000
   ```

4. **Update Slack App:**
   - Go to: https://api.slack.com/apps → Your App
   - Click "Event Subscriptions"
   - Request URL: `https://abc123.ngrok.io/api/slack/events`
   - (Note: You'll need to create this endpoint - see below)

5. **Subscribe to bot events:**
   - `message.channels` - Messages in channels
   - `message.im` - Direct messages
   - `app_mention` - When bot is mentioned

6. **Save Changes**

#### Option B: Deploy to Cloud (Production)

For production testing:
1. Deploy backend to cloud (Heroku, AWS, GCP)
2. Use actual domain for webhook URL
3. Configure in Slack app settings

---

## Part 4: Current Testing Capabilities

### What Works Right Now:

#### 1. ✅ Messages Page (Portal)
- Chat with AI through web interface
- View conversation history
- Track token usage
- Test AI responses

#### 2. ✅ API Testing
- Use `/api/agent/message` endpoint
- Send messages programmatically
- Get AI responses
- Store in database

#### 3. ✅ Summary Generation
- Generate AI summaries
- Save to Google Drive
- Track usage

---

## Part 5: Adding Slack Event Handler (Optional)

If you want the bot to respond to Slack messages in real-time, you need to add an event handler endpoint:

### Create Slack Webhook Endpoint

**File:** `backend/routes/slack_events.py` (Create this)

```python
from fastapi import APIRouter, Request, HTTPException
from services.credential_service import CredentialService
from services.agent_service import AgentService
from database import get_db
import hmac
import hashlib
import time

router = APIRouter(prefix="/api/slack", tags=["Slack Events"])

@router.post("/events")
async def slack_events(request: Request):
    """Handle Slack events"""
    body = await request.body()
    
    # Verify Slack signature (security)
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    
    # Parse JSON
    event_data = await request.json()
    
    # Handle URL verification challenge
    if event_data.get("type") == "url_verification":
        return {"challenge": event_data.get("challenge")}
    
    # Handle message events
    if event_data.get("event", {}).get("type") == "message":
        # Process message with AI
        # (Implementation needed)
        pass
    
    return {"ok": True}
```

Then add to main.py:
```python
from routes import slack_events
app.include_router(slack_events.router)
```

---

## 🎯 Recommended Testing Workflow

### For Development/Testing:

**Use the Portal Messages Page:**
1. ✅ Go to http://localhost:3000/messages
2. ✅ Type your questions
3. ✅ Get AI responses
4. ✅ View history
5. ✅ Track usage

**Why this is good:**
- No need for ngrok or public URL
- No Slack event configuration needed
- Tests all AI functionality
- Simpler to debug

### For Production:

**Set up Slack Events:**
1. Deploy to cloud
2. Configure Slack webhooks
3. Bot responds in Slack channels
4. Real-time interactions

---

## 📊 Current Features You Can Test

### 1. AI Chat (Messages Page)
```
You: "What is the capital of France?"
Bot: "The capital of France is Paris..."
```

### 2. AI Summaries
```
Content: [Long article]
→ Generate Summary
→ AI creates concise summary
→ Saves to Google Drive
→ Returns shareable link
```

### 3. Conversation Tracking
- All messages stored in database
- Token usage tracked
- Response times recorded
- Available in admin dashboard

---

## 🔍 Verify Slack Integration

### Test Slack Connection:

1. **In Settings:**
   - Scroll to "Slack Configuration"
   - Click "Test Connection"
   - Should see: ✅ "Connected to workspace: [Name]"

2. **Check what works:**
   - ✅ Bot token is valid
   - ✅ Can authenticate with Slack
   - ✅ Bot is installed in workspace
   - ✅ Credentials are saved

---

## 💡 Quick Test Scenarios

### Scenario 1: Ask a Question
```
Message: "Explain quantum computing in simple terms"
Expected: AI provides clear explanation
```

### Scenario 2: Request Summary
```
Message: "Please summarize: [paste long text]"
OR
Go to Summaries → Create Summary → AI generates summary
```

### Scenario 3: Multiple Conversations
```
Send several messages
View history in Messages page
See all tracked in database
Check token usage in Dashboard
```

---

## 🐛 Troubleshooting

### Issue: "Azure OpenAI not configured"

**Solution:**
1. Go to Settings
2. Configure Azure OpenAI credentials
3. Test the connection
4. Then try sending messages

### Issue: Can't send messages in Portal

**Solution:**
1. Check Azure OpenAI is configured
2. Test Azure OpenAI connection
3. Check browser console for errors
4. Verify backend logs

### Issue: Want bot to respond in Slack channels

**Solution:**
Currently the bot works through the portal. To enable Slack channel responses:
1. Need to add Slack event handler endpoint
2. Use ngrok for local testing
3. Or deploy to production
4. Configure webhook URL in Slack app

---

## 📈 What Gets Tracked

When you send messages:

**In Database:**
- ✅ Message content
- ✅ AI response
- ✅ Tokens used
- ✅ Response time
- ✅ Timestamp

**In Admin Dashboard:**
- ✅ Total messages count
- ✅ Total tokens used
- ✅ Total cost
- ✅ Usage statistics
- ✅ Audit logs

---

## 🎯 Summary

### Current Testing:
- ✅ **Messages Page** - Chat with AI through web portal
- ✅ **API Endpoint** - Send messages via `/api/agent/message`
- ✅ **Summaries** - Generate and save to Google Drive

### For Slack Channel Responses:
- ⚠️ Requires Slack event webhook setup
- ⚠️ Requires public URL (ngrok or deployment)
- ⚠️ Additional endpoint implementation needed

### Recommended:
**Start with the Messages page** - it fully tests the AI capabilities without needing Slack event configuration!

---

## 🚀 Quick Start Testing

**Fastest way to test right now:**

1. **Ensure Azure OpenAI is configured** in Settings
2. **Go to Messages** page
3. **Type:** "Hello! Can you help me?"
4. **Click Send**
5. **AI responds** with intelligent answer ✅
6. **Check Dashboard** for usage stats

**This fully tests:**
- AI integration
- Message processing
- Response generation
- Token tracking
- Database storage

---

## 📝 Next Steps

If you want Slack channel integration:
1. I can create the Slack event handler endpoint
2. You can use ngrok for local testing
3. Or deploy to production for permanent webhook

**Let me know if you want me to add the Slack event handler!**

For now, the **Messages page** provides full AI chatbot functionality without needing Slack event setup.

---

**Ready to test?** Just make sure Azure OpenAI is configured and go to the Messages page! 🚀
