# ⚡ Quick Slack Bot Test Guide

## 🎯 Easiest Way to Test Right Now

### Method 1: Test via Messages Page (No Slack Setup Needed)

This tests the full AI chatbot without needing Slack event configuration:

1. **Configure Azure OpenAI** (if not done):
   - Go to Settings
   - Enter Azure OpenAI credentials
   - Test connection

2. **Go to Messages Page:**
   - http://localhost:3000/messages

3. **Chat with AI:**
   ```
   You: "Hello! Can you explain what you can do?"
   AI: [Responds with capabilities]
   
   You: "What's the weather like today?"
   AI: [Provides response]
   
   You: "Can you help me write an email?"
   AI: [Helps with email]
   ```

4. **View History:**
   - See all previous messages
   - Check token usage
   - View response times

✅ **This fully tests the AI agent!**

---

## Method 2: Test Slack Connection (Verify Credentials)

### Quick Connection Test:

1. **Go to Settings:** http://localhost:3000/settings

2. **Scroll to "Slack Configuration"**

3. **If not configured:**
   - Get Bot Token from: https://api.slack.com/apps
   - Get Signing Secret
   - Enter in form
   - Click "Save Credentials"

4. **Click "Test Connection"**

5. **Expected Result:**
   ```
   ✅ Connected to workspace: [Your Workspace Name]
   ```

This verifies:
- ✅ Bot token is valid
- ✅ Bot is installed in workspace
- ✅ Can authenticate with Slack API

---

## Method 3: Send Message to Slack Channel

### Using API Docs Interface:

1. **Go to API Docs:** http://localhost:8000/docs

2. **Authorize:**
   - Click "Authorize" button (top right)
   - Enter your access token (from login)
   - Click "Authorize"

3. **Find POST `/api/agent/message`**

4. **Click "Try it out"**

5. **Enter:**
   ```json
   {
     "message": "Hello from my AI bot! Can you introduce yourself?",
     "channel_id": "test-channel"
   }
   ```

6. **Click "Execute"**

7. **Check Response:**
   ```json
   {
     "success": true,
     "response": "Hello! I'm an AI assistant...",
     "tokens_used": 50,
     "execution_time_ms": 1200
   }
   ```

8. **This tests:**
   - ✅ AI generates response
   - ✅ Message is stored
   - ✅ Tokens are counted
   - ✅ Response time tracked

---

## Method 4: Test via Python Script

Create a test script to verify everything works:

**File:** `test_bot.py`
```python
import requests

# Your credentials
BASE_URL = "http://localhost:8000"
USERNAME = "your_username"
PASSWORD = "your_password"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": USERNAME, "password": PASSWORD}
)
token = login_response.json()["access_token"]

# 2. Send message to AI
headers = {"Authorization": f"Bearer {token}"}
message_response = requests.post(
    f"{BASE_URL}/api/agent/message",
    headers=headers,
    json={
        "message": "What is artificial intelligence?",
        "channel_id": "test"
    }
)

# 3. Print result
print("✅ AI Response:")
print(message_response.json()["response"])
print(f"\n📊 Tokens used: {message_response.json()['tokens_used']}")
```

**Run it:**
```bash
python test_bot.py
```

---

## 🔥 Real Slack Channel Testing (Advanced)

If you want the bot to actually respond in Slack channels:

### Prerequisites:
1. ✅ Slack app created with bot scopes
2. ✅ Bot installed to workspace
3. ✅ ngrok or public URL for webhook

### Steps:

#### 1. Install ngrok
```bash
# Download from https://ngrok.com/download
# Or install via npm:
npm install -g ngrok
```

#### 2. Start ngrok
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

#### 3. Create Slack Event Endpoint

I can create this for you! Would you like me to add a Slack event handler that:
- Listens for Slack messages
- Responds with AI automatically
- Posts responses back to Slack

---

## 🎯 What I Recommend

### For Testing AI Functionality:

**Use the Messages Page** ⭐ (Easiest)
- Go to http://localhost:3000/messages
- Chat directly with AI
- No Slack event setup needed
- Full functionality

### For Testing Slack Integration:

**Use Test Connection** ⭐
- Settings → Slack Configuration
- Click "Test Connection"
- Verifies Slack credentials work

### For Production:

**Add Slack Event Handler**
- I can help you add this
- Bot responds in Slack channels
- Real-time interactions

---

## 📊 Test Checklist

- [ ] Azure OpenAI configured and tested
- [ ] Slack credentials saved
- [ ] Slack connection tested (shows workspace name)
- [ ] Messages page works (can chat with AI)
- [ ] Messages are saved to database
- [ ] Token usage is tracked
- [ ] Can view message history
- [ ] Dashboard shows statistics

---

## 🆘 Quick Troubleshooting

**Q: Can't send messages in Messages page**
A: Configure Azure OpenAI first (Settings → Azure OpenAI Configuration)

**Q: Slack test connection fails**
A: Verify bot token starts with `xoxb-` and is from correct workspace

**Q: Want bot to respond in Slack channels**
A: Need to add event handler endpoint (I can help with this)

**Q: AI responses are slow**
A: Normal - Azure OpenAI can take 1-3 seconds. Check execution_time_ms

---

## 🎊 Summary

**Fastest Test:** 
→ Messages page at http://localhost:3000/messages

**Most Complete Test:**
→ Configure all services → Test each → Use Messages & Summaries

**Production Test:**
→ Deploy → Configure Slack events → Bot responds in channels

---

**Want me to add real-time Slack channel response capability? Let me know!** 🚀
